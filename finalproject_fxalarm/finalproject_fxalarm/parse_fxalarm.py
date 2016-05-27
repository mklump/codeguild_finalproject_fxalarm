"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
from bs4 import BeautifulSoup

def parse_html_source_file(input_file):
    """
    This critical function accepts an html input file that is the complete http GET response after
    correctly logging in.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed for data.
    :returns: an object as BeautifulSoup that is the class wrapper around the html python module for html parsing.
    """
    soup_html_xml_parser = None
    try:
        with open(input_file) as html:
            soup_html_xml_parser = BeautifulSoup(html, 'html.parser')
        # end with block/close file
    except Exception as error:
        print(error.__cause__())
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
    