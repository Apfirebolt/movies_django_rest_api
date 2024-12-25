from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = 'Clears already populated Movie data from the database'

    def handle(self, *args, **kwargs):

        movies = Movie.objects.all()
        
        for movie in movies:
            try:
                print(f'Deleting movie {movie.Movie_Name}')
                movie.delete()
            except Exception as err:
                print('Could not delete ', err)
