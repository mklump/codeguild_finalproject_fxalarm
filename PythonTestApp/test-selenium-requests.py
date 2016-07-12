"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
import sys
import threading
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from seleniumrequests import Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from seleniumrequests.request import RequestMixin
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

JAVA_PROCESS = None

class HtmlUnitJS(Remote, RequestMixin):
    def __init__(self, **kwargs):
        return Remote.__init__(self, **kwargs)

def run_java_loc_server():
    """
    This function delegate for the main threadstart is responsible for launching the java based
    selenium-server-standalone for executing our required http get and post http requests to the
    javascript protected content on the target web site for parsing.
    """
    global JAVA_PROCESS
    try:
        JAVA_PROCESS = Popen(['java.exe', '-cp',
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
    an error has occured
    """
    thread = threading.Thread(target=run_java_loc_server)
    thread.start()
    sleep(5)
    global JAVA_PROCESS
    return JAVA_PROCESS

def main():
    try:
        java_proc = pstart_loc_server()
        htmlunit_driver = HtmlUnitJS(command_executor='http://localhost:4444/wd/hub',
                                     desired_capabilities={'browserName': 'htmlunit',
                                                           'javascriptEnabled': True,
                                                           'platform': 'ANY',
                                                           'version': 'firefox'})
        htmlunit_driver.set_page_load_timeout(2)
        htmlunit_driver.set_script_timeout(2)
        web_driver_wait = WebDriverWait(htmlunit_driver, 1, 0.5, Exception)
        #htmlunit_driver.execute_script('return document.readyState;').equals('complete')
        htmlunit_driver.get('http://www.forexearlywarning.com')
        htmlunit_driver.request(method='POST', url='http://www.forexearlywarning.com',
            find_window_handle_timeout=1, page_load_timeout=2, headers={}, cookies={}, data={})

        htmlunit_driver = Remote("http://localhost:4444/wd/hub",
                                 DesiredCapabilities.HTMLUNITWITHJS)
        
        htmlunit_driver = webdriver.Remote("http://localhost:4444/wd/hub",
                                           DesiredCapabilities.HTMLUNITWITHJS)
    except Exception as error:
        java_proc.terminate() #stop the running server process container thread!
        print(error)
        sys.exit(-1)
        raise

if __name__ == "__main__":
    sys.exit(int(main() or 0))