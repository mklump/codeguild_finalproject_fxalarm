"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
import sys
from bs4 import BeautifulSoup

def parse_html_source_file():
    soup_html_xml_parser = None
    try:
        with open('..\static\finalproject_fxalarm\sample_data\primary_data_sample.html') as html:
            soup_html_xml_parser = BeautifulSoup(html)
        # end with block/close file
    except Exception as error:
        print(error.__cause__())

def main():
    parse_html_source_file()

if __name__ == "__main__":
    sys.exit(int(main() or 0))