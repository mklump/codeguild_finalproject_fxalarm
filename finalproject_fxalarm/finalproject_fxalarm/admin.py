"""
Python Coding Bootcamp (pdxcodeguild)
Code File for finalproject_fxalarm/admin.py
by: Matthew James K on 5/16/2016
"""
from django.contrib import admin
from . import models

admin.site.register(models.MyCredentials)
admin.site.register(models.USD)
