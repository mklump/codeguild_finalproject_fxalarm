"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
from bs4 import BeautifulSoup
import re
import urllib
import threading
from django.http import HttpRequest
from django.http import HttpResponse

import requests
from requests.cookies import RequestsCookieJar
import browser_cookie3
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzlocal
from . import models
import os

gcookies = RequestsCookieJar()

def parse_html_source_file(input_file):
    """
    This critical function accepts an html input file that is the complete http GET response after
    correctly logging in.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed for data.
    :returns: an object as BeautifulSoup that is the class wrapper around the html python module for html parsing.
    """
    soup_html_xml_parser = None
    try:
        with open(input_file, 'rt') as html:
            soup_html_xml_parser = BeautifulSoup(html, 'html.parser')
        # end with block/close file
    except Exception as error:
        print(error)
        raise
    return soup_html_xml_parser

def parse_currency_node(html_parser, currency_symbol):
    """
    This critical function accepts an object of type BeautifulSoup as the html parser, and also a specific currency
    symbol, and returns the matched session acceleration value for the current html snapshot GET request or file.
    :param 1: html_parser as an object of type BeautifulSoup as the html parser
    :param 2: currency_symbol as a specific currency symbol to retrieve
    :returns: a string representation of the matched session acceleration value for the current html snapshot GET request or file
    """
    match = html_parser.find(string = currency_symbol)
    return '{0}={1}'.format(match, match.next_element.next_element.string)


def get_next_usd_parse(input_file):
    """
    This critical function accepts an input file to perform the extraction of the US Dollar session acceleration
    data snap shot at this moment in time, and returns this instance of the data stream.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed for data.
    :returns: a list/array [] representation of the USD instance of the data stream
    """
    usd_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD', 'USDCHF', 'AUDUSD', 'NZDUSD']
    html_parser = parse_html_source_file(input_file)
    return [ '%s' % parse_currency_node(html_parser, symbol) for symbol in usd_symbols ]
    
def set_fxalarm_db_login(username, pwd, website):
    """
    This function can only be run currenlt from a python interactive console.
    This function accepts 3 parameters, to save to the MyCredentials database table for access by
    this program - username_as_email, password, and target_website.
    :param 1: username as string to save to username_as_email
    :param 2: pwd as string to save to password
    :param 3: website as string to save to target_website
    """
    try:
        my_credentials = models.MyCredentials(
            username_as_email = username,
            password = pwd,
            target_website = website,
            )
        my_credentials.save()
    except Exception as error:
        print(error)
        raise

def open_fxalarm_session(): # refactor to accept 2 arguments username_as_email, password
    """
    This function reads the MyCredentials table for the existance of 1 row, and starts a new active session.
    :returns: True if the login succeeded, otherwise it will return False
    """
    try:
        form_post_params = {
            'vchEmail': models.MyCredentials.objects.all().values('username_as_email')[0]['username_as_email'],
            'vchPassword': models.MyCredentials.objects.all().values('password')[0]['password'],
        }
        target_site = get_target_website()
        gcookies = get_target_website_cookies()
        if 'PHPSESSID' not in gcookies._cookies:
            gcookies.set({ 'PHPSESSID':'2e40549eeb46e0603b341232a5c02fa0' })
        login_response = requests.post('%slogin' % target_site, data = form_post_params, cookies = gcookies)
        for cookie in login_response.cookies:
            gcookies.set_cookie(cookie)
        if '9951' != login_response.cookies['UserID']:
            raise RuntimeError('The login operation failed in the function open_fxalarm_session().')
        close_fxalarm_session()
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def get_and_keep_alive_realtime_data(): # refactor: split each to 3 parts request setup, execute request, verify the request
    """
    This function checks regularly that the current active session is still active,
    and calls parse function saving the realtime data.
    """
    try:
        target_site = models.MyCredentials.objects.all().values('target_website')[0]['target_website']
        cookies_needed = dict(requests.cookies['PHPSESSID'], requests.cookies['UserID'])
        active_session = requests.get('%smember-area.php' % target_site, cookies = cookies_needed)
        active_session = requests.get('%sheatmap.php' % target_site, cookies = cookies_needed)
        # main while gathering loop
        while '9951' == requests.cookies['UserID'] and 'deleted' != requests.cookies['UserID']: # TODO: Add additional stop condition!
            threading.current_thread().join(timeout = 15) # Wait here 15 seconds before proceeding.
            active_session = requests.get('%sget_v4.php' % target_site, cookies = cookies_needed)
            soup_html_parser = BeautifulSoup(active_session.text, 'html.parser')
            primary_source = soup_html_parser.find(string = 'acForm').next_sibling.string
            cookies_needed = dict(requests.cookies['PHPSESSID'])
            primary_data = requests.get(primary_source, cookies = cookies_needed)
            save_from_static_instance_file(primary_data) # primary data source .save()
            form_post_params = { 'chk' : 2 }
            cookies_needed = dict(requests.cookies['PHPSESSID'], requests.cookies['UserID'])
            escaped = requests.get('%sget.php' % target_site, data = form_post_params, cookies = cookies_needed)
            escaped_string = re.match('.+unescape\(\"(.+)\"\)\);', escaped)
            unescaped_string = urllib.parse.unquote_plus(escaped_string)
            backup_source = re.match('.*\n.*iframe src="(.+)"  height=.*\n.*', unescaped_string).group(1)
            form_post_params = { 'group' : 'all' }
            backup_data = requests.get('%sheatmap.php' % backup_source, data = form_post_params)
            save_from_static_instance_file(backup_data) # backup data source .save()
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def close_fxalarm_session(): # refactor: split each to 3 parts request setup, execute request, verify the request
    """
    This function checks if a current fxalarm session is active and closes it.
    """
    try:
        target_site = models.MyCredentials.objects.all().values('target_website')[0]['target_website']
        if 'UserID' in gcookies.items and 'deleted' != gcookies.get('UserID', {}):
            logout_response = requests.post('%slogout.php' % target_site)
            for cookie in logout_response.cookies:
                gcookies.set_cookie(cookie)
        if 'deleted' != gcookies.get('UserID', {}):
            gcookies.set_cookie( { 'UserID':'deleted' } )
        if 'UserID' not in gcookies.items and 'deleted' != gcookies.get('UserID', {}):
            raise RuntimeError('The logout operation failed in the function close_fxalarm_session().')
    except Exception as error:
        print(error)
        raise

def save_from_static_instance_file(inputfile):
    """
    This database function accepts a specified static html instance USD source file, calls the parse function,
    and saves the incomming USD data row at that moment as the save row occured.
    """
    try:
        usd = get_next_usd_parse(inputfile)
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
        raise

def get_target_website_cookies():
    """
    This function loads all supported browser cookies, and provides back the cookiejar structure
    of all the known and saved cookies for this application's target website
    :returns: cookiejar collection of all known cookies required for target website
    """
    gcookies = browser_cookie3.load()
    target_website = get_target_website()
    target_website = target_website.lstrip('http://www')
    return gcookies._cookies[target_website]

def get_target_website():
    """
    This function returns the target website this web application is using by querying the database for it.
    """
    return models.MyCredentials.objects.all().values('target_website')[0]['target_website']

def set_cookie(key, value, minutes_expire = 89):
    """
    This function sets the specified cookie using the specified key to the specified value with the
    specified expiration of 89 minutes as the default.
    :param 1: key as the cookie key as the name of this cookie
    :param 2: value as the value of which to set for this cookie
    :param 3: minutes_expire as the number of minutes before this specificed cookie expires
    """ # TODO: Write function to check what IP address the request object is running your code from!!!
    gcookies = browser_cookie3.load()
    if minutes_expire is None:
        max_age = 89  #89 minutes before expiration as the default if None is passed
    expires = datetime.datetime.strftime( 
        datetime.now(tzlocal()) + timedelta(seconds = max_age), "%a, %d-%b-%Y %H:%M:%S %Z"
        )
    created_cookie = browser_cookie3.create_cookie(
        get_target_website().lstrip('http://www'), #website for this cookie
        '/', #path for this cookie
        True, #is this cookie 'secure'?
        str(expires), #expiration for this cookie
        key, #key name for this cookie
        value #value for this cookie
        )
    browser_cookie3.chrome().set_cookie(created_cookie)