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

stop_execution = False
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
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/fxalarm_usd_index.html',
        context_instance=RequestContext(request, {
            'title_startscreen':'US Dollar (USD) Stream Warning',
        })
    )

def render_static_eventlogviewer(request):
    """
    This view function renders the static data content to the event viewer and log page route to
    fxalarm_event_log.html
    """
    assert isinstance(request, HttpRequest)
    logic.save_static_usd_data()
    usd_summary = logic.get_static_usd_summary()
    usd_detail = logic.get_static_usd_detail()
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
    assert isinstance(request, HttpRequest)
    main_execution = None
    backup_execution = None
    if not get_stop_execution():
        username_as_email = models.MyCredentials.objects.all().values(
            'username_as_email')[0]['username_as_email']
        password = models.MyCredentials.objects.all().values('password')[0]['password']
        current_session = parse_fxalarm.open_fxalarm_session(
            username_as_email, password
            )
        current_session = parse_fxalarm.request_memberarea_navigation(
            current_session[0], current_session[1]
            )
        current_session = parse_fxalarm.request_heatmap_navigation(
            current_session[0], current_session[1]
            )
        main_execution = parse_fxalarm.request_mainsource_link(
            current_session[0], current_session[1]
            )
        backup_execution = parse_fxalarm.request_backupsource_link(
            main_execution[0], main_execution[1]
            )

    while not get_stop_execution():
        current_session = parse_fxalarm.request_mainsource_data(
            main_execution[0], main_execution[1]
            )
        current_session = parse_fxalarm.request_backupsource_data(
            backup_execution[0], backup_execution[0]
            )
    # endof while not get_stop_execution():
    parse_fxalarm.close_fxalarm_session(current_session[0], current_session[1])
    set_stop_execution(False)

    usd_summary = logic.get_static_usd_summary()
    usd_detail = logic.get_static_usd_detail()
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
    assert isinstance(request, HttpRequest)
    if stop_gathering == 'True':
        stop_execution = True
    render_dynamic_eventlogviewer(request)
    return HttpResponse('')

def render_peace_be_with_you(request):
    """
    This view function renders a page that offers a blessing for the one person or people reading
    this page.
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'finalproject_fxalarm/peace_be_with_you_farwell.html',
        {
            'title_peace_be_with_you':'Peace be wtih you, take Good Care.',
        }
    )
