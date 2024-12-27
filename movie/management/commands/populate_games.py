from django.core.management.base import BaseCommand
import pandas as pd
from movie.models import Game


class Command(BaseCommand):
    help = "Populates Game Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/vgchartz_games.csv")

        for index, row in df.head(1000).iterrows():
            try:
                current_game = Game(
                    img=row.get("img"),
                    title=row.get("title"),
                    console=row.get("console"),
                    genre=row.get("genre"),
                    publisher=row.get("publisher"),
                    developer=row.get("developer"),
                    critic_score=row.get("critic_score"),
                    total_sales=row.get("total_sales"),
                    na_sales=row.get("na_sales"),
                    jp_sales=row.get("jp_sales"),
                    pal_sales=row.get("pal_sales"),
                    other_sales=row.get("other_sales"),
                    release_date=row.get("release_date"),
                    last_update=row.get("last_update")
                )
                current_game.save()
                print("Data saved for ", row["title"])
            except Exception as err:
                print("Could not save data for this game ", err)
