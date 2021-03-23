from django.urls import include, path
from rest_framework import routers
from .views import BillViewSet, CallRecordViewSet


router = routers.DefaultRouter()
# router.register(r'callstartrecord', CallStartRecordViewSet, basename="CallStartRecords")
# router.register(r'callendrecord', CallEndRecordViewSet, basename="CallEndRecords")
router.register(r'callrecord', CallRecordViewSet, basename="CallRecord")
router.register(r'bill', BillViewSet, basename="bill")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework'))
]