# blog/caching.py
import math
from django.core.cache import cache
from django.db.models import Prefetch
from blog.models import Project, ProjectImages
from api.serializers import ListProjectSerializer

PAGE_SIZE = 25
KEY_PREFIX = "api:projects:page:"
KEY_TOTAL_PAGES = "api:projects:total_pages"


def get_optimized_projects_queryset():
    """Returns the base queryset with all necessary joins."""
    return (
        Project.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related(
            "tags",
            Prefetch(
                "images",
                queryset=ProjectImages.objects.order_by("id"),
            ),
        )
        .order_by("-id")
    )


def warm_projects_cache():
    """
    Computes and stores all paginated responses directly in Redis.
    With 50-200 items, this generates 2-8 Redis keys instantly.
    """
    qs = get_optimized_projects_queryset()
    total_count = qs.count()

    if total_count == 0:
        cache.set(f"{KEY_PREFIX}1", {"count": 0, "next": None, "previous": None, "results": []}, timeout=None)
        cache.set(KEY_TOTAL_PAGES, 1, timeout=None)
        return

    total_pages = math.ceil(total_count / PAGE_SIZE)
    cache.set(KEY_TOTAL_PAGES, total_pages, timeout=None)

    cache_payloads = {}
    for page_num in range(1, total_pages + 1):
        offset = (page_num - 1) * PAGE_SIZE
        page_items = qs[offset : offset + PAGE_SIZE]

        # Structure payload to match standard DRF paginated output
        payload = {
            "count": total_count,
            "page": page_num,
            "total_pages": total_pages,
            "results": ListProjectSerializer(page_items, many=True).data,
        }
        cache_payloads[f"{KEY_PREFIX}{page_num}"] = payload

    # Save all pages in one round-trip to Redis with no expiration
    cache.set_many(cache_payloads, timeout=None)


def invalidate_and_rewarm_projects():
    """Wipes old project page keys and immediately repopulates fresh ones."""
    total_pages = cache.get(KEY_TOTAL_PAGES, 10)  # Default lookback buffer
    
    # Clean up existing page keys
    keys_to_delete = [f"{KEY_PREFIX}{i}" for i in range(1, total_pages + 5)]
    keys_to_delete.append(KEY_TOTAL_PAGES)
    cache.delete_many(keys_to_delete)

    # Immediately warm fresh data
    warm_projects_cache()