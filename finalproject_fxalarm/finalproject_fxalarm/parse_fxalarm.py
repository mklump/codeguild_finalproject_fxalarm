"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
from bs4 import BeautifulSoup
from django.http import HttpRequest
from django.http import HttpResponse

import requests
from . import models
import os

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
        raise RuntimeError(error)
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
        my_credentials = models.MyCredentials(username_as_email = username,
            password = pwd,
            target_website = website,
            )
        my_credentials.save()
    except Exception as error:
        print(error)
        raise RuntimeError(error)

def open_fxalarm_session(request: HttpRequest) -> bool:
    """
    This function reads the MyCredentials table for the existance of 1 row, and starts a new active session.
    """
    form_post_params = {
        'vchEmail': models.MyCredentials.username_as_email.objects.all()[0],
        'vchPassword': models.MyCredentials.password.objects.all()[0],
    }
    target_site = models.MyCredentials.target_website.objects.all()[0]
    r = requests.post('%slogin' % target_site, data = form_post_params)
    fxalarm = requests.post()

def get_and_keep_alive_realtime_data():
    """
    This function checks regularly that the current active session is still active, and calls parse function of realtime data.
    http://stackoverflow.com/questions/1622793/django-cookies-how-can-i-set-them
    """

def close_fxalarm_session(request: HttpRequest) -> bool:
    """
    This function accepts an HttpRequest from the view function, and checks if a current fxalarm session is active and closes it.
    http://docs.python-requests.org/en/master/user/quickstart/#cookies
    http://stackoverflow.com/questions/2489669/function-parameter-types-in-python
    :param 1: request as HttpRequest from the view function sent oridinally to open_fxalarm_session(), and kepted open by
    get_and_keep_alive_realtime_data() for real data gathering, and is now finished from a submit button signal from the page
    to stop gathering data, and immediately logout.
    :returns: True if the logout succeeded, otherwise it returns False.
    """
    target_site = models.MyCredentials.target_website.objects.all()[0]
    response = HttpResponse('')
    req = None
    if 'UserID' in request.COOKIES and 'deleted' != request.COOKIES['UserID']:
        req = requests.post('%slogout.php' % target_site)
        req.cookies['UserID'] = 'deleted' # OR EXECUTE
        response.set_cookie('UserID', 'deleted')
    if 'UserID' in request.COOKIES and 'deleted' == request.COOKIES['UserID'] or \
       'UserID' in req.cookies and 'deleted' == req.cookies['UserID']:
        return True
    else:
        return False

def set_cookie(response, key, value, days_expire=7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires,
                      domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

# Use the following code before sending a response:
def view(request: HttpRequest): # TODO: Write function to check what IP address the request object is running your code from!!!
  response = HttpResponse("hello")
  set_cookie(response, 'name', 'jujule')
  return response