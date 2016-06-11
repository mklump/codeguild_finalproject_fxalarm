# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finalproject_fxalarm/views.py
by Matthew James K on 5/16/2016

Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext

from . import logic
from . import models
from . import parse_fxalarm

stop_execution = True
"""
This global boolean variable in this views.py file will be evaluated each time the main data
gathering while-loop with in the view function render_dynamic_eventlogviewer() executes as
that while-loop's stop condition.
"""

def get_stop_execution():
    """
    This getter function returns the boolean global variable stop_execution.
    :returns: stop_execution as boolean global variable while-loop stop condition
    """
    return stop_execution

def set_stop_execution(value):
    """
    This setter function assigns the boolean global variable stop_execution.
    :param 1: value as boolean literal to assign to global variable stop_execution.
    """
    stop_execution = value

def render_home(request):
    """
    This view function renders the home page route to fxalarm_usd_index.html.
    """
    #assert isinstance(request, HttpRequest) For future rememberance should django ever change.
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
    main_execution = None
    backup_execution = None
    last_response = None
    if not get_stop_execution():
        username_as_email = models.MyCredentials.objects.all().values(
            'username_as_email')[0]['username_as_email']
        password = models.MyCredentials.objects.all().values('password')[0]['password']
        parse_fxalarm.erase_saved_cookielogfile()
        last_response = parse_fxalarm.open_fxalarm_session(
            username_as_email, password
            )
        last_response = parse_fxalarm.request_memberarea_navigation(last_response)
        get_the_link_response = parse_fxalarm.request_heatmap_navigation(last_response)
        main_response = parse_fxalarm.request_mainsource_link(get_the_link_response)
        backup_response = parse_fxalarm.request_backupsource_link(get_the_link_response)

    while not get_stop_execution():
        last_response = parse_fxalarm.request_mainsource_data(main_response)
        last_response = parse_fxalarm.request_backupsource_data(backup_response)
    # endof while not get_stop_execution():

    parse_fxalarm.close_fxalarm_session(last_response)
    set_stop_execution(False)

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

def render_stop_gathering(request, stop_gathering):
    """
    This view function halts the execution of the main while-loop execution of the previous view
    function render_dynamic_eventlogviewer() by changing the status of a global boolean variable
    named stop_execution that this while loop will be checking as a stop condition.
    """
    if stop_gathering == 'True':
        stop_execution = True
    render_dynamic_eventlogviewer(request)
    return HttpResponse('')

def render_peace_be_with_you(request):
    """
    This view function renders a page that offers a blessing for the one person or people reading
    this page.
    """
    return render(
        request,
        'finalproject_fxalarm/peace_be_with_you_farwell.html',
        {
            'title_peace_be_with_you':'Peace be wtih you, take Good Care.',
        }
    )
