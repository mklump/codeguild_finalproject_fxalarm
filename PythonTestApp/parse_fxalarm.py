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
        with open('primary_data_sample.html') as html:
            soup_html_xml_parser = BeautifulSoup(html, 'html.parser')
        # end with block/close file
    except Exception as error:
        print(error.__cause__())
    return soup_html_xml_parser

def main():
    html_parser = parse_html_source_file()
    string_match = html_parser.find(string = 'EURUSD')
    print(string_match + ' ' + string_match.next_element.next_element.contents[0]) # We found something!

if __name__ == "__main__":
    sys.exit(int(main() or 0))