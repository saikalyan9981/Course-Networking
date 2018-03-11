from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tcourse import views as tc_views
from mysite import settings
from django.views.static import serve

from . import views

app_name = 'eventcalendar'

urlpatterns=[

url(r'^$', views.home, name='eventcalendar'),
url(r'^(?P<pYear>\d{4})/(?P<pMonth>\d{1,2})$', views.calendar, name='evecalendar'),



]