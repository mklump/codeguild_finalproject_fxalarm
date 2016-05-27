"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
import sys
import datetime
from dateutil.tz import tzlocal
from bs4 import BeautifulSoup

def parse_html_source_file(input_file:str):
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

def parse_currency_node(html_parser:str, currency_symbol:str):
    """
    This critical function accepts an object of type BeautifulSoup as the html parser, and also a specific currency
    symbol, and returns the matched session acceleration value for the current html snapshot GET request or file.
    :param 1: html_parser as an object of type BeautifulSoup as the html parser
    :param 2: currency_symbol as a specific currency symbol to retrieve
    :returns: a string representation of the matched session acceleration value for the current html snapshot GET request or file
    """
    match = html_parser.find(string = currency_symbol)
    data_match = match + '=' + match.next_element.next_element.string
    return data_match

def get_next_usd_parse(input_file:str):
    """
    This critical function accepts an input file to perform the extraction of the US Dollar session acceleration
    data snap shot at this moment in time, and returns this instance of the data stream.
    :param 1: input_file is the relative or remote path to the html file that will be html parsed for data.
    :returns: a string representation of the USD instance of the data stream
    """
    usd_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD', 'USDCHF', 'AUDUSD', 'NZDUSD']
    html_parser = parse_html_source_file(input_file)
    array = [ '%s ' % parse_currency_node(html_parser, symbol) for symbol in usd_symbols ]
    usd_stream = ''
    usd_stream = usd_stream.join(array)
    timenow = datetime.datetime.now(tzlocal())
    timenow = timenow.strftime('at %Y-%m-%d %H:%M:%S %Z')
    usd_stream += '%s' % timenow
    print(usd_stream)
    return usd_stream

def print_usd_at_now():
    get_next_usd_parse('primary_data_index_QC-22.html')
    get_next_usd_parse('backup_data_heatmap_GROUP-AD.html')
    get_next_usd_parse('backup_data_heatmap_GROUP-ALL.html')

def main():
    print_usd_at_now()

if __name__ == "__main__":
    sys.exit(int(main() or 0))