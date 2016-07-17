"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016
"""
import re
import urllib
import time
import random
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzlocal
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from . import models
from . import pstart_loc_server

java_server = None
"""
The java_server global variable represents the instance of selenium remote htmlunit web driver.
"""

def get_java_server():
    """
    This is the get function for the global variable java_server.
    """
    return java_server

htmlunitjs_driver = None
"""
This htmlunitjs_driver global variable represents client connection instance to the selenium
remote htmlunit web driver.
"""

def get_htmlunitjs_driver():
    """
    This is the get function for the globale variable htmlunitjs_driver.
    """
    return htmlunitjs_driver

def parse_html_source_file(input_file):
    """
    This critical function accepts an html input file that is the complete http GET response
    after correctly logging in.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed
    for data.
    :returns: an object as BeautifulSoup that is the class wrapper around the html python module
    for html parsing.
    """
    soup_html_xml_parser = None
    try:
        if len(input_file) <= 260:
            with open(input_file, mode='rt') as html:
                soup_html_xml_parser = BeautifulSoup(html, 'html.parser')
            # end with block/close file
        else:
            soup_html_xml_parser = BeautifulSoup(input_file, 'html.parser')
        return soup_html_xml_parser
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def parse_currency_node(html_parser, currency_symbol):
    """
    This critical function accepts an object of type BeautifulSoup as the html parser, and also
    a specific currency symbol, and returns the matched session acceleration value for the current
    html snapshot GET request or file.
    :param 1: html_parser as an object of type BeautifulSoup as the html parser
    :param 2: currency_symbol as a specific currency symbol to retrieve
    :returns: a string representation of the matched session acceleration value for the current
    html snapshot GET request or file
    """
    match = html_parser.find(string=currency_symbol)
    return ('{0}={1}').format(match, match.next_element.next_element.string)

def get_next_usd_parse(input_file):
    """
    This critical function accepts an input file to perform the extraction of the US Dollar session
    acceleration data snap shot at this moment in time, and returns this instance of the data
    stream.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed
    for data.
    :returns: a list/array [] representation of the USD instance of the data stream
    """
    usd_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD', 'USDCHF', 'AUDUSD', 'NZDUSD']
    html_parser = parse_html_source_file(input_file)
    return ['%s' % parse_currency_node(html_parser, symbol) for symbol in usd_symbols]

def set_fxalarm_db_login(username, pwd, website):
    """
    This function can only be run current from a python interactive console.
    This function accepts 3 parameters, to save to the MyCredentials database table for access by
    this program - username_as_email, password, and target_website.
    Do not remove this function! This is for future use to add this one row without the admin page.
    :param 1: username as string to save to username_as_email
    :param 2: pwd as string to save to password
    :param 3: website as string to save to target_website
    """
    try:
        my_credentials = models.MyCredentials(
            username_as_email=username,
            password=pwd,
            target_website=website,)
        my_credentials.save()
    except Exception as error:
        print(error)
        raise

def get_target_website():
    """
    This function returns the target website this web application is using by querying the
    database for it.
    """
    return models.MyCredentials.objects.all().values('target_website')[0]['target_website']

def startup_htmlunitjs_webdriver():
    """
    This function starts up the selenium-requests remote webdriver, and simultaneously connects
    the htmlunit parser client web broswer.
    """
    global java_server
    global htmlunitjs_driver
    java_server = pstart_loc_server.pstart_loc_server()
    if java_server == None:
        raise RuntimeError('Staring the selenium server standalone failed to start.')
    else: #htmlunitjs_driver IS NOW mainsource_session
        htmlunitjs_driver = pstart_loc_server.HtmlUnitJS(
            command_executor='http://localhost:4444/wd/hub',
            keep_alive=True,
            desired_capabilities={'browserName': 'htmlunit',
                                  'javascriptEnabled': True,
                                  'platform': 'ANY',
                                  'version': 2})

def check_http_response(target_request_url):
    """
    This function accepts a target_request_url and checks if the url is 'executable', and has
    correct responsiveness based on the response status code.
    :param 1: target_request_url as a string of the complete url to be checked for responsiveness
    :returns: the returned requests.session.response object if all went well
    """
    try:
        response_last_url = get_htmlunitjs_driver().get(target_request_url)
        if response_last_url != None and response_last_url.status_code >= 400:
            raise RuntimeError(
                ('The request_url {0} returned status: {1}').format(
                    request_url,
                    response_last_url.status_code))
        return response_last_url
    except Exception as error:
        print(error)
        raise

def execute_next_http_request(response_last_url,
                              request_url,
                              is_get_http_request=True,
                              request_params=None,
                              headers=None):
    """
    This function accepts a request_url, request_params, and is_get_http_request for the next http
    request, and executes the full url all the needed request argument settings. If it does,
    then the requests.reponse object is handed back to the next request.
    :param 1: response_last_url is the Requests.Response of the last Requests.Get for use in the
        next Requests.Get() while streaming Requests.Reponse.text
    :param 2: request_url as the complete url to be executed
    :param 3: is_get_http_request as a bool is a flag that will execute this request as a GET
        http request if the flag is True, otherwise the request will be a POST if it is False
    :param 4: request_params (optional) to be used with this request execution
    :param 5: headers (optional) dictionary that must be included with this request execution such
        as tracked Referers
    :returns: the requests.response object of the requests.Session.Get()/.Post() if all went well
    """
    try:
        if is_get_http_request:
            response_last_url = get_htmlunitjs_driver().request(method='get',
                url=request_url,         # required for all requests
                data=request_params,     # required for most requests
                headers=headers          # required for all requests
                )
        else:
            response_last_url = get_htmlunitjs_driver().request(method='post',
                url=request_url,         # required for all requests
                data=request_params,     # required for most requests
                headers=headers          # required for all requests
                )
        log_changed_cookies(response_last_url)
        return check_response_last_url(response_last_url, headers, request_params)
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def check_response_last_url(response_last_url, request_headers=None, request_params=None):
    """
    This function accepts the response_last_url as the requests.Response object instance of the
    last http GET or POST request, and tests the responsiveness and status code of that request.
    NOTE: Do not call this function outside of try/except code block.
    :param 1: response_last_url as the requests.Response instance being tested
    :param 2: headers dictionary included with this request to be tested
    :param 3: request_params dictionary included with this request to be tested
    :returns: the requests.Response object of the requests.Session.Get()/.Post() if all went well
    """
    log_changed_cookies(response_last_url)
    if response_last_url.elapsed.total_seconds() > 5 or response_last_url.status_code >= 400:
        log_line = ('\nThe http request url: {0}, with cookies: {1}, with get request ' +
                                'data: {2}, and with headers: {3} has failed with status code: ' +
                                '{4}, and taking {5} seconds amount of time to see a ' +
                                'response.').format(response_last_url.url, response_last_url.cookies,
                                                  request_params, request_headers,
                                                  response_last_url.status_code,
                                                  response_last_url.elapsed.total_seconds())
        with open('session_cookie_log.txt', mode='+a') as cookie_log:
            cookie_log.writelines([log_line]) #append a single line on this cookie change
        #end with open('session_cookie_log.txt') block close cookie_log obj for next one
        raise RuntimeError(log_line)
    return response_last_url

def open_fxalarm_session(username_as_email, password, response_last_url):
    """
    This function reads the MyCredentials table for the existence of 1 row, and starts a new
        active session.
    :param 1: username_as_email as the secure credentials email as username from the database with
        the request
    :param 2: password as the secure credentials password from the database with the request
    :param 3: response_last_url is the Requests.Response of the last Requests.Get for use in the
        next Requests.Get() while streaming Requests.Reponse.text
    :returns: login_response that this attempted login through requests.session.post() received
    """
    try:
        form_post_params = {
            'vchEmail': username_as_email,
            'vchPassword': password,
            'x':random.randint(1, 49),
            'y':random.randint(1, 19),
        }
        target_site = get_target_website()
        header = {'Referer':'%slogin' % target_site}
        response_last_url = execute_next_http_request(response_last_url,       #Previous response
                                                      '%slogin' % target_site, #First POST request
                                                      False,                 #POST request, not GET
                                                      form_post_params, #Dict. of POST login data
                                                      header)           #Referer header entry
        if get_htmlunitjs_driver().get_cookie('UserID') == None:
            raise RuntimeError(
                'The login operation failed in the function ' +
                'open_fxalarm_session(), or a login attempt at the target ' +
                'website is not currently allowed (90min lockout).'
                )
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_memberarea_navigation(response_last_url):
    """
    This function request navigation immediately follows after open_fxalarm_session(), but before
        request_heatmap_navigation() to step the requests mock browser object through the required
        click web links to the main streaming html page.
    :param 1: response_last_url is the Request.Response object instance that was passed from
        the last call to open_fxalarm_session()
    :returns: response_last_url that this attempted requests.session.get() received
    """
    try:
        target_site = get_target_website()
        header = {'Referer':'%slogin' % target_site}
        response_last_url = execute_next_http_request(response_last_url,
                                                      '%smember-area.php' % target_site,
                                                      True,
                                                      None,
                                                      header)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_heatmap_navigation(response_last_url):
    """
    This function request navigation immediately follows after request_memberarea_navigation(),
        but before request_mainsource_link() to step the requests mock browser object
        through the required click web links to the main streaming html page.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_memberarea_navigation()
    :returns: response_last_url that this attempted requests.session.get() received
    """
    try:
        target_site = get_target_website()
        header = {'Referer':'%smember-area.php' % target_site}
        response_last_url = execute_next_http_request(response_last_url,
                                                      '%sheatmap.php' % target_site,
                                                      True,
                                                      None,
                                                      header)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_mainsource_link(response_last_url):
    """
    This function request navigation immediately follows after request_heatmap_navigation(),
        but before request_mainsource_data(). This function is responsible for finding
        the main data source web link in an active data session to be passed to the html scrape
        functions that are not part of this request.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_heatmap_navigation()
    :returns: response_last_url that this attempted requests.session.get() received
    """
    try:
        target_site = get_target_website()
        header = {'Referer':'%sheatmap.php' % target_site}
        response_last_url = execute_next_http_request(response_last_url,
                                                      '%sget_v4.php' % target_site,
                                                      True,
                                                      None,
                                                      header)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def get_mainsource_components(response_last_url):
    """
    This function immediately follows after request_mainsource_link(), but before
        request_mainsource_data().
    This function is responsible for gathering the required request components for the
        request_mainsource_data() function.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_mainsource_link()
    :returns: a list of strings for the response_last_url, primary_source_url, request_header, and
        the request_postdata to be used by the next calling function in views.py
    """
    try:
        target_site = get_target_website()
        request_header = {'Referer':'%sget_v4.php' % target_site, 'Origin':target_site}
        response_last_url.encoding = 'utf-8'
        html = BeautifulSoup(response_last_url.text, 'html.parser')
        primary_source_url = html.find(attrs={'id':'acForm'}).attrs['action']
        log_changed_urlsite(primary_source_url)
        mainmap_key = html.find(name='input', attrs={'type':'hidden', 'name':'ak'}).attrs['value']
        request_postdata = {'ak':mainmap_key}
        return [response_last_url, primary_source_url, request_header, request_postdata]
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def create_mainsource_session(response_last_url, mainsource_link, request_header, request_postdata):
    """
    The URL redirect that is parsed from the response of the mainsource_link for where to go
    appears to require a second sub-session as an http web session in addition to the main login
    session from the target website. This is accomplished by creating and returning a new
    sub-session with the current main session still going.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_mainsource_link()
    :param 2: mainsource_link as the URL that is creating the new session for the main source to run
    :param 3: request_header as the dictionary collection to be posted with the mainsource_link
    :param 4: request_postdata as the dictionary collection of form post data to start new session
    :returns: response_last_url request.Response object instance of this post request
    """
    try:
        response_last_url = htmlunitjs_driver.request(method='post', url=mainsource_link,
                                                      find_window_handle_timeout=2,
                                                      page_load_timeout=2,
                                                      data=request_postdata,
                                                      headers=request_header)
        check_response_last_url(response_last_url, request_header, request_postdata)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_mainsource_data(response_last_url):
    """
    This function immediately follows after get_mainsource_components(), but before
        request_backupsource_data().
    This function is responsible for retrieving the main source data from the main source link.
    The response.text after the request executes should be the full html data source we are
        looking for!
    :param 1: response_last_url requests.Response object instance of the last http post request
    :returns: a list of two things - htmlunitjs_driver as a seleniumrequests.Remote htmlunit
        webdriver object instance that is the sub-session for mainsource_link, and also
        response_last_url response object of this post
    """
    try:
        primary_source_url = response_last_url.url
        request_headers = {'Referer':primary_source_url}
        time.sleep(3) # Wait here 3 seconds before proceeding.
        response_last_url = htmlunitjs_driver.request(
            method='get', url=primary_source_url, find_window_handle_timeout=2,
            page_load_timeout=2, headers=request_headers)
        check_response_last_url(response_last_url, request_headers)
        response_last_url.encoding = 'utf-8'
        save_parsed_fxdata_to_usdtable(response_last_url.text) # Data! -> primary data .save()
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_backupsource_link(response_last_url):
    """
    This function request navigation (Asian Session Only <group=all> not European Session
        <group=ad>) immediately follows after request_mainsource_data(), but before
        request_backupsource_data(). This function is responsible for finding
        the backup data source web link in an active data session to be passed to the html scrape
        functions that are not part of this request.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_mainsource_data()
    :returns: response_last_url that this attempted requests.session.get() received
    """
    try:
        target_site = get_target_website()
        form_post_params = {'chk' : 2}
        header = {'Referer':'%sheatmap.php' % target_site}
        response_last_url = execute_next_http_request(response_last_url,
                                                      '%sget.php?chk=2' % target_site,
                                                      True,
                                                      form_post_params,
                                                      header)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def request_backupsource_data(response_last_url):
    """
    This function request navigation (Asian Session Only <group=all> not European Session
        <group=ad>) immediately follows after request_backupsource_link(), but before
        close_fxalarm_session().
    This function is responsible for executing from the request for the backup data source html
        page in case of the event that the main source html page were to fail to respond.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last call to request_backupsource_link()
    :returns: response_last_url that this attempted requests.session.get() received
    """
    try:
        response_last_url.encoding = 'utf-8'
        escaped_string = re.match('.+unescape\(\"(.+)\"\)\);', response_last_url.text).group(1)
        unescaped_string = urllib.parse.unquote_plus(escaped_string)
        backup_source_url = re.match('.*\n.*iframe src="(.+)"  height=.*\n.*',
                                     unescaped_string).group(1)
        log_changed_urlsite(backup_source_url)
        header = {'Referer':backup_source_url}
        response_last_url = execute_next_http_request(response_last_url,
                                                      backup_source_url,
                                                      True,
                                                      None,
                                                      header)
        response_last_url.encoding = 'utf-8'
        #Backup data!  -> backup data source .save()
        save_parsed_fxdata_to_usdtable(response_last_url.text)
        return response_last_url
    except Exception as error:
        print(error)
        close_fxalarm_session(response_last_url)
        raise

def close_fxalarm_session(response_last_url = None):
    """
    This function checks if a current fxalarm session is active and closes it by executing 3 http
        requests.get() calls to properly logout.
    ALL OF THESE 3 REQUESTS MUST HAPPEN TOGETHER AS ONE UNIT, NOT ONE APART.
    :param 1: response_last_url is the Request.Response object instance that was passed from the
        last http request
    """
    try:
        target_site = get_target_website()
        header = {'Referer':'%sheatmap.php' % target_site}
        login_cookie = get_htmlunitjs_driver().get_cookie('UserID')
        login_cookie['value'] = 'deleted'
        get_htmlunitjs_driver().delete_cookie('UserID')
        get_htmlunitjs_driver().add_cookie(login_cookie)
        response_last_url = execute_close_requests(response_last_url, target_site)
        if 'UserID' in get_htmlunitjs_driver().get_cookies():
            raise RuntimeError('The logout operation failed in the function ' +
                               'close_fxalarm_session(). Cookie name=\'UserID\' was present - ' +
                               'please wait 90min to login again, and contact support.')
        get_htmlunitjs_driver().quit()
        get_java_server().terminate() #stop the running server process container thread!
    except Exception as error:
        print(error)

def execute_close_requests(response_last_url, target_site):
    """
    This function executes the two close requests for close_fxalarm_session(response_last_url)
    :param 1: response_last_url as the requests.session.response instance of the last http request
    :param 2: target_site as the current target of these http close requests
    """
    header = {'Referer':'%sheatmap.php' % target_site}
    response_last_url = execute_next_http_request(
        response_last_url, '%slogout.php' % target_site, True, None, header)
    response_last_url = execute_next_http_request(
        response_last_url, '%slogin.php' % target_site, True, {'err' : 2}, header)
    return response_last_url

def save_parsed_fxdata_to_usdtable(inputfile):
    """
    This database function accepts a specified static html instance USD source file, calls the
    parse function, and saves the incoming USD data row at that moment as the save row occurred.
    """
    try:
        usd_parse = get_next_usd_parse(inputfile) #returns usd_parse list of 7 float values needed.
        usd_instance = models.USD(
            EURUSD=float(usd_parse[0].rstrip('%').split('=')[1]),
            GBPUSD=float(usd_parse[1].rstrip('%').split('=')[1]),
            USDJPY=float(usd_parse[2].rstrip('%').split('=')[1]),
            USDCAD=float(usd_parse[3].rstrip('%').split('=')[1]),
            USDCHF=float(usd_parse[4].rstrip('%').split('=')[1]),
            AUDUSD=float(usd_parse[5].rstrip('%').split('=')[1]),
            NZDUSD=float(usd_parse[6].rstrip('%').split('=')[1]),
            timestamp=datetime.now(tzlocal()))
        usd_instance.save()
    except Exception as error:
        print(error)
        close_fxalarm_session()
        raise

def log_changed_cookies(previous_response=None):
    """
    This function loads all supported cookies, and provides back the cookiejar structure
        of all the known and saved cookies for comparison/logging for this application's
        target website while an active session is in progress.
    :param 1: previous_response represents the previous response including the response
        cookies of the last http request.
    """
    all_cookies = get_htmlunitjs_driver().get_cookies()
    target = get_target_website()
    target_website1 = target.lstrip('http://').rstrip('/')
    target_website2 = target.lstrip('http://www').rstrip('/')
    if target_website1 not in all_cookies and \
        target_website2 not in all_cookies and \
        len(previous_response.cookies) == 0:
        return None
    if len(previous_response.cookies) > 0:
        for cookie in previous_response.cookies:
            str_cookie_expires = 'None'
            if cookie.expires != None:
                str_cookie_expires = datetime.fromtimestamp(
                    cookie.expires).replace(tzinfo=tzlocal()).strftime('%Y-%m-%d %H:%M:%S %Z')
            log_line = ('\nA cookie was set by the URL: {0} was found in the last http ' + \
                'response: -> Name:{1} Value:{2} Expires:{3}.').format(
                    previous_response.url, cookie.name, cookie.value, str_cookie_expires)
            print(log_line)
            with open('session_cookie_log.txt', mode='+a') as cookie_log:
                cookie_log.writelines([log_line]) #append a single line on this cookie change
            #end with open('session_cookie_log.txt') block close cookie_log obj for next one

def add_cookie(key, value, minutes_expire=None):
    """
    This function sets the specified cookie using the specified key to the specified value with
        the specified expiration of 89 minutes as the default. Do not remove yet! -> Future Need
    :param 1: key as the cookie key as the name of this cookie
    :param 2: value as the value of which to set for this cookie
    :param 3: minutes_expire as the number of minutes before this specified cookie expires
    """
    if minutes_expire is None:
        max_age = 89 * 60 #89 minutes before expiration as the default if None is passed
    expires = datetime.strptime(
        datetime.strftime(
            datetime.now(tz=tzlocal()) +
            timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S %Z"),
        "%a, %d-%b-%Y %H:%M:%S %Z"
        )
    created_cookie = get_htmlunitjs_driver().add_cookie({
        'name':key, #key name for this cookie
        'value':value, #value for this cookie
        'path':'/', #path for this cookie
        'domain':get_target_website().lstrip('http://').rstrip('/'), #website for this cookie
        'secure':True, #is this cookie 'secure'?
        'expiry':expires.toordinal() #expiration for this cookie
        })

def erase_saved_cookielogfile():
    """
    This function erases the saved log file 'session_cookie_log.txt' in the project root.
    """
    with open('session_cookie_log.txt', mode='+w') as wiped:
        wiped.writelines([('This cookie log file was last cleared on: {0}').format(
            datetime.now(tz=tzlocal()).strftime('%Y-%m-%d %H:%M:%S %Z'))])

def log_changed_urlsite(changed_urlsite: str):
    """
    This function logs any new website URLs encountered during the course of this application's
        execution that are not the targeted website stored as part of this application's database.
    :param 1: changed_urlsite as the parsed or found website not in the database
    """
    target = get_target_website()
    if changed_urlsite != target:
        log_line = ('\nA URL different from the target website in DB: {0} was found/parsed.'
                    ).format(changed_urlsite)
        print(log_line)
        with open('session_cookie_log.txt', mode='+a') as cookie_log:
            cookie_log.writelines([log_line]) #append a single line on this cookie change
        #end with open('session_cookie_log.txt') block close cookie_log obj for next one