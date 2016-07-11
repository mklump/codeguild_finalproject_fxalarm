"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
import sys
import selenium.webdriver.chrome.service as service
from selenium import webdriver
import seleniumrequests
from seleniumrequests import Remote
from subprocess import Popen, PIPE, STDOUT

def main():
    try:
        #JAVA_PROCESS = Popen(['java.exe', '-jar', './selenium-server-standalone-2.53.1.jar'],
        #          stdout=PIPE, stderr=STDOUT)
        #for line in JAVA_PROCESS.stdout:
        #    print(line)
        #if JAVA_PROCESS == None:
        #    raise RuntimeError('Staring the selenium server standalone failed to start.')
        #else:
        htmlunit_driver = Remote("http://localhost:4444/wd/hub",
                                    webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        htmlunit_driver
        driver = webdriver.Remote("http://localhost:4444/wd/hub",
                                    webdriver.DesiredCapabilities.HTMLUNITWITHJS)
    except Exception as error:
        print(error)
        raise

if __name__ == "__main__":
    sys.exit(int(main() or 0))