"""
Python Coding Bootcamp (pdxcodeguild)
Code File for finalproject_fxalarm/admin.py
by Matthew James K (PIPs for Heaven, LLC) on 5/25/2016
"""
from django.contrib import admin
from . import models

admin.site.register(models.MyCredentials)
admin.site.register(models.USD)
