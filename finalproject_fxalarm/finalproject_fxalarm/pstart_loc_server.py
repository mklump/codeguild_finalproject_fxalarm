"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/pstart_loc_server.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016
"""
import threading
from time import sleep
from subprocess import Popen, PIPE, STDOUT

JAVA_PROCESS = None

def run_java_loc_server():
    """
    This function delegate for the main threadstart is responsible for launching the java based
    selenium-server-standalone for executing our required http get and post http requests to the
    javascript protected content on the target web site for parsing.
    """
    global JAVA_PROCESS
    try:
        JAVA_PROCESS = Popen(['java.exe', '-jar', './selenium-server-standalone-2.53.1.jar'],
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
    :returns: JAVA_PROCESS as Popen object instance of the server process that was started
    """
    thread = threading.Thread(target=run_java_loc_server)
    thread.start()
    global JAVA_PROCESS
    return JAVA_PROCESS
    
if __name__ == "__main__":
    sys.exit(int(pstart_loc_server() or 0))