#!/usr/bin/env python
#coding: utf8 
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


CATEGORY_CHOICES (('CF','Espresso'),('CP','Cappuccino'),('WN','Wine'),('ZT','Volunteering')) # TODO need to bring this touples and dictionary in settings_common TASK_CATEGORIES to something in common
DEVICE_CHOISES = (('MO', 'Mobile only'), ('DO', 'Desktop only'), ('AD', 'Any device'))


def getPlatformOwner():
    return User.objects.filter(pk = settings.BUSINESS['platform_owner_id']).get()
    
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']

# JOBS RELATED CLASSES:

class App(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    token = models.CharField(max_length=40, primary_key=True)
    title = models.CharField(max_length=100, default="-")
    callback = models.URLField(unique=True) # ??? why do we need this callback
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20))
        return super(App, self).save(*args, **kwargs)

    def __unicode__(self):
        return '' + str(self.owner.username) + ' - ' + str(self.name) # TODO this should be redone according to accounts approach

JOB_STATUS_CHOISES = (('NP', 'Not published'), ('PB', 'Published'), ('DL', 'Deleted'))

class Job(models.Model):
    #general
    app = models.ForeignKey(App)
    title = models.CharField(max_length=255, default='New task')
    description = models.CharField(max_length=1024, default='***')
    category = models.CharField(max_length=2, default='CF', blank=True)
    status = models.CharField(max_length=2, choices=JOB_STATUS_CHOISES, default='NP')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    
    #userinterface
    userinterface_url = models.URLField(null = True, blank = True) # ??? I think that this can be skipped - and just become a part of job creation
    userinterface_html = models.TextField(null = True, blank = True)
    
    #qualitycontrol
    gold_min = models.IntegerField(default = 0, null = True)
    gold_max = models.IntegerField(default = 0, null = True)
    score_min = models.IntegerField(default = 0, null = True)
    dataunits_per_task = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)
    max_dataunits_per_worker = models.IntegerField(default = 100) # ??? TODO Some limitation of amount of dataunits single worker can complete  
    device_type = models.CharField(max_length=2, choices=DEVICE_CHOISES, default='AD')
    qualitycontrol_url = models.URLField(null = True, blank = True)

    #other
    webhook_url = models.URLField(null = True, blank = True)
    
    def refreshUserInterface(self):
        try:
            self.userinterface_html = urllib2.urlopen(self.userinterface_url).read()
            self.save()
            return True
        except:
            return False

DATAUNIT_STATUS_CHOISES = (('NC', 'Not completed'), ('CD', 'Completed'), ('DL', 'Deleted'))

class DataUnit(models.Model):
    job = models.ForeignKey(Job)
    value = jsonfield.JSONField()
    gold = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=DATAUNIT_STATUS_CHOISES, default = 'NC')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 

    def __unicode__(self):
        return str(self.id)

# ANSWERS RELATED CLASSES
TASK_STATUS_CHOISES = (('NC', 'Not completed'), ('CD', 'Completed'), ('DL', 'Deleted'))

class Task(models.Model):
    job = models.ForeignKey(Job)
    user = models.ForeignKey(User, blank = True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)


class Answer(models.Model):
    task = models.ForeignKey(Task)
    datanit = models.ForeignKey(DataUnit, blank = True)
    value = jsonfield.JSONField(blank = True)
    score = models.FloatField(default = 0.0, null = True, blank = True)

    def __unicode__(self):
        return str(self.id)
