from django.contrib import admin
from .models import Blog, BlogPost, PostImage, BlogImage


admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(PostImage)
admin.site.register(BlogImage)
