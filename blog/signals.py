from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .blog_caching import invalidate_and_rewarm_blogs
from .caching import invalidate_and_rewarm_projects
from .gallery_caching import invalidate_and_rewarm_gallery
from .models import (
    BlogPost,
    GalleryPost,
    GalleryPostImages,
    PostImage,
    Project,
    ProjectImages,
)

# ==========================================
# 1. Project Invalidation & Re-warming
# ==========================================


@receiver([post_save, post_delete], sender=Project)
def handle_project_change(sender, instance, **kwargs):
    invalidate_and_rewarm_projects(project_id=instance.id)


@receiver([post_save, post_delete], sender=ProjectImages)
def handle_project_image_change(sender, instance, **kwargs):
    if instance.project_id:
        invalidate_and_rewarm_projects(project_id=instance.project_id)


@receiver(m2m_changed, sender=Project.tags.through)
def handle_project_tags_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_and_rewarm_projects(project_id=instance.id)


# ==========================================
# 2. Gallery Post Invalidation & Re-warming
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
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_and_rewarm_gallery(post_id=instance.id)


# ==========================================
# 3. Blog Post Invalidation & Re-warming
# ==========================================


@receiver([post_save, post_delete], sender=BlogPost)
def handle_blog_post_change(sender, instance, **kwargs):
    invalidate_and_rewarm_blogs(post_id=instance.id)


@receiver([post_save, post_delete], sender=PostImage)
def handle_blog_image_change(sender, instance, **kwargs):
    if instance.post_id:
        invalidate_and_rewarm_blogs(post_id=instance.post_id)


@receiver(m2m_changed, sender=BlogPost.tags.through)
def handle_blog_tags_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        invalidate_and_rewarm_blogs(post_id=instance.id)