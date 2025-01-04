from django.db import models


# Create your models here.
class Fund(models.Model):
    scheme_code = models.IntegerField()
    date = models.CharField(max_length=20, null=True, blank=True)
    isin_div_payout_isin_growth = models.CharField(max_length=30, null=True, blank=True)
    isin_div_reinvestment = models.CharField(max_length=30, blank=True, null=True)
    mutual_fund_family = models.CharField(max_length=100, blank=True, null=True)
    net_asset_value = models.DecimalField(max_digits=10, decimal_places=3)
    scheme_category = models.CharField(max_length=100, blank=True, null=True)
    scheme_name = models.CharField(max_length=200)
    scheme_type = models.CharField(max_length=100)

    def __str__(self):
        return self.scheme_name