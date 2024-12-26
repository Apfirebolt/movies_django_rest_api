"""
Tests for the Answer API.
"""

from django.test import TestCase
from django.urls import reverse
from api.serializers import ListMovieSerializer
from rest_framework.test import APIClient
from rest_framework import status
from movie.models import Movie


def movies_url():
    """Return movies URL"""
    return reverse("api:list-create-movies")


def detail_url(movie_id):
    """Return Movie detail URL"""
    return reverse("api:detail-movies", args=[movie_id])


class PublicMovieApiTests(TestCase):
    """Test the publicly available Movie API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_movies(self):
        """Test retrieving movies"""
        Movie.objects.create(
            ID=1000,
            Movie_Name="The Shawshank Redemption",
            Year=1994,
            Timing="120 mins",
            Rating=9.3,
            Votes="2345",
            Genre="Drama",
            Language="English",
        )
        Movie.objects.create(
            ID=200,
            Movie_Name="The Godfather",
            Year=1972,
            Timing="132 mins",
            Rating=9.2,
            Votes="123",
            Genre="Crime",
            Language="English",
        )

        res = self.client.get(movies_url())

        movies = Movie.objects.all().order_by("ID")
        serializer = ListMovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_movie_successful(self):
        """Test creating a new movie"""
        payload = {
            "ID": 1,
            "Movie_Name": "The Shawshank Redemption",
            "Year": 1994,
            "Timing": 142,
            "Rating": 9.3,
            "Votes": 2345,
            "Genre": "Drama",
            "Language": "English",
        }
        self.client.post(movies_url(), payload)

        exists = Movie.objects.filter(Movie_Name=payload["Movie_Name"]).exists()
        self.assertTrue(exists)


    def test_delete_movie(self):
        """Test deleting a movie"""
        movie = Movie.objects.create(
            ID=1,
            Movie_Name="The Shawshank Redemption",
            Year=1994,
            Timing="142 mins",
            Rating=9.3,
            Votes=2345,
            Genre="Drama",
            Language="English",
        )

        res = self.client.delete(detail_url(movie.ID))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    
    def test_update_movie(self):
        """Test updating a movie"""
        movie = Movie.objects.create(
            ID=1,
            Movie_Name="The Shawshank Redemption",
            Year=1994,
            Timing="142 mins",
            Rating=9.3,
            Votes=2345,
            Genre="Drama",
            Language="English",
        )

        payload = {
            "ID": 1,
            "Movie_Name": "The Shawshank",
            "Year": 1994,
            "Timing": 142,
            "Rating": 9.3,
            "Votes": 2345,
            "Genre": "Drama",
            "Language": "English",
        }

        res = self.client.put(detail_url(movie.ID), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()
        self.assertEqual(movie.Movie_Name, payload["Movie_Name"])
        self.assertEqual(movie.Year, payload["Year"])

    def test_invalid_movie(self):
        """Test creating a movie with invalid payload"""
        payload = {
            "ID": 1,
            "Movie_Name": "ABC",
            "Year": 1994,
            "Timing": 142,
            "Rating": 9.3,
            "Votes": 2345,
            "Genre": "Drama",
            "Language": "English",
        }
        res = self.client.post(movies_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print(res.data)

    
    def test_invalid_movie_year(self):
        """Test creating a movie with invalid year"""
        payload = {
            "ID": 1,
            "Movie_Name": "The Shawshank Redemption",
            "Year": 1800,
            "Timing": 142,
            "Rating": 9.3,
            "Votes": 2345,
            "Genre": "Drama",
            "Language": "English",
        }
        res = self.client.post(movies_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print(res.data)
        