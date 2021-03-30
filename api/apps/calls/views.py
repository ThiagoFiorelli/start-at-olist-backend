from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.shortcuts import get_list_or_404
from datetime import datetime, date, time, timedelta

from .serializers import CallRecordSerializer
from .models import CallRecord


CALL_STANDING_CHARGE = 0.36
CALL_MINUTE_CHARGE = 0.09


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all().order_by("id")
    serializer_class = CallRecordSerializer


class BillViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        source = data.get("source")
        period = data.get("period")
        bill = {
            "source": source,
            "period": period,
            "call_record": [],
            "total_price": 00.00,
        }

        if not source:
            return Response(
                "Invalid request. Missing source parameter.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if period:
            queryset = CallRecord.objects.filter(source=source).filter(
                end_date__year=period.split("/")[1],
                end_date__month=period.split("/")[0],
            )
        else:
            default_date = date.today().replace(day=1) - timedelta(days=1)
            bill["period"] = f"{default_date.month}/{default_date.year}"
            queryset = CallRecord.objects.filter(source=source).filter(
                end_date__year=default_date.year, end_date__month=default_date.month
            )

        list_call = get_list_or_404(queryset)

        for call in list_call:
            destination = call.destination
            start_date = call.start_date.date().strftime("%d/%b/%Y")
            start_time = call.start_date.time()
            duration = call.end_date - call.start_date
            price = self.get_call_record_price(call.start_date, call.end_date, duration)

            call_record = {
                "destination": destination,
                "call_start_date": start_date,
                "call_start_time": start_time,
                "duration": str(duration),
                "price": price,
            }

            bill["total_price"] += price
            bill["call_record"].append(call_record)

        return Response(data=bill, status=status.HTTP_200_OK)

    def get_call_record_price(self, call_start, call_end, duration):
        time_limit_start = time(6)
        time_limit_end = time(22)
        charge = timedelta(0, 0, 0)

        if call_end.time() >= call_start.time():
            if time_limit_start <= call_start.time() <= time_limit_end:
                if time_limit_start <= call_end.time() <= time_limit_end:
                    charge = call_end - call_start
                else:
                    charge = datetime.combine(
                        date.min, time_limit_end
                    ) - datetime.combine(date.min, call_start.time())
            else:
                if time_limit_start <= call_end.time() <= time_limit_end:
                    charge = datetime.combine(
                        date.min, call_end.time()
                    ) - datetime.combine(date.min, time_limit_start)
                else:
                    charge = datetime.combine(
                        date.min, time_limit_end
                    ) - datetime.combine(date.min, time_limit_start)
        else:
            if time_limit_start <= call_start.time() <= time_limit_end:
                charge = datetime.combine(date.min, time_limit_end) - datetime.combine(
                    date.min, call_start.time()
                )
            if time_limit_start <= call_end.time() <= time_limit_end:
                charge += datetime.combine(
                    date.min, call_end.time()
                ) - datetime.combine(date.min, time_limit_start)

        total_minute_charge = int(charge.total_seconds() / 60)

        if duration.days > 0:
            charge_per_day = datetime.combine(
                date.min, time_limit_end
            ) - datetime.combine(date.min, time_limit_start)
            total_minute_charge += (
                int(charge_per_day.total_seconds() / 60) * duration.days
            )

        total_charge = round(
            total_minute_charge * CALL_MINUTE_CHARGE + CALL_STANDING_CHARGE, 2
        )

        return total_charge
