from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    ListMovieSerializer,
    ListGameSerializer,
    ListCustomUserSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    ListBlogSerializer,
    ListBlogPostSerializer,
    ListPostImageSerializer,
    ListBlogImageSerializer,
    ListProjectSerializer,
    ListProjectImageSerializer,
    ListGalleryPostSerializer,
    ListGalleryPostImageSerializer,
    TagsSerializer,
    GenericImageSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import CustomUser
from rest_framework.response import Response
from . pagination import CustomPagination
from movie.models import Movie, Game
from blog.models import Blog, BlogPost, PostImage, BlogImage, Project, ProjectImages, Tags, GalleryPostImages, GalleryPost, GenericImage


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    search_fields = ['username', 'email']


class ListMovieApiView(ListAPIView):
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['Movie_Name', 'Year', 'Genre']
    ordering_fields = ['Votes', 'Movie_Name']
    search_fields = ['Movie_Name',]

class DetailMovieApiView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()

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


class ListGameApiView(ListAPIView):

    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'developer', 'console']
    ordering_fields = ['title', 'developer']
    search_fields = ['title', 'developer', 'console']


class DetailGameApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = ListGameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Game.objects.all()

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


class ListBlogApiView(ListAPIView):

    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'author']
    ordering_fields = ['date_posted', 'title']
    search_fields = ['title', 'author']


class CreateBlogApiView(CreateAPIView):

    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DetailBlogApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()

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
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    

class CreateBlogPostApiView(CreateAPIView):

    serializer_class = ListBlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListBlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ListBlogPostApiView(ListAPIView):

    serializer_class = ListBlogPostSerializer
    queryset = BlogPost.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'author']
    ordering_fields = ['date_posted', 'title']
    search_fields = ['title', 'author']


class DetailBlogPostApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = ListBlogPostSerializer
    queryset = BlogPost.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBlogPostSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListBlogPostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    

class CreatePostImageApiView(CreateAPIView):

    serializer_class = ListPostImageSerializer
    queryset = PostImage.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = ListPostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ListProjectApiView(ListAPIView):

    serializer_class = ListProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'author']
    ordering_fields = ['date_posted', 'title']
    search_fields = ['title', 'author']


class CreateProjectApiView(CreateAPIView):

    serializer_class = ListProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProjectDetailApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = ListProjectSerializer
    queryset = Project.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ListProjectSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListProjectSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    

class AddProjectImageApiView(CreateAPIView):

    serializer_class = ListProjectImageSerializer
    queryset = ProjectImages.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = ListProjectImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ListCreateTagsApiView(ListCreateAPIView):

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class TagDetailApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()

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
    queryset = GalleryPost.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'author']
    ordering_fields = ['date_posted', 'title']
    search_fields = ['title', 'author']


class CreateGalleryPostApiView(CreateAPIView):

    serializer_class = ListGalleryPostSerializer
    queryset = GalleryPost.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ListGalleryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class GalleryPostDetailApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = ListGalleryPostSerializer
    queryset = GalleryPost.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ListGalleryPostSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListGalleryPostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    

class AddGalleryPostImageApiView(CreateAPIView):

    serializer_class = ListGalleryPostImageSerializer
    queryset = GalleryPostImages.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = ListGalleryPostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class GenericImageListApiView(ListAPIView):

    serializer_class = GenericImageSerializer
    queryset = GenericImage.objects.all()
    
    
    