# -*- coding: utf-8 -*-
"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/logic.py
by Matthew James K on 5/16/2016
"""
from . import models
from . import parse_fxalarm

def get_static_usd_summary_by_timestamp():
    """
    This database function retrieves each USD instance row, and provides back the timestamp summary of each USD capture.
    :returns: a list/array [] of strings as the summary representation of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects().all():
        currency_collection.append('USD Capture: at %s' % row.__repr__().rsplit('at')[1])
    return currency_collection

def get_static_usd_detail_at_timestamp():
    """
    This database function retrieves each use instance row, and provides back the full details of each USD capture.
    :returns: a list/array [] of strings as the full details of each USD instance row
    """
    currency_collection = []
    for row in models.USD.objects().all():
        currency_collection.append(row.__repr__().rsplit('at')[0])
    return currency_collection

def save_static_usd_current_session_data():
    """
    This database function clears the last saved static currency data, and consecutively saves the USD session data
    from the three static sample html file sources.
    """
    message = None
    if False == reset_currency_database():
        message = 'The currency database table(s) was not properly cleared/reset before next run.'
    static_files = [ 'primary_data_index_QC-22.html', 'backup_data_heatmap_GROUP-AD.html', 'backup_data_heatmap_GROUP-ALL.html' ]
    for file in static_files:
        if False == save_from_static_instance_file(file):
            message = 'The database save function failed processing file: %s. Please recheck function.' % file
            break
    if None != message:
        raise RuntimeError(message)

def reset_currency_database():
    """
    This database function resets all the 'old content' data that was already used during the last
    execution of this application.
    :returns: True if reseting all currency database tables succeeded, otherwise it returns False
    :Note: The calling function of this method should raise an exception if this fails!
    """
    models.USD.objects().all().remove()
    if 0 < len(models.USD.objects().all()):
        return False
    else:
        return True

def save_from_static_instance_file(inputfile):
    """
    This database function accepts a specified static html instance USD source file, calls the parse function,
    and saves the incomming USD data row at that moment as the save row occured.
    :returns: True is the db save operation succeeded, otherwise it returns False
    """
    try:
        usd = parse_fxalarm.get_next_usd_parse(inputfile)
        usd_instance = models.USD(
            EURUSD = float(usd[0].rstrip('%')),
            GBPUSD = float(usd[1].rstrip('%')),
            USDJPY = float(usd[2].rstrip('%')),
            USDCAD = float(usd[3].rstrip('%')),
            USDCHF = float(usd[4].rstrip('%')),
            AUDUSD = float(usd[5].rstrip('%')),
            NZDUSD = float(usd[6].rstrip('%')),
            timestamp = datetime.datetime.now()
        )
        usd_instance.save()
    except Exception:
        return False
    
    return True