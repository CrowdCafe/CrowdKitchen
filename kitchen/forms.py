from django import forms
from datetime import date, timedelta
from models import App, Job
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

log = logging.getLogger(__name__)

class JobForm(ModelForm):
	creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	app = forms.ModelChoiceField(queryset=App.objects.all(), widget=forms.HiddenInput)
	
	class Meta:
		model = Job
		exclude = ('deleted','date_deadline','date_created')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(JobForm, self).__init__(*args, **kwargs)

class AppForm(ModelForm):
	creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput)

	class Meta:
		model = App
		exclude = ('deleted','token')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(AppForm, self).__init__(*args, **kwargs)
		