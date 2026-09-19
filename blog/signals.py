from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from .models import Project, ProjectImages


def invalidate_project_cache():
    cache.clear()


@receiver([post_save, post_delete], sender=Project)
def clear_cache_on_project_change(sender, instance, **kwargs):
    invalidate_project_cache()


@receiver([post_save, post_delete], sender=ProjectImages)
def clear_cache_on_project_image_change(sender, instance, **kwargs):
    invalidate_project_cache()


@receiver(m2m_changed, sender=Project.tags.through)
def clear_cache_on_project_tags_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_project_cache()