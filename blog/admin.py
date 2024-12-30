from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Blog, BlogPost, PostImage, BlogImage, Project, ProjectImages, Tags, GalleryPost, GalleryPostImages


class BlogAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date_posted', 'date_updated', 'views')
    list_filter = ('date_posted', 'date_updated')
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'
    ordering = ['date_posted']
    summernote_fields = ('content',)

class ProjectAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date_posted', 'date_updated', 'views', 'project_link', 'technology')
    list_filter = ('date_posted', 'date_updated')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_posted'
    ordering = ['date_posted']
    summernote_fields = ('description',)

class GalleryPostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date_posted', 'date_updated', 'views')
    list_filter = ('date_posted', 'date_updated')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_posted'
    ordering = ['date_posted']
    summernote_fields = ('description',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost)
admin.site.register(PostImage)
admin.site.register(BlogImage)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImages)
admin.site.register(Tags)
admin.site.register(GalleryPost, GalleryPostAdmin)
admin.site.register(GalleryPostImages)
