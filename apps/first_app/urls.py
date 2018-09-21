from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^pokes$', views.success),
    url(r'^login$', views.login),
    url(r'^poke/(?P<id>\d+)$', views.poke),
]