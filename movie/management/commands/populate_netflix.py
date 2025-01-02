from django.core.management.base import BaseCommand
import pandas as pd
from movie.models import Netflix


class Command(BaseCommand):
    help = "Populates Netflix Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/netflix_titles.csv")

        for index, row in df.iloc[7001:].iterrows():
            try:
                current_title = Netflix(
                    show_id=row.get("show_id"),
                    type=row.get("type"),
                    title=row.get("title"),
                    director=row.get("director"),
                    cast=row.get("cast"),
                    country=row.get("country"),
                    date_added=pd.to_datetime(row.get("date_added"), errors='coerce'),
                    release_year=row.get("release_year"),
                    rating=row.get("rating"),
                    duration=row.get("duration"),
                    listed_in=row.get("listed_in"),
                    description=row.get("description")
                )
                current_title.save()
                print("Data saved for ", row["title"])
            except Exception as err:
                print("Could not save data for this game ", err)
