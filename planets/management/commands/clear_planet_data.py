from django.core.management.base import BaseCommand
from planets.models import Planet


class Command(BaseCommand):
    help = "Clears Planet Database and populates it from csv file"

    def handle(self, *args, **kwargs):
        # Iterate over all the planets and delete them

        for planet in Planet.objects.all():
            planet.delete()
            print("Data deleted for ", planet.planet_name)
    
        print("All data deleted from the Planet Database")
        
