from django.core.management.base import BaseCommand
from movie.models import Netflix


class Command(BaseCommand):
    help = 'Clears already populated Netflix data from the database'

    def handle(self, *args, **kwargs):

        shows = Netflix.objects.all()
        
        for show in shows:
            try:
                print(f'Deleting show {show.title}')
                show.delete()
            except Exception as err:
                print('Could not delete ', err)
