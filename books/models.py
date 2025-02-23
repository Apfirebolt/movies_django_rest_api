from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    price_starting_with = models.DecimalField(max_digits=10, decimal_places=2)
    publish_date_month = models.CharField(max_length=50, null=True, blank=True)
    publish_date_year = models.IntegerField()

    def __str__(self):
        return self.title
