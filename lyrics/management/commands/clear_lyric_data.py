from django.core.management.base import BaseCommand
from lyrics.models import Lyrics


class Command(BaseCommand):
    help = "Clears Lyrics Database"

    def handle(self, *args, **kwargs):
        # Iterate over all the lyrics and delete them

        for lyric in Lyrics.objects.all():
            lyric.delete()
            print("Data deleted for ", lyric.title)
    
        print("All data deleted from the Lyric Database")
        
