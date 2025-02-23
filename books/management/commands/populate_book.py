from django.core.management.base import BaseCommand
import pandas as pd
from books.models import Book
import os


class Command(BaseCommand):
    help = "Populates Book Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/books.csv")
        not_saved = []
        for index, row in df.iloc[1501:15000].iterrows():
            try:
                current_book = Book(
                    title=row.get("Title"),
                    authors=row.get("Authors"),
                    category=row.get("Category"),
                    description=row.get("Description"),
                    price_starting_with=row.get("Price Starting With ($)"),
                    publisher=row.get("Publisher"),
                    publish_date_month=row.get("Publish Date (Month)"),
                    publish_date_year=row.get("Publish Date (Year)"),    
                )
                current_book.save()
                print("Data saved for ", row["Title"])
            except Exception as err:
                not_saved.append(row["Title"])
                print("Could not save data for this book ", err, row["Title"])
