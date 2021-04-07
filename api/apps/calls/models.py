from django.db import models
from datetime import timedelta


class CallRecord(models.Model):
    call_id = models.CharField(max_length=64, unique=True)
    source = models.CharField(max_length=16)
    destination = models.CharField(max_length=16)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    duration = models.DurationField(default=timedelta())
    price = models.DecimalField(max_digits=9, decimal_places=2, default=00.00)


class Bill(models.Model):
    source = models.CharField(max_length=16)
    period = models.DateTimeField()
    call_records = models.ManyToManyField(CallRecord)
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, default=00.00)
