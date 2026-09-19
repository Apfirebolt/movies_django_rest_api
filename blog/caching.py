# blog/caching.py
import math
from django.core.cache import cache
from django.db.models import Prefetch

from blog.models import Project, ProjectImages
from api.serializers import DetailProjectSerializer, ListProjectSerializer

PAGE_SIZE = 25
KEY_PREFIX = "api:projects:page:"
KEY_DETAIL_PREFIX = "api:projects:detail:"
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


def warm_project_detail_cache(project_id: int):
    """Caches a single project's detail payload indefinitely."""
    try:
        instance = (
            Project.objects.filter(is_published=True)
            .select_related("author")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=ProjectImages.objects.order_by("id"),
                ),
            )
            .get(id=project_id)
        )
        payload = DetailProjectSerializer(instance).data
        cache.set(f"{KEY_DETAIL_PREFIX}{project_id}", payload, timeout=None)
        return payload
    except Project.DoesNotExist:
        cache.delete(f"{KEY_DETAIL_PREFIX}{project_id}")
        return None


def warm_projects_list_cache():
    """Computes and stores all paginated list responses directly in Redis."""
    qs = get_optimized_projects_queryset()
    total_count = qs.count()

    if total_count == 0:
        cache.set(
            f"{KEY_PREFIX}1",
            {"count": 0, "next": None, "previous": None, "results": []},
            timeout=None,
        )
        cache.set(KEY_TOTAL_PAGES, 1, timeout=None)
        return

    total_pages = math.ceil(total_count / PAGE_SIZE)
    cache.set(KEY_TOTAL_PAGES, total_pages, timeout=None)

    cache_payloads = {}
    for page_num in range(1, total_pages + 1):
        offset = (page_num - 1) * PAGE_SIZE
        page_items = qs[offset : offset + PAGE_SIZE]

        payload = {
            "count": total_count,
            "page": page_num,
            "total_pages": total_pages,
            "results": ListProjectSerializer(page_items, many=True).data,
        }
        cache_payloads[f"{KEY_PREFIX}{page_num}"] = payload

    cache.set_many(cache_payloads, timeout=None)


def warm_all_projects_cache():
    """Warms both the paginated lists and every individual project detail."""
    warm_projects_list_cache()

    # Pre-populate all individual project detail keys in one multi-set
    projects = get_optimized_projects_queryset()
    detail_payloads = {
        f"{KEY_DETAIL_PREFIX}{project.id}": DetailProjectSerializer(project).data
        for project in projects
    }
    if detail_payloads:
        cache.set_many(detail_payloads, timeout=None)


def invalidate_and_rewarm_projects(project_id=None):
    """
    Cleans up stale page keys and detail keys, then immediately repopulates.
    Visitors will never experience a cache miss.
    """
    # 1. Clear and re-warm detail cache if a specific project ID is provided
    if project_id:
        cache.delete(f"{KEY_DETAIL_PREFIX}{project_id}")
        warm_project_detail_cache(project_id)

    # 2. Invalidate existing page list keys
    total_pages = cache.get(KEY_TOTAL_PAGES, 10)
    keys_to_delete = [f"{KEY_PREFIX}{i}" for i in range(1, total_pages + 5)]
    keys_to_delete.append(KEY_TOTAL_PAGES)
    cache.delete_many(keys_to_delete)

    # 3. Immediately rebuild list pages
    warm_projects_list_cache()