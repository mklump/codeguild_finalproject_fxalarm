# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/logic.py
by Matthew James K on 5/16/2016
"""
import os
from datetime import datetime
from dateutil.tz import tzlocal
from . import models
from . import parse_fxalarm

def get_static_usd_summary_by_timestamp():
    """
    This database function retrieves each USD instance row, and provides back the timestamp summary of each USD capture.
    :returns: a list/array [] of strings as the summary representation of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects.all():
        time_field = repr(row).rsplit(' timestamp=')[1]
        currency_collection.append('USD Capture: at %s' % time_field)
    return currency_collection

def get_static_usd_detail_at_timestamp():
    """
    This database function retrieves each use instance row, and provides back the full details of each USD capture.
    :returns: a list/array [] of strings as the full details of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects.all():
        currency_collection.append(repr(row).rsplit(' timestamp=')[0])
    return currency_collection

def save_static_usd_current_session_data():
    """
    This database function clears the last saved static currency data, and consecutively saves the USD session data
    from the three static sample html file sources.
    """
    message = None
    if False == reset_currency_database():
        message = 'The currency database table(s) was not properly cleared/reset before next run.'
    static_files = [
        find_filename_by_startlookingpath('primary_data_index_QC-22.html', 'finalproject_fxalarm'),
        find_filename_by_startlookingpath('backup_data_heatmap_GROUP-AD.html', 'finalproject_fxalarm'),
        find_filename_by_startlookingpath('backup_data_heatmap_GROUP-ALL.html', 'finalproject_fxalarm'),
    ]
    for file in static_files:
        save_from_static_instance_file(file)

def find_filename_by_startlookingpath(filename, startlookingpath):
    """
    This function searches a directory tree for a single resulting filename, and from a specific startlookingpath directory
    name to start searching for this file.
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

    if 0 < models.USD.objects.count():
        models.USD.objects.all().delete()
    if 0 == models.USD.objects.count():
        return True
    else:
        return False

def save_from_static_instance_file(inputfile):
    """
    This database function accepts a specified static html instance USD source file, calls the parse function,
    and saves the incomming USD data row at that moment as the save row occured.
    """
    try:
        usd = parse_fxalarm.get_next_usd_parse(inputfile)
        usd_instance = models.USD(
            EURUSD = float(usd[0].rstrip('%').split('=')[1]),
            GBPUSD = float(usd[1].rstrip('%').split('=')[1]),
            USDJPY = float(usd[2].rstrip('%').split('=')[1]),
            USDCAD = float(usd[3].rstrip('%').split('=')[1]),
            USDCHF = float(usd[4].rstrip('%').split('=')[1]),
            AUDUSD = float(usd[5].rstrip('%').split('=')[1]),
            NZDUSD = float(usd[6].rstrip('%').split('=')[1]),
            timestamp = datetime.now(tzlocal())
        )
        usd_instance.save()
    except Exception as error:
        print(error)
        raise RuntimeError(error)