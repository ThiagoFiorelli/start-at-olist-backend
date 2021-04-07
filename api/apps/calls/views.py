from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.shortcuts import get_list_or_404
from datetime import datetime, date, time, timedelta
from dateutil import parser
from decimal import Decimal

from .serializers import CallRecordSerializer, BillSerializer
from .models import CallRecord, Bill


CALL_STANDING_CHARGE = 0.36
CALL_MINUTE_CHARGE = 0.09


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all().order_by("id")
    serializer_class = CallRecordSerializer

    def create(self, request, *args, **kwargs):
        request.data.pop("duration", None)
        request.data.pop("price", None)
        request.data.pop("is_completed", None)

        if request.data.get("end_date"):
            request.data["is_completed"] = True
            start_date = parser.parse(request.data.get("start_date"))
            end_date = parser.parse(request.data.get("end_date"))
            if end_date <= start_date:
                return Response(
                    "Invalid request. end_date must be greater than start_date.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            duration = end_date - start_date
            request.data["duration"] = duration
            request.data["price"] = self.get_call_record_price(
                start_date, end_date, duration
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        request.data.pop("duration", None)
        request.data.pop("price", None)
        request.data.pop("is_completed", None)
        lookup_field = pk
        call_record = self.get_object()

        if call_record.is_completed:
            return Response(
                data="Cannot update completed calls.",
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        if request.data.get("end_date"):
            request.data["is_completed"] = True
            start_date = call_record.start_date
            end_date = parser.parse(request.data.get("end_date"))
            if end_date <= start_date:
                return Response(
                    "Invalid request. end_date must be greater than start_date.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            duration = end_date - start_date
            request.data["duration"] = duration
            request.data["price"] = self.get_call_record_price(
                start_date, end_date, duration
            )

        serializer = self.get_serializer(
            instance=call_record, data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

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


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all().order_by("id")
    serializer_class = BillSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        source = data.get("source")
        period = data.get("period")
        total_price = Decimal(00.00)
        current_month = date.today().replace(day=1)

        if not source:
            return Response(
                "Invalid request. Missing source parameter.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if period:
            period = datetime.strptime(period, "%m/%Y")
            if period.date() >= current_month:
                return Response(
                    "Invalid request. The period must be less than the current date.",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            last_month = current_month - timedelta(days=1)
            period = datetime.combine(
                last_month.replace(
                    day=1), datetime.min.time())

        bill = Bill.objects.filter(source=source, period=period)
        if not bill:
            calls = CallRecord.objects.filter(
                source=source,
                end_date__year=period.year,
                end_date__month=period.month,
                is_completed=True
            )

            list_call = get_list_or_404(calls)
            bill = Bill.objects.create(source=source, period=period)

            for call in list_call:
                total_price += call.price
                bill.call_records.add(call)

            bill.total_price = total_price
            bill.save()
        else:
            bill = bill[0]

        serializer = BillSerializer(bill)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
