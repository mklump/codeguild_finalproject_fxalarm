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
from . import models
from . import parse_fxalarm

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
    logic.save_static_usd_current_session_data()
    usd_summary = logic.get_static_usd_summary_by_timestamp()
    usd_detail = logic.get_static_usd_detail_at_timestamp()
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {
            'title_eventlog':'USD Live Streaming Data',
            'usd_summary':usd_summary,
            'usd_detail':usd_detail,
        }
    )

def render_dynamic_eventlogviewer(request):
    """
    This function renders real-time data content to the event viewer and log page route to fxalarm_event_log.html
    """
    assert isinstance(request, HttpRequest)
    username_as_email = models.MyCredentials.objects.all().values('username_as_email')[0]['username_as_email']
    password = models.MyCredentials.objects.all().values('password')[0]['password']
    current_session = parse_fxalarm.open_fxalarm_session(username_as_email, password)
    current_session = parse_fxalarm.step_through_membersarea_to_source(current_session[0], current_session[1])
    current_session = parse_fxalarm.execute_main_data_gathering_loop(current_session[0], current_session[1])
    parse_fxalarm.close_fxalarm_session(current_session[0], current_session[1])
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {
            'title_eventlog':'USD Live Streaming Data',
        }
    )

def render_peace_be_with_you(request):
    """
    This function renders a page that offers a blessing for the one person or people reading this page.
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/peace_be_with_you_farwell.html',
        {
            'title_peace_be_with_you':'Peace be wtih you, take Good Care.',
        }
    )