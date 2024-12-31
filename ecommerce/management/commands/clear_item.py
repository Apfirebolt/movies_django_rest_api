from django.core.management.base import BaseCommand
import pandas as pd
from ecommerce.models import Item


class Command(BaseCommand):
    help = 'Clears already populated Item data from the database'

    def handle(self, *args, **kwargs):

        items = Item.objects.all()
        
        for item in items:
            try:
                print(f'Deleting item {item.title}')
                item.delete()
            except Exception as err:
                print('Could not delete ', err)
        