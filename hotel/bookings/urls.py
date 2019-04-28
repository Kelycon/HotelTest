from django.conf.urls import url
from .views import (
    BookingCreate, BookingDetail, BookingList
)


urlpatterns = [
    url(r'^booking-create/(?P<pk>.+)/', BookingCreate.as_view(), name='booking-create'),
    url(r'^booking-detail/(?P<pk>.+)/', BookingDetail.as_view(), name='booking-detail'),
    url(r'^booking-list/', BookingList.as_view(), name='booking-list')
]
