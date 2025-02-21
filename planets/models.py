from django.db import models


# Create your models here.
class Planet(models.Model):
    planet_name = models.CharField(max_length=100)  # '11 Com b' -> CharField
    planet_host = models.CharField(max_length=100)  # '11 Com' -> CharField
    num_stars = models.IntegerField(null=True, blank=True)  # 2 -> IntegerField
    num_planets = models.IntegerField(null=True, blank=True)  # 1 -> IntegerField
    discovery_method = models.CharField(
        max_length=100, null=True, blank=True
    )  # 'Radial Velocity' -> CharField
    discovery_year = models.IntegerField(null=True, blank=True)  # 2007 -> IntegerField
    discovery_facility = models.CharField(
        max_length=100, null=True, blank=True
    )  # 'Xinglong Station' -> CharField
    orbital_period_days = models.FloatField(
        null=True, blank=True
    )  # 326.03 -> FloatField
    orbit_semi_major_axis = models.FloatField(
        null=True, blank=True
    )  # 1.29 -> FloatField
    mass = models.FloatField(null=True, blank=True)  # 6165.6 -> FloatField
    eccentricity = models.FloatField(null=True, blank=True)  # 0.231 -> FloatField
    insolation_flux = models.FloatField(
        null=True, blank=True
    )  # nan -> FloatField (nullable)
    equilibrium_temperature = models.FloatField(
        null=True, blank=True
    )  # nan -> FloatField (nullable)
    spectral_type = models.CharField(
        max_length=50, null=True, blank=True
    )  # 'G8 III' -> CharField
    stellar_effective_temperature = models.FloatField(
        null=True, blank=True
    )  # 4742.0 -> FloatField
    stellar_radius = models.FloatField(null=True, blank=True)  # 19.0 -> FloatField
    stellar_mass = models.FloatField(null=True, blank=True)  # 2.7 -> FloatField
    stellar_metallicity = models.FloatField(
        null=True, blank=True
    )  # -0.35 -> FloatField
    stellar_metallicity_ratio = models.CharField(
        max_length=50, null=True, blank=True
    )  # '[Fe/H]' -> CharField
    stellar_surface_gravity = models.FloatField(
        null=True, blank=True
    )  # 2.31 -> FloatField
    distance = models.FloatField(null=True, blank=True)  # 93.1846 -> FloatField
    gaia_magnitude = models.FloatField(null=True, blank=True)  # 4.44038 -> FloatField

    def __str__(self):
        return self.planet_name
