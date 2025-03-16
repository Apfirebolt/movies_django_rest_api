from django.core.management.base import BaseCommand
import pandas as pd
from lyrics.models import Lyrics


class Command(BaseCommand):
    help = "Populates Lyrics Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/lyrics.csv")
        not_saved = []
        for index, row in df.iloc[9001:].iterrows():
            try:
                current_lyric = Lyrics(
                    title=row.get("Title"),
                    film=row.get("Film"),
                    singer=row.get("Singer"),
                    composer=row.get("Composer"),
                    lyricist=row.get("Lyricist"),
                    year=row.get("Year"),
                    lyrics=row.get("Lyrics"),
                )
                current_lyric.save()
                print("Data saved for ", row["Title"])
            except Exception as err:
                not_saved.append(row["Title"])
                print("Could not save data for this lyric ", err, row["Title"])
