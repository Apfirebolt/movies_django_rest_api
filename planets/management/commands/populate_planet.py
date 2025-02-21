from django.core.management.base import BaseCommand
import pandas as pd
from planets.models import Planet
import os


class Command(BaseCommand):
    help = "Populates Planet Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/planets.csv")
        not_saved = []
        for index, row in df.iterrows():
            try:
                current_planet = Planet(
                    planet_name=row.get("Planet Name"),
                    planet_host=row.get("Planet Host"),
                    num_stars=row.get("Num Stars"),
                    num_planets=row.get("Num Planets"),
                    discovery_method=row.get("Discovery Method"),
                    discovery_year=row.get("Discovery Year"),
                    discovery_facility=row.get("Discovery Facility"),
                    orbital_period_days=row.get("Orbital Period Days"),
                    orbit_semi_major_axis=row.get("Orbit Semi-Major Axis"),
                    mass=row.get("Mass"),
                    eccentricity=row.get("Eccentricity"),
                    insolation_flux=row.get("Insolation Flux"),
                    equilibrium_temperature=row.get("Equilibrium Temperature"),
                    spectral_type=row.get("Spectral Type"),
                    stellar_effective_temperature=row.get("Stellar Effective Temperature"),
                    stellar_radius=row.get("Stellar Radius"),
                    stellar_mass=row.get("Stellar Mass"),
                    stellar_metallicity=row.get("Stellar Metallicity"),
                    stellar_metallicity_ratio=row.get("Stellar Metallicity Ratio"),
                    stellar_surface_gravity=row.get("Stellar Surface Gravity"),
                    distance=row.get("Distance"),
                    gaia_magnitude=row.get("Gaia Magnitude")
                )
                current_planet.save()
                print("Data saved for ", row["Planet Name"])
            except Exception as err:
                not_saved.append(row["Planet Name"])
                print("Could not save data for this planet ", err, row["Planet Name"])

        # Print the planets that were not saved in a notepad file
        os.makedirs(os.path.dirname("data/not_saved_planets.txt"), exist_ok=True)

        with open("data/not_saved_planets.txt", "w") as file:
            for planet in not_saved:
                file.write(planet + "\n")
            
        print("Data for the following planets could not be saved: ", not_saved)
