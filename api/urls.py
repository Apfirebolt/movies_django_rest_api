from django.urls import path
from . views import ListMovieApiView, DetailMovieApiView

urlpatterns = [
    path('movies', ListMovieApiView.as_view(), name='list-create-movies'),
    path('movies/<int:pk>', DetailMovieApiView.as_view(), name='detail-movies'),
]