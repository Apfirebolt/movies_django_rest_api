from django.db import models

class Item(models.Model):
    product_id = models.CharField("Product Id", max_length=100, blank=True, null=True)
    title = models.CharField("Title", max_length=300, blank=True, null=True)
    link = models.CharField("Link", max_length=200, blank=True, null=True)
    price = models.IntegerField("Price", blank=True, null=True)
    mrp = models.IntegerField("MRP", blank=True, null=True)
    brand = models.CharField("Brand", max_length=200, blank=True, null=True)
    rating = models.FloatField("Rating", blank=True, null=True)
    totalRating = models.IntegerField("Total Rating", blank=True, null=True)
    discount = models.IntegerField("Discount", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        '''Doc string for meta'''
        verbose_name_plural = "Items"