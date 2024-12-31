from django.views.generic import DetailView, ListView
from .models import Blog, Project, GalleryPost, BlogPost
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/detail_blog.html'


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/list_blog.html'
    context_object_name = 'blogs'


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project/detail_project.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'project/list_project.html'
    context_object_name = 'projects'


class GalleryPostDetailView(DetailView):
    model = GalleryPost
    context_object_name = 'gallery_post'
    template_name = 'gallery/detail_gallery_post.html'


class GalleryPostListView(ListView):
    model = GalleryPost
    template_name = 'gallery/list_gallery_post.html'
    context_object_name = 'gallery_posts'


class BlogPostDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blog_post'
    template_name = 'blog/detail_blog_post.html'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/list_blog_post.html'
    context_object_name = 'blog_posts'