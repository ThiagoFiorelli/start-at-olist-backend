from rest_framework import serializers
from .models import CallRecord


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = '__all__'


# class CallStartRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CallStartRecord
#         fields = '__all__'


# class CallEndRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CallEndRecord
#         fields = '__all__'
