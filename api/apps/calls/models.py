from django.db import models


class CallRecord(models.Model):
    call_id = models.CharField(max_length=64, unique=True)
    source = models.CharField(max_length=16)
    destination = models.CharField(max_length=16)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()  

    def get_duration(self):
        duration = self.end_date - self.start_date
        return duration


# CALL_TYPE_CHOICES = (
#     ("end", "End"),
#     ("start", "Start"),
# )


# class CallStartRecord(models.Model):
#     call_type = models.CharField(max_length=5, choices=CALL_TYPE_CHOICES, default='start')
#     timestamp = models.DateTimeField()
#     call_id = models.CharField(max_length=64, unique=True)
#     source = models.CharField(max_length=16)
#     destination = models.CharField(max_length=16)


# class CallEndRecord(models.Model):
#     call_type = models.CharField(max_length=5, choices=CALL_TYPE_CHOICES, default='end')
#     timestamp = models.DateTimeField()
#     call_id = models.CharField(max_length=64, unique=True)
#     call_start_id = models.OneToOneField(CallStartRecord, on_delete=models.CASCADE)


# class Bill(models.Model):
#     source = models.CharField(max_length=16)
#     period = model.CharField(max_length=64)


# class BillRecord(models.Model):
#     destination = models.CharField(max_length=16)
#     start_date = models.DateTimeField()
#     start_time = models.DateTimeField()
#     duration = models.DateTimeField()
#     price = price = models.DecimalField(max_digits=9, decimal_places=2, null=False)