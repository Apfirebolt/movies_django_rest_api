from django.urls import path
from . views import ListMovieApiView, DetailMovieApiView, ListGameApiView, DetailGameApiView

urlpatterns = [
    path('movies', ListMovieApiView.as_view(), name='list-create-movies'),
    path('movies/<int:pk>', DetailMovieApiView.as_view(), name='detail-movies'),
    path('games', ListGameApiView.as_view(), name='list-create-games'),
    path('games/<int:pk>', DetailGameApiView.as_view(), name='detail-games')
]