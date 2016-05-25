"""
Python Coding Bootcamp (pdxcodeguild)
FXAlarm Final Project file finsalproject_fxalarm/parse_fxalarm.py
by Matthew James K on 5/25/2016
"""
from bs4 import BeautifulSoup

def parse_html_source_file():
    with open('..\static\finalproject_fxalarm\sample_data\primary_data_sample.html') as html: