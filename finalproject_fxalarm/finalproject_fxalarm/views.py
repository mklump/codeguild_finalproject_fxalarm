# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finalproject_fxalarm/views.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016

Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext

from . import logic
from . import models
from . import parse_fxalarm

def render_home(request):
    """
    This view function renders the home page route to fxalarm_usd_index.html.
    """
    #assert isinstance(request, HttpRequest) For future remembrance should django ever change.
    return render(
        request,
        'finalproject_fxalarm/fxalarm_usd_index.html',
        #This is a future reminder there are other keys here that could potentially help us.
        #The name of this key for this convenience function is context_instance:
        context_instance=RequestContext(request, {
            'title_startscreen':'US Dollar (USD) Stream Warning',
        })
    )

def render_static_eventlogviewer(request):
    """
    This view function renders the static data content to the event viewer and log page route to
    fxalarm_event_log.html
    """
    logic.save_static_usd_data()
    usd_summary = logic.get_usd_summary()
    usd_detail = logic.get_usd_detail()
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
    This view function renders real-time data content to the event viewer and log page route to
    fxalarm_event_log.html
    """
    logic.set_stop_execution(False)
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {'title_eventlog':'USD Live Streaming Data'}
    )

def render_start_gathering(request):
    """
    This view function starts the data gathering main() execution thread.
    The thread will first launch the selenium remote webdriver separate thread, and then starts
    the data gathering in this current running thread.
    """
    logic.start_usd_datagathering_thread()
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {'title_eventlog':'USD Live Streaming Data'}
    )

def render_stop_gathering(request, stop_gathering):
    """
    This view function halts the execution of the main while-loop execution of the previous view
    function render_dynamic_eventlogviewer() by changing the status of a global boolean variable
    named stop_execution that the while loop in the logic.py will be checking as a stop condition.
    """
    if stop_gathering == 'True':
        logic.set_stop_execution(True)
    usd_summary = logic.get_usd_summary()
    usd_detail = logic.get_usd_detail()
    return render(
        request,
        'finalproject_fxalarm/fxalarm_event_log.html',
        {
            'title_eventlog':'USD Live Streaming Data',
            'usd_summary':usd_summary,
            'usd_detail':usd_detail,
        }
    )

def render_peace_be_with_you(request):
    """
    This view function renders a page that offers a blessing for the one person or people reading
    this page.
    """
    return render(
        request,
        'finalproject_fxalarm/peace_be_with_you_farwell.html',
        {'title_peace_be_with_you':'Peace be with you, take Good Care.'}
    )
