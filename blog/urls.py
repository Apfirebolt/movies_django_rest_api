from django.urls import path
from django.conf.urls.static import static
from django_movie_api import settings
from .views import BlogListView, BlogPostListView, ProjectListView, ProjectDetailView, GalleryPostListView, \
    GalleryPostDetailView, BlogDetailView, BlogPostDetailView


urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog'),
    path('blog-posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('blog-post/<int:pk>/', BlogPostDetailView.as_view(), name='blog-post'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project'),
    path('gallery-posts/', GalleryPostListView.as_view(), name='gallery-posts'),
    path('gallery-post/<int:pk>/', GalleryPostDetailView.as_view(), name='gallery-post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
