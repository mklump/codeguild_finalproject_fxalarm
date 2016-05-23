# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finalproject_fxalarm/views.py
by Matthew James K on 5/16/2016

Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from . import logic

def render_home(request):
    """
    This function renders the home page route to fxalarm_usd_index.html.
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/fxalarm_usd_index.html',
        context_instance = RequestContext(request, {
            'title_startscreen':'US Dollar (USD) Stream Warning',
        })
    )

def render_eventlogviewer(request):
    """
    This function renders the event viewer and log page route to fxalarm_event_log.html
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        context_instance = RequestContext(request, {
            'title_eventlog':'USD Live Streaming Data',
        })
    )