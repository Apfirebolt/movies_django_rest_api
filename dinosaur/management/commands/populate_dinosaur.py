from django.core.management.base import BaseCommand
import pandas as pd
from dinosaur.models import Dinosaur


class Command(BaseCommand):
    help = "Populates Dinosaur Database from csv file"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/dinosaur.csv")

        for index, row in df.iterrows():
            try:
                current_dinosaur = Dinosaur(
                    name=row.get("name"),
                    diet=row.get("diet"),
                    period=row.get("period"),
                    lived_in=row.get("lived_in"),
                    type=row.get("type"),
                    length=row.get("length"),
                    taxonomy=row.get("taxonomy"),
                    named_by=row.get("named_by"),
                    species=row.get("species"),
                    link=row.get("link")
                )
                current_dinosaur.save()
                print("Data saved for ", row["name"])
            except Exception as err:
                print("Could not save data for this dinosaur ", err, row["name"])

