# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/urls.py
by Matthew James K on 5/16/2016

Definition of urls for finalproject_fxalarm.
"""

from django.contrib import admin
from django.conf.urls import url, include
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^$', views.render_home, name='home'),
    #url(r'^$', views.render_dynamic_eventlogviewer, name = 'home'),

    url(r'^viewer$|^event_viewer$|^log$', views.render_static_eventlogviewer, name='event_viewer'),
    #url(r'^viewer$|^event_viewer$|^log$', views.render_dynamic_eventlogviewer, name='event_viewer'),
    url(r'^event_viewer/(?P<stop_gathering>.+)$', views.render_stop_gathering, name='stop_gathering'),
    url(r'^peace$', views.render_peace_be_with_you, name='peace_onto_you'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

