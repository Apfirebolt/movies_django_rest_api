from django.db import models


class Dinosaur(models.Model):
    name = models.CharField(max_length=200)
    diet = models.CharField(max_length=200)
    period = models.CharField(max_length=200)
    lived_in = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    length = models.CharField(max_length=200, null=True, blank=True)
    taxonomy = models.CharField(max_length=200, null=True, blank=True)
    named_by = models.CharField(max_length=200, null=True, blank=True)
    species = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'dinosaur'

    def __str__(self):
        return self.name
