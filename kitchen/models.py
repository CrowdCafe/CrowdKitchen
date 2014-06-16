from django.db import models

from social_auth.models import UserSocialAuth
from datetime import datetime 
import jsonfield
from decimal import Decimal
from datetime import  timedelta

from django.contrib.auth.models import User
from account.models import Account, FundTransfer

from django.conf import settings

from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Sum

import requests
import json
import urllib2
import os
import binascii

from rest_framework.authtoken.models import Token


CATEGORY_CHOICES = (('CF','Espresso'),('CP','Cappuccino'),('WN','Wine'),('ZT','Volunteering')) #TODO need to bring this touples and dictionary in settings_common TASK_CATEGORIES to something in common

DEVICE_CHOISES = (('MO', 'Mobile only'), ('DO', 'Desktop only'), ('AD', 'Any device'))

# JOBS RELATED CLASSES:

class App(models.Model):
    account = models.ForeignKey(Account)
    creator = models.ForeignKey(User) # the one created the app
    token = models.CharField(max_length=40, blank = True)
    title = models.CharField(max_length=100)
    callback_url = models.URLField(unique=True) #ASK why do we need this callback
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20))
        return super(App, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)
    #def __unicode__(self):
    #    return '' + str(self.owner.username) + ' - ' + str(self.name) # TODO this should be redone according to accounts approach

JOB_STATUS_CHOISES = (('NP', 'Not published'), ('PB', 'Published'), ('DL', 'Deleted'))

class Job(models.Model):
    #general
    app = models.ForeignKey(App)
    creator = models.ForeignKey(User) # the one created the job
    title = models.CharField(max_length=255, default='New job')
    description = models.TextField()
    category = models.CharField(max_length=2, default='CF', blank=True)
    price = models.FloatField() # reward given to a worker per data_unit #ASK - is this name appropriate? wage/rate/cost/reward?
    status = models.CharField(max_length=2, choices=JOB_STATUS_CHOISES, default='NP')

    dataunits_per_page = models.IntegerField(default = 5)
    device_type = models.CharField(max_length=2, choices=DEVICE_CHOISES, default='AD')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    #other
    webhook_url = models.URLField(null = True, blank = True)
    
    #userinterface
    userinterface_url = models.URLField(null = True, blank = True)
    userinterface_html = models.TextField(null = True, blank = True)
    #make sure we do not have anly volnurabilities in userinterface_html
    def __unicode__(self):
        return str(self.id)
    def refreshUserInterface(self):
        try:
            self.userinterface_html = urllib2.urlopen(self.userinterface_url).read()
            self.save()
            return True
        except:
            return False

class QualityControl(models.Model):
    job = models.OneToOneField(Job)
    min_answers_per_dataunit = models.IntegerField(default = 1)
    max_dataunits_per_worker = models.IntegerField(default = 100) # Some limitation of amount of dataunits single worker can complete  
    def __unicode__(self):
        return str(self.id)

class GoldQualityControl(QualityControl):
    gold_min = models.IntegerField(default = 0, null = True)
    gold_max = models.IntegerField(default = 0, null = True)
    score_min = models.IntegerField(default = 0, null = True)
    qualitycontrol_url = models.URLField(null = True, blank = True)
    def __unicode__(self):
        return str(self.id)

DATAUNIT_STATUS_CHOISES = (('NC', 'Not completed'), ('CD', 'Completed'), ('DL', 'Deleted'))

class DataUnit(models.Model):
    job = models.ForeignKey(Job)
    input_data = jsonfield.JSONField()
    status = models.CharField(max_length=2, choices=DATAUNIT_STATUS_CHOISES, default = 'NC')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 

    def __unicode__(self):
        return str(self.id)

class GoldDataUnit(DataUnit):
    expected_data = jsonfield.JSONField()
    def __unicode__(self):
        return str(self.id)

# ANSWERS RELATED CLASSES

class Answer(models.Model):
    dataunit = models.ForeignKey(DataUnit, blank = True)
    output_data = jsonfield.JSONField(blank = True)
    score = models.FloatField(default = 0.0, null = True, blank = True)
    worker = models.ForeignKey(User, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        return str(self.id)
