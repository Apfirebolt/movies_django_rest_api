from django.db.models import Prefetch, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from .serializers import (
    ListMovieSerializer,
    ListGameSerializer,
    ListNetflixSerializer,
    ListCustomUserSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    ListBlogSerializer,
    ListBlogPostSerializer,
    ListPostImageSerializer,
    ListBlogImageSerializer,
    ListProjectSerializer,
    DetailProjectSerializer,
    ListProjectImageSerializer,
    ListGalleryPostSerializer,
    DetailGalleryPostSerializer,
    ListGalleryPostImageSerializer,
    TagsSerializer,
    GenericImageSerializer,
    ListItemsSerializer,
    ListFundSerializer,
    ListDinosaurSerializer,
    ListPlanetSerializer,
    ListBookSerializer,
    ListLyricsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import CustomUser
from rest_framework.response import Response
from .pagination import CustomPagination
from ecommerce.models import Item
from funds.models import Fund
from dinosaur.models import Dinosaur
from movie.models import Movie, Game, Netflix
from planets.models import Planet
from books.models import Book
from lyrics.models import Lyrics
from blog.caching import (
    KEY_DETAIL_PREFIX,
    get_optimized_projects_queryset,
    warm_project_detail_cache,
    KEY_PREFIX,
    warm_projects_list_cache
)
from blog.gallery_caching import (
    GALLERY_PAGE_PREFIX,
    GALLERY_DETAIL_PREFIX,
    get_optimized_gallery_queryset,
    warm_gallery_list_cache,
    warm_gallery_detail_cache,
)
from blog.models import (
    Blog,
    BlogPost,
    PostImage,
    BlogImage,
    Project,
    ProjectImages,
    Tags,
    GalleryPostImages,
    GalleryPost,
    GenericImage,
)


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


@method_decorator(cache_page(60 * 15), name='dispatch')
class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["username", "email"]
    ordering_fields = ["username", "email"]
    search_fields = ["username", "email"]


@method_decorator(cache_page(60 * 15), name='dispatch')
class ListMovieApiView(ListAPIView):
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["Movie_Name", "Year", "Genre"]
    ordering_fields = ["Votes", "Movie_Name"]
    search_fields = [
        "Movie_Name",
    ]


class DetailMovieApiView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListMovieSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListMovieSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ListGameApiView(ListAPIView):
    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "developer", "console"]
    ordering_fields = ["title", "developer"]
    search_fields = ["title", "developer", "console"]


class DetailGameApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListGameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Game.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListGameSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListGameSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


# Netflix API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListNetflixApiView(ListAPIView):
    serializer_class = ListNetflixSerializer
    queryset = Netflix.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "director", "type"]
    ordering_fields = ["release_year", "title"]
    search_fields = ["title", "director", "type"]


# Ecommerce API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListItemApiView(ListAPIView):
    serializer_class = ListItemsSerializer
    queryset = Item.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "brand"]
    ordering_fields = ["price"]
    search_fields = ["title", "brand"]

    def get_queryset(self):
        queryset = Item.objects.all()
        return queryset


# Funds API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListFundApiView(ListAPIView):
    serializer_class = ListFundSerializer
    queryset = Fund.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["scheme_name", "scheme_type"]
    ordering_fields = ["net_asset_value", "scheme_name"]
    search_fields = ["scheme_name", "scheme_type"]


# Dinosaur API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListDinosaurApiView(ListAPIView):
    serializer_class = ListDinosaurSerializer
    queryset = Dinosaur.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["name", "diet"]
    ordering_fields = ["length", "name"]
    search_fields = [
        "name",
        "diet",
        "period",
        "lived_in",
        "type",
        "taxonomy",
        "named_by",
        "species",
        "link",
    ]


# Planets API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListPlanetApiView(ListAPIView):
    serializer_class = ListPlanetSerializer
    queryset = Planet.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["planet_name", "planet_host", "discovery_method"]
    ordering_fields = ["discovery_year", "planet_name"]
    search_fields = [
        "planet_name",
        "planet_host",
        "discovery_method",
        "spectral_type",
        "stellar_metallicity_ratio",
    ]


class PlanetDetailApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListPlanetSerializer
    queryset = Planet.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ListPlanetSerializer(instance)
        return Response(serializer.data)


# Books API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListBookApiView(ListAPIView):
    serializer_class = ListBookSerializer
    queryset = Book.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "authors", "category"]
    ordering_fields = ["publish_date_year", "title"]
    search_fields = ["title", "authors", "publisher", "category"]


class BookDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListBookSerializer
    queryset = Book.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ListBookSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBookSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


# Lyrics API
@method_decorator(cache_page(60 * 15), name='dispatch')
class ListLyricsApiView(ListAPIView):
    serializer_class = ListLyricsSerializer
    queryset = Lyrics.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "singer", "composer"]
    ordering_fields = ["year", "title"]
    search_fields = ["title", "singer", "composer", "lyrics"]


@method_decorator(cache_page(60 * 15), name='dispatch')
class ListBlogApiView(ListAPIView):
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "author"]
    ordering_fields = ["date_posted", "title"]
    search_fields = ["title", "author"]


class CreateBlogApiView(CreateAPIView):
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on create
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DetailBlogApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ListBlogSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBlogSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on update
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        cache.clear()  # Invalidate cache on delete
        return Response(status=204)


class CreateBlogPostApiView(CreateAPIView):
    serializer_class = ListBlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListBlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on create
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ListBlogPostApiView(ListAPIView):
    serializer_class = ListBlogPostSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = {
        "title": ["exact", "icontains"],
        "author": ["exact"],
        "author__username": ["exact", "iexact"],
        "is_published": ["exact"],
    }
    ordering_fields = ["date_posted", "title", "views"]
    search_fields = ["title", "description", "content", "author__username"]

    def get_queryset(self):
        return (
            BlogPost.objects.all()
            .select_related("author")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=PostImage.objects.order_by("order", "id"),
                ),
            )
            .order_by("-date_posted", "-id")
        )


class DetailBlogPostApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListBlogPostSerializer
    queryset = BlogPost.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBlogPostSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBlogPostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on update
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        cache.clear()  # Invalidate cache on delete
        return Response(status=204)


class CreatePostImageApiView(CreateAPIView):
    serializer_class = ListPostImageSerializer
    queryset = PostImage.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListPostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on image creation
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CreateBlogImageApiView(CreateAPIView):
    serializer_class = ListBlogImageSerializer
    queryset = BlogImage.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = ListBlogImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListProjectApiView(ListAPIView):
    serializer_class = ListProjectSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "author"]
    ordering_fields = ["date_posted", "title"]
    search_fields = ["title", "author"]

    def get_queryset(self):
        return (
            Project.objects.all()
            .select_related("author")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=ProjectImages.objects.order_by("id"),
                ),
            )
            .order_by("-id")
        )

    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        non_page_params = [k for k in query_params.keys() if k != "page"]
        is_default_request = len(non_page_params) == 0

        if is_default_request:
            page_number = query_params.get("page", "1")
            cache_key = f"{KEY_PREFIX}{page_number}"
            cached_payload = cache.get(cache_key)

            # 1. Instant Cache Hit (< 5ms)
            if cached_payload is not None:
                return Response(cached_payload)

            warm_projects_list_cache()
            cached_payload = cache.get(cache_key)
            if cached_payload is not None:
                return Response(cached_payload)

        return super().list(request, *args, **kwargs)


class CreateProjectApiView(CreateAPIView):
    serializer_class = ListProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on create
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProjectDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DetailProjectSerializer

    def get_queryset(self):
        # Uses single-trip joined queries for author, tags, and ordered images
        return get_optimized_projects_queryset()

    def retrieve(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk") or self.kwargs.get("id")
        cache_key = f"{KEY_DETAIL_PREFIX}{project_id}"

        # Increment view count atomically without taking an exclusive full-row lock
        Project.objects.filter(pk=project_id).update(views=F("views") + 1)

        # 1. Instant Cache Hit (< 5ms)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # 2. Cold-start fallback: warm cache and return
        cached_data = warm_project_detail_cache(project_id)
        if cached_data is not None:
            return Response(cached_data)

        # 3. Standard 404 handler if the record doesn't exist
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Cache invalidation & re-warming is automatically handled by the post_save signal
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Cache invalidation & re-warming is automatically handled by the post_delete signal
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddProjectImageApiView(CreateAPIView):
    serializer_class = ListProjectImageSerializer
    queryset = ProjectImages.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListProjectImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on image addition
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListCreateTagsApiView(ListCreateAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TagDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TagsSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TagsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


class ListGalleryPostApiView(ListAPIView):
    serializer_class = ListGalleryPostSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = {
        "title": ["exact", "icontains"],
        "author": ["exact"],
        "author__username": ["exact", "iexact"],
        "is_published": ["exact"],
    }
    ordering_fields = ["date_posted", "title", "views"]
    search_fields = ["title", "description", "author__username"]

    def get_queryset(self):
        return get_optimized_gallery_queryset()

    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        # Standard navigation requests (e.g. no query params or only ?page=X)
        non_page_params = [k for k in query_params.keys() if k != "page"]
        is_default_request = len(non_page_params) == 0 and not (
            request.user.is_authenticated and request.user.is_staff
        )

        if is_default_request:
            page_num = query_params.get("page", "1")
            cache_key = f"{GALLERY_PAGE_PREFIX}{page_num}"
            cached_data = cache.get(cache_key)

            if cached_data is not None:
                return Response(cached_data)

            warm_gallery_list_cache()
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)
            
        return super().list(request, *args, **kwargs)


class CreateGalleryPostApiView(CreateAPIView):
    serializer_class = ListGalleryPostSerializer
    queryset = GalleryPost.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListGalleryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on create
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GalleryPostDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DetailGalleryPostSerializer

    def get_queryset(self):
        return (
            GalleryPost.objects.all()
            .select_related("author")
            .prefetch_related(
                "tags",
                Prefetch(
                    "images",
                    queryset=GalleryPostImages.objects.order_by("order", "id"),
                ),
            )
        )

    def retrieve(self, request, *args, **kwargs):
        post_id = self.kwargs.get("pk") or self.kwargs.get("id")
        cache_key = f"{GALLERY_DETAIL_PREFIX}{post_id}"

        # Atomic counter increment without full row lock
        GalleryPost.objects.filter(pk=post_id).update(views=F("views") + 1)

        # 1. Instant Cache Hit (< 5ms)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        cached_data = warm_gallery_detail_cache(post_id)
        if cached_data is not None:
            return Response(cached_data)

        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Cache invalidation & re-warming is automatically handled by post_save signal
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Cache invalidation & re-warming is automatically handled by post_delete signal
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddGalleryPostImageApiView(CreateAPIView):
    serializer_class = ListGalleryPostImageSerializer
    queryset = GalleryPostImages.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListGalleryPostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()  # Invalidate cache on image addition
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@method_decorator(cache_page(60 * 15), name='dispatch')
class GenericImageListApiView(ListAPIView):
    serializer_class = GenericImageSerializer
    queryset = GenericImage.objects.all()
    permission_classes = [IsAuthenticated]