from django.urls import path
from .views import (
    ListMovieApiView,
    DetailMovieApiView,
    ListGameApiView,
    DetailGameApiView,
    CreateCustomUserApiView,
    ListBlogApiView,
    CreateBlogApiView,
    ListBlogPostApiView,
    CreateBlogPostApiView,
    CreateBlogImageApiView,
    CreatePostImageApiView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register", CreateCustomUserApiView.as_view(), name="signup"),
    path("login", TokenObtainPairView.as_view(), name="signin"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("blogs", ListBlogApiView.as_view(), name="list-create-blogs"),
    path("blogs/add", CreateBlogApiView.as_view(), name="detail-blogs"),
    path("blog-posts", ListBlogPostApiView.as_view(), name="list-create-blog-posts"),
    path("blog-posts/add", CreateBlogPostApiView.as_view(), name="detail-blog-posts"),
    path("blog-images", CreateBlogImageApiView.as_view(), name="create-blog-images"),
    path("post-images", CreatePostImageApiView.as_view(), name="create-post-images"),
    path("movies", ListMovieApiView.as_view(), name="list-create-movies"),
    path("movies/<int:pk>", DetailMovieApiView.as_view(), name="detail-movies"),
    path("games", ListGameApiView.as_view(), name="list-create-games"),
    path("games/<int:pk>", DetailGameApiView.as_view(), name="detail-games"),
]
