from django import forms
from datetime import date, timedelta
from models import App, Job, Task, DataUnit, Answer
from account.models import Account

from models import JOB_STATUS_CHOISES
from django.conf import settings

from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout

import logging
from decimal import Decimal
from django.utils.datetime_safe import datetime
from django.forms.forms import Form
from django.forms.fields import FileField
from utils import getGithubRepositoryFiles

log = logging.getLogger(__name__)

class JobForm(ModelForm):
	owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	app = forms.ModelChoiceField(queryset=App.objects.all(), widget=forms.HiddenInput)

	title = forms.CharField(label=(u'Title')) # ??? what is the difference between (u'Title') and 'Title'?
	description = forms.CharField(label=(u'Description'), widget=forms.Textarea())
	webhook_url = forms.URLField(label='Webhook', required=False)
	status = forms.ChoiceField(choices=JOB_STATUS_CHOISES, widget=forms.Select(), initial = 'NP', label=(u'Status'), required=False)
	category = forms.ChoiceField(choices=settings.TASK_CATEGORIES_DICTIONARY, initial = 'ZT', widget=forms.Select(), label=(u'Category'), required=False)
	userinterface_url = forms.URLField(label='UserInterface url', required=False)
	
	class Meta:
		model = Job
		exclude = ('date_deadline','date_created','template_html')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		self.helper.layout = Layout(Fieldset('Job','title', 'description','userinterface_url','category','status','webhook_url','owner','app'))
		super(JobForm, self).__init__(*args, **kwargs)

class AppForm(ModelForm):
	owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput)

	class Meta:
		model = App
		exclude = ('date_created','token')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		self.helper.layout = Layout(Fieldset('Application','title', 'callback_url','owner','account'))
		super(AppForm, self).__init__(*args, **kwargs)