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

def render_static_eventlogviewer(request):
    """
    This function renders the static data content to the event viewer and log page route to fxalarm_event_log.html
    """
    assert isinstance(request, HttpRequest)
    #logic.save_static_usd_current_session_data()
    #usd_summary = logic.get_static_usd_summary_by_timestamp()
    #usd_detail = logic.get_static_usd_detail_at_timestamp()
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {
            'title_eventlog':'USD Live Streaming Data',
            #'usd_summary':usd_summary,
            #'usd_detail':usd_detail,
        }
    )

def render_dynamic_eventlogviewer(request):
    """
    This function renders real-time data content to the event viewer and log page route to fxalarm_event_log.html
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {
            'title_eventlog':'USD Live Streaming Data',
        }
    )