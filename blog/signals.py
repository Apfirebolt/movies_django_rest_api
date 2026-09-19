from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .gallery_caching import invalidate_and_rewarm_gallery
from .models import GalleryPost, GalleryPostImages, Project, ProjectImages

# ==========================================
# Project Invalidation
# ==========================================


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


# ==========================================
# Gallery Post Invalidation & Re-warming
# ==========================================


@receiver([post_save, post_delete], sender=GalleryPost)
def handle_gallery_post_change(sender, instance, **kwargs):
    invalidate_and_rewarm_gallery(post_id=instance.id)


@receiver([post_save, post_delete], sender=GalleryPostImages)
def handle_gallery_image_change(sender, instance, **kwargs):
    if instance.post_id:
        invalidate_and_rewarm_gallery(post_id=instance.post_id)


@receiver(m2m_changed, sender=GalleryPost.tags.through)
def handle_gallery_tags_change(sender, instance, action, **kwargs):
    # M2M updates don't fire post_save on the post itself
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_and_rewarm_gallery(post_id=instance.id)