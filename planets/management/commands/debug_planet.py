from django.core.management.base import BaseCommand
from planets.models import Planet
import os
import math


class Command(BaseCommand):
    help = "Debug Planet Database data"

    def handle(self, *args, **kwargs):
        
        all_planets = Planet.objects.all()
        for planet in all_planets:
            if planet.mass and math.isnan(planet.mass):
                planet.mass = 0
                planet.save()
                print(f"Mass for {planet.planet_name} was NaN. Changed to 0")
