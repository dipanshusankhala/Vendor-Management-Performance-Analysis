from django.db import models
from Vendor_profile.models import Vendor


class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,to_field='vendor_code')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()