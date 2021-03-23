from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.shortcuts import get_list_or_404
from datetime import datetime, date, time, timedelta

from .serializers import CallRecordSerializer
from .models import CallRecord


CALL_STANDING_CHARGE = 0.36
CALL_MINUTE_CHARGE = 0.09


# class CallStartRecordViewSet(viewsets.ModelViewSet):
#     queryset = CallStartRecord.objects.all().order_by('id')
#     serializer_class = CallStartRecordSerializer


# class CallEndRecordViewSet(viewsets.ModelViewSet):
#     queryset = CallEndRecord.objects.all().order_by('id')
#     serializer_class = CallEndRecordSerializer


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all().order_by('id')
    serializer_class = CallRecordSerializer


class BillViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all().order_by('id')
    serializer_class = CallRecordSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        source = data.get("source")
        period = data.get("period")
        response = []
        if period:
            queryser = CallRecord.objects.filter(source=source).filter(end_date__year=period.split('/')[1], end_date__month=period.split('/')[0])
        else:
             queryser = CallRecord.objects.filter(source=source)

        list_call = get_list_or_404(queryser)

        for call in list_call:
            destination = call.destination
            start_date = call.start_date.date().strftime("%d/%b/%Y")
            start_time = call.start_date.time().strftime("%Hh%Mm%Ss")
            end_date = call.end_date.date().strftime("%d/%b/%Y")
            end_time = call.end_date.time().strftime("%Hh%Mm%Ss")
            duration = call.get_duration()
            price = self.get_call_record_price(call.start_date, call.end_date)

            print(destination, start_date, start_time, end_date, end_time, duration, price)

            response.append([destination, start_date, start_time, end_date, end_time, duration, price])


        return Response(data=response, status=status.HTTP_200_OK)

    def get_call_record_price(self, call_start, call_end):
        time_limit_start = time(6)
        time_limit_end = time(22)
        ret = "nao entrou"
        no_charge = timedelta(0, 0, 0)
        charge = timedelta(0, 0, 0)

        duration = datetime.combine(date.min, time_limit_start) - datetime.combine(date.min, time_limit_start)

        print(type(time_limit_start), type(call_start))

        if time_limit_start <= call_start.time() <= time_limit_end:
            if time_limit_start <= call_end.time() <= time_limit_end:
                charge = call_end - call_start
            else:
                charge = datetime.combine(date.min, time_limit_end) - datetime.combine(date.min, call_start.time())
                no_charge = datetime.combine(date.min, call_end.time()) - datetime.combine(date.min, time_limit_end)
        else:
            if time_limit_start <= call_end.time() <= time_limit_end:
                charge = datetime.combine(date.min, call_end.time()) - datetime.combine(date.min, time_limit_start)
            else:
                no_charge = call_end - call_start

        total_minute_charge = int(charge.total_seconds()/60)
        total_charge = round(total_minute_charge * CALL_MINUTE_CHARGE + CALL_STANDING_CHARGE, 2)

        return total_charge
