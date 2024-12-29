from django.contrib import admin
from .models import Blog, BlogPost, PostImage, BlogImage, Project, ProjectImages, Tags, GalleryPost, GalleryPostImages


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'date_updated', 'views')
    list_filter = ('date_posted', 'date_updated')
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'
    ordering = ['date_posted']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost)
admin.site.register(PostImage)
admin.site.register(BlogImage)
admin.site.register(Project)
admin.site.register(ProjectImages)
admin.site.register(Tags)
admin.site.register(GalleryPost)
admin.site.register(GalleryPostImages)
