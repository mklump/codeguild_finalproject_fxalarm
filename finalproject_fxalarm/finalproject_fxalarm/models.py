"""
Python Coding Bootcamp (pdxcodeguild)
Program exercise file finalproject_fxalarm/models.py
by Matthew James K on 5/19/2016

Definition of models.
"""

from django.db import models
import datetime
from dateutil.tz import tzlocal

# Create your models here.
class MyCredentials(models.Model):
    """
    MyCredentials class represents a username as an email address and password for logon to named external website.
    """
    username_as_email = models.EmailField()
    password = models.TextField()
    target_website = models.URLField()

    def __str__(self):
        return 'MyCredentials(username_as_email={0},password=\'Ask Matthew.\',target_website={1}'.format(self.username_as_email, self.target_website)

    def __repr__(self):
        return 'MyCredentials(username_as_email={0},password=\'Ask Matthew.\',target_website={1}'.format(self.username_as_email, self.target_website)

class USD(models.Model):
    """
    USD class represents the seven currency pairs for streaming US Dollar data from the subscription website datasource.
    """
    EURUSD = models.FloatField()
    GBPUSD = models.FloatField()
    USDJPY = models.FloatField()
    USDCAD = models.FloatField()
    USDCHF = models.FloatField()
    AUDUSD = models.FloatField()
    NZDUSD = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return 'EURUSD={0} GBPUSD={1} USDJPY={2} USDCAD={3} USDCHF={4} AUDUSD={5} NZDUSD={6} timestamp={7}'.format(
            EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF, AUDUSD, NZDUSD, timestamp
            )

    def __repr__(self):
        #timenow = datetime.datetime.now(tzlocal())
        time_field = datetime.datetime(timestamp, tzlocal())
        time_field = time_field.strftime('at %Y-%m-%d %H:%M:%S %Z')
        return 'EURUSD={0} GBPUSD={1} USDJPY={2} USDCAD={3} USDCHF={4} AUDUSD={5} NZDUSD={6} timestamp={7}'.format(
            EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF, AUDUSD, NZDUSD, '%s' % time_field
            )