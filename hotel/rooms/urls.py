from django.conf.urls import url
from .views import (
    home, FindAvailability
)


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^find-availability/', FindAvailability.as_view(), name='availability')
]
