from django.core.management.base import BaseCommand
import json
from funds.models import Fund


class Command(BaseCommand):
    help = "Populates Fund Database from json file"

    def handle(self, *args, **kwargs):
    
        # Path to the JSON file
        file_path = 'data/funds.json'

        # Read the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        for row in data[10001:12000]:

            try:
                current_fund = Fund(
                    scheme_code=row.get("Scheme_Code"),
                    date=row.get("Date"),
                    isin_div_payout_isin_growth=row.get("ISIN_Div_Payout_ISIN_Growth"),
                    isin_div_reinvestment=row.get("ISIN_Div_Reinvestment"),
                    mutual_fund_family=row.get("Mutual_Fund_Family"),
                    net_asset_value=row.get("Net_Asset_Value"),
                    scheme_category=row.get("Scheme_Category"),
                    scheme_name=row.get("Scheme_Name"),
                    scheme_type=row.get("Scheme_Type")
                )
                current_fund.save()
                print("Data saved for ", row["Scheme_Name"])

            except Exception as err:
                print("Could not save data for this fund ", err)
