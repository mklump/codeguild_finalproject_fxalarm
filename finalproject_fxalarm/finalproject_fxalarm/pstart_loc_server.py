"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/pstart_loc_server.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016
"""
import sys
import threading
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from seleniumrequests import Remote
from seleniumrequests.request import RequestMixin

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
    an error has occurred
    """
    thread = threading.Thread(target=run_java_loc_server)
    thread.start()
    sleep(3)
    global JAVA_PROCESS
    return JAVA_PROCESS

if __name__ == "__main__":
    sys.exit(int(pstart_loc_server() or 0))