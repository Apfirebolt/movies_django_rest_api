from django.core.management.base import BaseCommand
from movie.models import Game


class Command(BaseCommand):
    help = 'Clears already populated Game data from the database'

    def handle(self, *args, **kwargs):

        games = Game.objects.all()
        
        for game in games:
            try:
                print(f'Deleting game {game.title}')
                game.delete()
            except Exception as err:
                print('Could not delete ', err)
