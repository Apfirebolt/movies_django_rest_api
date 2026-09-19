# blog/blog_caching.py
import math
from django.core.cache import cache
from django.db.models import Prefetch

from blog.models import BlogPost, PostImage
from api.serializers import ListBlogPostSerializer

PAGE_SIZE = 25  # Match your CustomPagination page size
BLOG_PAGE_PREFIX = "api:blogs:page:"
BLOG_DETAIL_PREFIX = "api:blogs:detail:"
BLOG_TOTAL_PAGES_KEY = "api:blogs:total_pages"


def get_optimized_blog_queryset():
    """Optimized base queryset with single-trip joins for author, tags, and ordered images."""
    return (
        BlogPost.objects.filter(is_published=True)
        .select_related("author", "blog")
        .prefetch_related(
            "tags",
            Prefetch(
                "images",
                queryset=PostImage.objects.order_by("order", "id"),
            ),
        )
        .order_by("-date_posted", "-id")
    )


def warm_blog_detail_cache(post_id: int):
    """Caches a single blog post's detail payload indefinitely."""
    try:
        instance = (
            BlogPost.objects.filter(is_published=True)
            .select_related("author", "blog")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=PostImage.objects.order_by("order", "id"),
                ),
            )
            .get(id=post_id)
        )
        payload = ListBlogPostSerializer(instance).data
        cache.set(f"{BLOG_DETAIL_PREFIX}{post_id}", payload, timeout=None)
        return payload
    except BlogPost.DoesNotExist:
        cache.delete(f"{BLOG_DETAIL_PREFIX}{post_id}")
        return None


def warm_blog_list_cache():
    """Computes and stores all paginated list responses directly in Redis."""
    qs = get_optimized_blog_queryset()
    total_count = qs.count()

    if total_count == 0:
        cache.set(
            f"{BLOG_PAGE_PREFIX}1",
            {"count": 0, "next": None, "previous": None, "results": []},
            timeout=None,
        )
        cache.set(BLOG_TOTAL_PAGES_KEY, 1, timeout=None)
        return

    total_pages = math.ceil(total_count / PAGE_SIZE)
    cache.set(BLOG_TOTAL_PAGES_KEY, total_pages, timeout=None)

    cache_payloads = {}
    for page_num in range(1, total_pages + 1):
        offset = (page_num - 1) * PAGE_SIZE
        page_items = qs[offset : offset + PAGE_SIZE]

        payload = {
            "count": total_count,
            "page": page_num,
            "total_pages": total_pages,
            "results": ListBlogPostSerializer(page_items, many=True).data,
        }
        cache_payloads[f"{BLOG_PAGE_PREFIX}{page_num}"] = payload

    cache.set_many(cache_payloads, timeout=None)


def warm_all_blog_cache():
    """Warms both the paginated list pages and all individual post details."""
    warm_blog_list_cache()

    posts = get_optimized_blog_queryset()
    detail_payloads = {
        f"{BLOG_DETAIL_PREFIX}{post.id}": ListBlogPostSerializer(post).data
        for post in posts
    }
    if detail_payloads:
        cache.set_many(detail_payloads, timeout=None)


def invalidate_and_rewarm_blogs(post_id=None):
    """
    Invalidates stale list pages and specific post detail, then repopulates immediately.
    """
    # 1. Clear and re-warm detail key if a post ID was specified
    if post_id:
        cache.delete(f"{BLOG_DETAIL_PREFIX}{post_id}")
        warm_blog_detail_cache(post_id)

    # 2. Invalidate existing page list keys
    total_pages = cache.get(BLOG_TOTAL_PAGES_KEY, 10)
    keys_to_delete = [f"{BLOG_PAGE_PREFIX}{i}" for i in range(1, total_pages + 5)]
    keys_to_delete.append(BLOG_TOTAL_PAGES_KEY)
    cache.delete_many(keys_to_delete)

    # 3. Immediately rebuild list pages
    warm_blog_list_cache()