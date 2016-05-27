# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/urls.py
by Matthew James K on 5/16/2016

Definition of urls for finalproject_fxalarm.
"""

from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
admin.autodiscover()
import django.contrib.auth.views

from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.render_home, name = 'home'),
    url(r'^event$|^viewer$|^log$', views.render_static_eventlogviewer, name = 'static_viewer'),
    #url(r'^event$|^viewer$|^log$', views.render_dynamic_eventlogviewer, name = 'dynamic_viewer'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
