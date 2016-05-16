"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/urls.py
by Matthew James K on 5/16/2016

Definition of urls for finalproject_fxalarm.
"""

from datetime import datetime
from django.contrib import admin
from django.conf.urls import url
import django.contrib.auth.views

from app import views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', views.render_home, name = 'home'),
    url(r'^(event|viewer|log)$', views.render_eventlogviewer, name = 'viewer')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
