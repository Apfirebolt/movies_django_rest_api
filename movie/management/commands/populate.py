from django.core.management.base import BaseCommand
import pandas as pd
from movie.models import Movie


class Command(BaseCommand):
    help = "Populates Movie Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/movies.csv")

        item_count = 1
        for index, row in df.head(100).iterrows():
            try:
                rating = row["Rating(10)"] if row["Rating(10)"] != '-' else None
                current_movie = Movie(
                    ID = item_count,
                    Movie_Name=row["Movie Name"],
                    Year=row["Year"],
                    Timing=row["Timing(min)"],
                    Rating=rating,
                    Votes=row["Votes"],
                    Genre=row["Genre"],
                    Language=row["Language"],
                )
                current_movie.save()
                item_count += 1
                print("Data saved for ", row["Movie Name"])
            except Exception as err:
                print("Could not save data for this movie ", err)
