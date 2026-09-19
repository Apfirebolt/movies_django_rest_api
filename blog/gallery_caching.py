import math
from django.core.cache import cache
from django.db.models import Prefetch

from blog.models import GalleryPost, GalleryPostImages
from api.serializers import ListGalleryPostSerializer, DetailGalleryPostSerializer

PAGE_SIZE = 25
GALLERY_PAGE_PREFIX = "api:gallery:page:"
GALLERY_DETAIL_PREFIX = "api:gallery:detail:"
GALLERY_TOTAL_PAGES_KEY = "api:gallery:total_pages"


def get_optimized_gallery_queryset():
    """Base queryset with single-query joins for authors, tags, and ordered images."""
    return (
        GalleryPost.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related(
            "tags",
            Prefetch(
                "images",
                queryset=GalleryPostImages.objects.order_by("order", "id"),
            ),
        )
        .order_by("-date_posted", "-id")
    )


def warm_gallery_detail_cache(post_id: int):
    """Caches a single gallery post's detail payload indefinitely."""
    try:
        instance = (
            GalleryPost.objects.filter(is_published=True)
            .select_related("author")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=GalleryPostImages.objects.order_by("order", "id"),
                ),
            )
            .get(id=post_id)
        )
        payload = DetailGalleryPostSerializer(instance).data
        cache.set(f"{GALLERY_DETAIL_PREFIX}{post_id}", payload, timeout=None)
        return payload
    except GalleryPost.DoesNotExist:
        cache.delete(f"{GALLERY_DETAIL_PREFIX}{post_id}")
        return None


def warm_gallery_list_cache():
    """Pre-computes and caches all paginated pages of published gallery posts."""
    qs = get_optimized_gallery_queryset()
    total_count = qs.count()

    if total_count == 0:
        cache.set(f"{GALLERY_PAGE_PREFIX}1", {"count": 0, "results": []}, timeout=None)
        cache.set(GALLERY_TOTAL_PAGES_KEY, 1, timeout=None)
        return

    total_pages = math.ceil(total_count / PAGE_SIZE)
    cache.set(GALLERY_TOTAL_PAGES_KEY, total_pages, timeout=None)

    cache_payloads = {}
    for page_num in range(1, total_pages + 1):
        offset = (page_num - 1) * PAGE_SIZE
        page_items = qs[offset : offset + PAGE_SIZE]
        cache_payloads[f"{GALLERY_PAGE_PREFIX}{page_num}"] = {
            "count": total_count,
            "page": page_num,
            "total_pages": total_pages,
            "results": ListGalleryPostSerializer(page_items, many=True).data,
        }
    cache.set_many(cache_payloads, timeout=None)


def warm_all_gallery_cache():
    """Warms both the paginated lists and every individual post detail."""
    warm_gallery_list_cache()
    
    posts = get_optimized_gallery_queryset()
    detail_payloads = {
        f"{GALLERY_DETAIL_PREFIX}{post.id}": DetailGalleryPostSerializer(post).data
        for post in posts
    }
    if detail_payloads:
        cache.set_many(detail_payloads, timeout=None)


def invalidate_and_rewarm_gallery(post_id=None):
    """
    Cleans up stale list keys and detail cache, then immediately repopulates.
    Visitors will never experience a cache miss.
    """
    # 1. Clear and re-warm detail cache if specific post ID is given
    if post_id:
        cache.delete(f"{GALLERY_DETAIL_PREFIX}{post_id}")
        warm_gallery_detail_cache(post_id)

    # 2. Invalidate existing page keys
    total_pages = cache.get(GALLERY_TOTAL_PAGES_KEY, 10)
    keys_to_delete = [f"{GALLERY_PAGE_PREFIX}{i}" for i in range(1, total_pages + 5)]
    keys_to_delete.append(GALLERY_TOTAL_PAGES_KEY)
    cache.delete_many(keys_to_delete)

    # 3. Immediately rebuild list pages
    warm_gallery_list_cache()