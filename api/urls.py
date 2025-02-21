from django.urls import path
from .views import (
    ListMovieApiView,
    DetailMovieApiView,
    ListGameApiView,
    ListNetflixApiView,
    DetailGameApiView,
    CreateCustomUserApiView,
    ListBlogApiView,
    CreateBlogApiView,
    ListBlogPostApiView,
    DetailBlogApiView,
    CreateBlogPostApiView,
    DetailBlogPostApiView,
    CreateBlogImageApiView,
    CreatePostImageApiView,
    CreateProjectApiView,
    ListProjectApiView,
    ProjectDetailApiView, 
    ListCreateTagsApiView,
    TagDetailApiView,
    ListGalleryPostApiView,
    CreateGalleryPostApiView,
    GalleryPostDetailApiView,
    GenericImageListApiView,
    ListItemApiView,
    ListFundApiView,
    ListDinosaurApiView,
    ListPlanetApiView
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
    path("blogs/add", CreateBlogApiView.as_view(), name="add-blogs"),
    path("blogs/<int:pk>", DetailBlogApiView.as_view(), name="detail-blogs"),
    path("blog-posts", ListBlogPostApiView.as_view(), name="list-create-blog-posts"),
    path("blog-posts/<int:pk>", DetailBlogPostApiView.as_view(), name="detail-blog-posts"),
    path("blog-posts/add", CreateBlogPostApiView.as_view(), name="add-blog-posts"),
    path("blog-images", CreateBlogImageApiView.as_view(), name="create-blog-images"),
    path("post-images", CreatePostImageApiView.as_view(), name="create-post-images"),
    path("projects", ListProjectApiView.as_view(), name="list-projects"),
    path("projects/add", CreateProjectApiView.as_view(), name="add-projects"),
    path("projects/<int:pk>", ProjectDetailApiView.as_view(), name="detail-projects"),
    path("gallery-posts", ListGalleryPostApiView.as_view(), name="list-create-gallery-posts"),
    path("gallery-posts/add", CreateGalleryPostApiView.as_view(), name="add-gallery-posts"),
    path("gallery-posts/<int:pk>", GalleryPostDetailApiView.as_view(), name="detail-gallery-posts"),
    path("tags", ListCreateTagsApiView.as_view(), name="list-create-tags"),
    path("tags/<int:pk>", TagDetailApiView.as_view(), name="detail-tags"),
    path("generic-images", GenericImageListApiView.as_view(), name="list-images"),

    path("funds", ListFundApiView.as_view(), name="list-funds"),
    path("netflix", ListNetflixApiView.as_view(), name="list-create-netflix"),
    path("movies", ListMovieApiView.as_view(), name="list-create-movies"),
    path("movies/<int:pk>", DetailMovieApiView.as_view(), name="detail-movies"),
    path("games", ListGameApiView.as_view(), name="list-create-games"),
    path("games/<int:pk>", DetailGameApiView.as_view(), name="detail-games"),
    path("items", ListItemApiView.as_view(), name="list-items"),
    path("dinosaur", ListDinosaurApiView.as_view(), name="list-dinosaur"),
    path("planets", ListPlanetApiView.as_view(), name="list-planet"),
]
