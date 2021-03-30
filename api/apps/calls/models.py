from django.db import models


class CallRecord(models.Model):
    call_id = models.CharField(max_length=64, unique=True)
    source = models.CharField(max_length=16)
    destination = models.CharField(max_length=16)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
