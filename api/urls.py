from django.urls import path
from . views import ListMovieApiView

urlpatterns = [
    path('movies', ListMovieApiView.as_view(), name='list-movies'),
]