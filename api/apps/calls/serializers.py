from rest_framework import serializers
from .models import CallRecord, Bill


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    call_records = CallRecordSerializer(many=True)

    class Meta:
        model = Bill
        fields = ["source", "period", "call_records", "total_price"]
