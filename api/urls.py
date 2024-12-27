from django.urls import path
from . views import ListMovieApiView, DetailMovieApiView, ListGameApiView, DetailGameApiView, CreateCustomUserApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', CreateCustomUserApiView.as_view(), name='signup'),
    path('login', TokenObtainPairView.as_view(), name='signin'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('movies', ListMovieApiView.as_view(), name='list-create-movies'),
    path('movies/<int:pk>', DetailMovieApiView.as_view(), name='detail-movies'),
    path('games', ListGameApiView.as_view(), name='list-create-games'),
    path('games/<int:pk>', DetailGameApiView.as_view(), name='detail-games')
]