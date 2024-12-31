from django.views.generic import DetailView, ListView
from .models import Blog, Project, GalleryPost, BlogPost
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog-detail.html'


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog-list.html'
    context_object_name = 'blogs'


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project-detail.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project-list.html'
    context_object_name = 'projects'


class GalleryPostDetailView(DetailView):
    model = GalleryPost
    context_object_name = 'gallery_post'
    template_name = 'gallery/gallery-detail.html'


class GalleryPostListView(ListView):
    model = GalleryPost
    template_name = 'gallery/gallery-list.html'
    context_object_name = 'gallery_posts'


class BlogPostDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blog_post'
    template_name = 'blog/post-detail.html'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post-list.html'
    context_object_name = 'blog_posts'