# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/logic.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016
"""
import os
from time import sleep
import threading
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
    global stop_execution
    return stop_execution

def set_stop_execution(value):
    """
    This setter function assigns the boolean global variable stop_execution.
    :param 1: value as boolean literal to assign to global variable stop_execution.
    """
    global stop_execution
    stop_execution = value

def get_usd_summary():
    """
    This database function retrieves each USD instance row, and provides back the timestamp
    summary of each USD capture.
    :returns: a list/array [] of strings as the summary representation of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects.all():
        time_field = repr(row).rsplit(' timestamp=')[1]
        currency_collection.append('USD Capture: at %s' % time_field)
    return currency_collection

def get_usd_detail():
    """
    This database function retrieves each use instance row, and provides back the full details of
    each USD capture.
    :returns: a list/array [] of strings as the full details of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects.all():
        currency_collection.append(repr(row).rsplit(' timestamp=')[0])
    return currency_collection

def save_static_usd_data():
    """
    This database function clears the last saved static currency data, and consecutively saves the
    USD session data from the three static sample html file sources.
    """
    if reset_currency_database() == False:
        raise RuntimeError('The currency database table(s) was not properly cleared/reset before' +
                           'next run.')
    static_files = [
        find_filename_startlookingpath(
            'primary_data_index_QC-22-1.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-2.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-3.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-4.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-5.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-6.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-7.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'primary_data_index_QC-22-8.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'backup_data_heatmap_GROUP-AD.html',
            'finalproject_fxalarm'),
        find_filename_startlookingpath(
            'backup_data_heatmap_GROUP-ALL.html',
            'finalproject_fxalarm'),
    ]
    for file in static_files:
        parse_fxalarm.save_parsed_fxdata_to_usdtable(file)

def find_filename_startlookingpath(filename, startlookingpath):
    """
    This function searches a directory tree for a single resulting filename, and from a specific
    startlookingpath directory name to start searching for this file.
    :param 1: a string filename as the specific file single result of which to find
    :param 2: a string startlookingpath as the directory starting location to begin searching
    :returns: a string as the absolute path of where the specified file exists
    """
    for root, dirs, files in os.walk(startlookingpath):
        if filename in files:
            return os.path.join(root, filename)

def reset_currency_database():
    """
    This database function resets all the 'old content' data that was already used during the last
    execution of this application.
    :returns: True if reseting all currency database tables succeeded, otherwise it returns False
    :Note: The calling function of this method should raise an exception if this fails!
    """

    if models.USD.objects.count() > 0:
        models.USD.objects.all().delete()
    retval_clear_status = True if models.USD.objects.count() == 0 else False
    return retval_clear_status

def usd_datagathering_thread():
    """
    This function delegate for the main thread start is responsible for starting off the US Dollar
    data gathering lines of code that was previously running in the view function for rendering
    the dynamic data viewing web page.
    If this program required a main() top-most level function to start the entire program - this
    function delegate used in a thread would be it!
    The if code block sets up the session for gathering, and the while code block does the actual
    gathering.
    The while loop stops running after the stop_execution boolean global variable is changed from
    the corresponding button being pressed on the fxalarm_event_log.html web page.
    """
    main_execution = None
    backup_execution = None
    parse_fxalarm.startup_htmlunitjs_webdriver()
    last_response = parse_fxalarm.check_http_response(parse_fxalarm.get_target_website())
    if not get_stop_execution():
        username_as_email = models.MyCredentials.objects.all().values(
            'username_as_email')[0]['username_as_email']
        password = models.MyCredentials.objects.all().values('password')[0]['password']
        parse_fxalarm.erase_saved_cookielogfile()
        last_response = parse_fxalarm.open_fxalarm_session(
            username_as_email, password, last_response
            )
        last_response = parse_fxalarm.request_memberarea_navigation(last_response)
        get_the_link_response = parse_fxalarm.request_heatmap_navigation(last_response)
        main_response = parse_fxalarm.request_mainsource_link(get_the_link_response)
        main_response = parse_fxalarm.get_mainsource_components(main_response)
        main_response = parse_fxalarm.create_mainsource_session(
            main_response[0], main_response[1], main_response[2], main_response[3])
        backup_response = parse_fxalarm.request_backupsource_link(get_the_link_response)

    while not get_stop_execution():
        last_response = parse_fxalarm.request_mainsource_data(main_response)
        last_response = parse_fxalarm.request_backupsource_asian_sess_data(backup_response)
        last_response = parse_fxalarm.request_backupsource_eurous_sess_data(backup_response)
    # end of while not get_stop_execution():

def start_usd_datagathering_thread():
    """
    This function is responsible for starting the fxalarm main() delegate data gathering thread.
    """
    thread = threading.Thread(target=usd_datagathering_thread)
    thread.start()
    sleep(1)
    print('The main() function delegate usd_datagathering_thread() is running.')
    #print_usd_gathered_data()

def print_usd_gathered_data():
    """
    This function prints to standard out the actual data gathered from the target website.
    """
    print('The following lines presented are the USD Summary lines:')
    print(get_usd_summary())
    print('The following lines presented are the USD Detail lines:')
    print(get_usd_detail())

if __name__ == "__main__":
    sys.exit(int(start_usd_datagathering_thread() or 0))