from django.conf.urls import url
from .views import (
    signin, signout, signup
)


urlpatterns = [
    url(r'^signin/$', signin, name='signin-user'),
    url(r'^signout/$', signout, name='signout-user'),
    url(r'^signup/$', signup, name='signup-user'),
]
