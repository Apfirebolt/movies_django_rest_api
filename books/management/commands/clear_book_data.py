from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = "Clears Book Database"

    def handle(self, *args, **kwargs):
        # Iterate over all the planets and delete them

        for book in Book.objects.all():
            book.delete()
            print("Data deleted for ", book.title)
    
        print("All data deleted from the Book Database")
        
