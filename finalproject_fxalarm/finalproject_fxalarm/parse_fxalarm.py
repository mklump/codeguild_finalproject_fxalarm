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
import uuid
import os

gcookies = RequestsCookieJar()

def get_gcookies():
    """
    Get function for the global variable gcookies
    """
    return gcookies

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

def check_next_http_request(response_last_url, request_url, cookies_needed = None, request_params = None, headers = None, stream = None):
    """
    This function accepts a request_url, request_params, and cookies_needed for the next http request, checks if
    the url is 'executable', and then passes it to execute_next_http_request() with all the parameters if the
    complete path can be reached.
    :param 1: response_last_url is the Requests.Response of the last Requests.Get for use in the next
        Requests.Get() while streaming Requests.Reponse.text
    :param 2: request_url as the complete url to be checked
    :param 3: cookies_needed CookieJar (optional) dictionary to be used with this request execution
    :param 4: request_params (optional) to be used with this request execution
    :param 5: headers (optional) dictionary that must be included with this request execution such as tracked Referers
    :param 6: stream as (optional) whether to immediately download the response content 
    :returns: the returned requests.response object if all went well
    """
    try:
        response_last_url = requests.get(request_url)
        if 200 == response_last_url.status_code:
            response_last_url = execute_next_http_request(request_url, cookies_needed, request_params, headers, stream)
        else:
            raise RuntimeError('The request_url {0} returned status: {1}'.format(request_url, response_last_url.status_code))
        return response_last_url
    except Exception as error:
        print(error)
        raise

def execute_next_http_request(response_last_url, request_url, cookies_needed = None, request_params = None, headers = None, stream = None):
    """
    This fuction accepts a request_url, request_params, and cookies_needed for the next http request, and executes
    the full url with the get request parameters, and cookies collection to ensure the response was timly, and that the
    response has the correct response code. If it does, then the requests.reponse object is handed back to the next request.
    :param 1: response_last_url is the Requests.Response of the last Requests.Get for use in the next
        Requests.Get() while streaming Requests.Reponse.text
    :param 2: request_url as the complete url to be executed
    :param 3: cookies_needed CookieJar (optional) dictionary to be used with this request execution
    :param 4: request_params (optional) to be used with this request execution
    :param 5: headers (optional) dictionary that must be included with this request execution such as tracked Referers
    :param 6: stream as (optional) whether to immediately download the response content
    :returns: the returned requests.response object if all went well
    """
    try:
        response_last_url = requests.get(request_url, cookies = cookies_needed, data = request_params, headers = headers, stream = stream)
        get_target_website_cookies(response_last_url.cookies)
        if 5 < response_last_url.elapsed.total_seconds() or 200 != response_last_url.status_code:
            raise RuntimeError('The http request url: {0}, with streaming: {1}, with cookies: {2}, with get request data: {3}, and with headers: {4}' +
                               ' has failed with status code: {5}, and taking {6} seconds amount of time to see a response.'.format(
                               request_url, stream, cookies_needed, request_params, headers,
                               response_last_url.status_code, response_last_url.elapsed.total_seconds())
                               )
        return response_last_url
    except Exception as error:
        print(error)
        raise

def open_fxalarm_session(username_as_email, password):
    """
    This function reads the MyCredentials table for the existance of 1 row, and starts a new active session.
    :param 1: username_as_email as the secure credentials email as username from the database with the request
    :param 2: password as the secure credentials password from the database with the request
    :returns: a list of login_response, and the gcookies global cookies instances that were created which determines the active session
    """
    login_response = None
    try:
        form_post_params = {
            'vchEmail': username_as_email,
            'vchPassword': password,
            'x':37,
            'y':10,
        }
        target_site = get_target_website()
        header = { 'Referer':'%slogin' % target_site }
        get_target_website_cookies()
        if 'PHPSESSID' not in get_gcookies().iterkeys():
            uid = uuid.uuid4()
            set_cookie('PHPSESSID', uid.hex)
        login_response = requests.post('%slogin' % target_site, data = form_post_params, cookies = get_gcookies(), headers = header)
        get_target_website_cookies(login_respons.cookies)
        if '9951' != login_response.cookies.get('UserID', {}):
            raise RuntimeError('The login operation failed in the function open_fxalarm_session(), or ' +
                               'a login attempt at the target website is not currently allowed (90min lockout).')
        #close_fxalarm_session()
        return_list = [ login_response, get_gcookies() ]
        return return_list
    except Exception as error:
        print(error)
        close_fxalarm_session(login_response, get_gcookies())
        raise

def step_through_membersarea_to_source(response_last_url, cookies_needed):
    """
    This function immediately follows after open_fxalarm_session(), but before execute_main_data_gathering_loop() to
    step the requests mock browser object through the required click web links to the main streaming html page.
    :param 1: response_last_url is the Request.Response object instance that was passed from the last call to open_fxalarm_session()
    :param 2: cookies_needed is the RequestsCookieJar object instance that was passed from the last call to open_fxalarm_session()
    """
    try:
        target_site = get_target_website()
        get_target_website_cookies(cookies_needed)
        header = { 'Referer':'%slogin' % target_site }
        response_last_url = check_next_http_request(response_last_url,'%smember-area.php' % target_site, cookies_needed, None, header)
        header = { 'Referer':'%smember-area.php' % target_site }
        response_last_url = check_next_http_request(response_last_url,'%sheatmap.php' % target_site, cookies_needed,  None, header)
        return_list = [ response_last_url, get_gcookies() ]
        return return_list
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def execute_main_data_gathering_loop(response_last_url, cookies_needed):
    """
    This function checks regularly that the current active session is still active,
    and calls parse function saving the realtime data.
    :param 1: response_last_url is the Request.Response object instance that was passed from the last call to step_through_membersarea_to_source()
    :param 2: cookies_needed is the RequestsCookieJar object instance that was passed from the last call to step_through_membersarea_to_source()
    """
    try:
        target_site = get_target_website()
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
        return_list = [ response_last_url, get_gcookies() ]
        return return_list
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def close_fxalarm_session(response_last_url, cookies_needed):
    """
    This function checks if a current fxalarm session is active and closes it by executing 3 http requests.get() calls to properly logout.
    :param 1: response_last_url is the Request.Response object instance that was passed from the last call to open_fxalarm_session()
    :param 2: cookies_needed is the RequestsCookieJar object instance that was passed from the last call to open_fxalarm_session()
    """
    try:
        target_site = get_target_website()
        header = { 'Referer':'%sheatmap.php' % target_site }
        get_gcookies().update(get_target_website_cookies(cookies_needed).copy())
        response_last_url = check_next_http_request(response_last_url,'%slogout.php' % target_site, cookies_needed, None, header)
        #response_last_url = check_next_http_request(response_last_url,'%slogout.php' % target_site) #original request
        response_last_url = check_next_http_request(response_last_url,'%slogin.php' % target_site, cookies_needed, { 'err' : 2 }, header)
        response_last_url = check_next_http_request(response_last_url,'%slogin.php' % target_site, cookies_needed, None, header)
        if 'deleted' != get_gcookies().get('UserID', {}):
            set_cookie('UserID', 'deleted')
        if 'UserID' not in get_gcookies().items() and 'deleted' != get_gcookies().get('UserID', {}):
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

def get_target_website_cookies(more_cookies_to_load = None):
    """
    This function loads all supported browser cookies, and provides back the cookiejar structure
    of all the known and saved cookies for this application's target website
    :param 1: more_cookies_to_load represents a collection of the cookies set from the last response to the previous get request
    :returns: cookiejar collection of all known cookies required for target website
    """
    get_gcookies().update(browser_cookie3.load())
    target = get_target_website()
    target_website1 = target.lstrip('http://').rstrip('/')
    target_website2 = target.lstrip('http://www').rstrip('/')
    if target not in get_gcookies()._cookies:
        return RequestsCookieJar()
    else:
        get_gcookies().clear()
        for cookie in browser_cookie3.load(target_website1):
            get_gcookies().set_cookie(cookie)
        for cookie in browser_cookie3.load(target_website2):
            get_gcookies().set_cookie(cookie)
        if None != more_cookies_to_load:
            for cookie in more_cookies_to_load:
                get_gcookies().set_cookie(cookie)
        return get_gcookies()

def get_target_website():
    """
    This function returns the target website this web application is using by querying the database for it.
    """
    return models.MyCredentials.objects.all().values('target_website')[0]['target_website']

def set_cookie(key, value, minutes_expire = None):
    """
    This function sets the specified cookie using the specified key to the specified value with the
    specified expiration of 89 minutes as the default.
    :param 1: key as the cookie key as the name of this cookie
    :param 2: value as the value of which to set for this cookie
    :param 3: minutes_expire as the number of minutes before this specificed cookie expires
    :returns: the created_cookie that was set
    """ # TODO: Write function to check what IP address the request object is running your code from!!!
    if minutes_expire is None:
        max_age = 89 * 60 #89 minutes before expiration as the default if None is passed
    expires = datetime.strptime(datetime.strftime( 
        datetime.now(tzlocal()) + timedelta(seconds = max_age), "%a, %d-%b-%Y %H:%M:%S %Z"
        ), "%a, %d-%b-%Y %H:%M:%S %Z")
    created_cookie = browser_cookie3.create_cookie(
        get_target_website().lstrip('http://').rstrip('/'), #website for this cookie
        '/', #path for this cookie
        True, #is this cookie 'secure'?
        expires.toordinal(), #expiration for this cookie
        key, #key name for this cookie
        value #value for this cookie
        )
    browser_cookie3.chrome().set_cookie(created_cookie)
    while key in get_target_website_cookies().items():
        get_gcookies().clear(get_target_website().lstrip('http://').rstrip('/'), '/', key)
    get_gcookies().set_cookie(created_cookie)
    return created_cookie