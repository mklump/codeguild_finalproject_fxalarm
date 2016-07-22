"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
import re
import sys
import urllib
import threading
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from seleniumrequests import Remote
from seleniumrequests.request import RequestMixin
from selenium.webdriver import Remote as remote_webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

JAVA_PROCESS = None

class HtmlUnitJS(Remote, RequestMixin):
    def __init__(self, **kwargs):
        return Remote.__init__(self, **kwargs)

def run_java_loc_server():
    """
    This function delegate for the main thread start is responsible for launching the java based
    selenium-server-standalone for executing our required http get and post http requests to the
    javascript protected content on the target web site for parsing.
    """
    global JAVA_PROCESS
    try:
        JAVA_PROCESS = Popen(['java.exe', '-cp', # -cp <class search path of directories and zip/jar files> for jvm javaruntime v7+
                              'htmlunit-driver-standalone-2.21.jar;' +
                              'selenium-server-standalone-2.53.1.jar',
                              'org.openqa.grid.selenium.GridLauncher'],
                  stdout=PIPE, stderr=STDOUT)
        for line in JAVA_PROCESS.stdout:
            print(line)
    except Exception as error:
        print(error)
        raise

def pstart_loc_server():
    """
    This function is responsible for creating the separate threading.Thread in which our selenium
    server standalone will execute.
    :returns: the Popen local object instance of JAVA_PROCESS as Popen object instance to kill when
    an error has occurred
    """
    thread = threading.Thread(target=run_java_loc_server)
    thread.start()
    sleep(5)
    global JAVA_PROCESS
    return JAVA_PROCESS

def main():
    try:
        java_proc = pstart_loc_server()
        htmlunit_driver = HtmlUnitJS(
            command_executor='http://localhost:4444/wd/hub',
            keep_alive=True,
            desired_capabilities={'browserName': 'htmlunit',
                                  'javascriptEnabled': True,
                                  'platform': 'ANY',
                                  'version': 2})

        encoded_script = ''
        decoded = urllib.parse.unquote(encoded_script)
        source_script = re.match('[ \n\t]*<script.*>[ \n\t]*(.+)[ \n\t]*<\/script>$', decoded)
        if source_script == None:
            raise RuntimeError('No match.')
        else:
            outter_script = source_script.group(1)
        inner_url = re.match('.*iframe src=\"([httphm:\/\.0-9]+)\"', outter_script).group(1)
        htmlunit_driver.get('')
        euro_us_session = htmlunit_driver.request(method='get', url=inner_url+'heatmap.php?group=ad', page_load_timeout=2)
        asian_session = htmlunit_driver.request(method='get', url=inner_url+'heatmap.php?group=all', page_load_timeout=2)
        print('EURO US SESSION')
        print(euro_us_session.text)
        print('ASIAN SESSION')
        print(asian_session.text)
        
        #htmlunit_driver.execute_script(outter_script)
        #source1 = htmlunit_driver.find_element_by_tag_name('html')
        #source2 = htmlunit_driver.page_source
        #source3 = htmlunit_driver.page_source.text
        #find_elements_by_tag_name
        
        #htmlunit_driver.execute_script('return document.readyState;').equals('complete')

        #htmlunit_driver.request(method='POST', url='http://204.12.52.120/hm3488746/',
        #    find_window_handle_timeout=1, page_load_timeout=2, headers={}, cookies={}, data={})
        #htmlunit_driver.get('http://204.12.52.120/hm3488746/')

        #htmlunit_driver = Remote("http://localhost:4444/wd/hub",
        #                         DesiredCapabilities.HTMLUNITWITHJS)

        #htmlunit_driver = webdriver.Remote("http://localhost:4444/wd/hub",
        #                                   DesiredCapabilities.HTMLUNITWITHJS)
    except Exception as error:
        java_proc.terminate() #stop the running server process container thread!
        print(error)
        sys.exit(-1)
        raise

if __name__ == "__main__":
    sys.exit(int(main() or 0))