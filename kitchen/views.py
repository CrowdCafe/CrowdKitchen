# TODO - needs to be rewritten
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import App, Job, DataUnit, Answer
from account.models import Account

from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage

from forms import JobForm, AppForm

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

import logging

import re
import csv
import urllib2
import StringIO

log = logging.getLogger(__name__)

# -------------------------------------------------------------
# Apps
# -------------------------------------------------------------
class AppCreateView(CreateView):
	model = App
	template_name = "kitchen/crispy.html"
	form_class = AppForm

	def get_initial(self):
		initial = {}
		initial['creator'] = self.request.user
		initial['account'] = get_object_or_404(Account,pk = self.kwargs.get('account_pk', None))
		return initial
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		log.debug("saved")
		app = form.save()
		app.save()

		return redirect(reverse('app-list', kwargs={'account_pk': app.account.id}))

class AppUpdateView(UpdateView):
	model = App
	template_name = "kitchen/crispy.html"
	form_class = AppForm

	def form_invalid(self, form):
		log.debug("form is not valid")
		return UpdateView.form_invalid(self, form)
	def get_object(self):
		return get_object_or_404(App, pk = self.kwargs.get('app_pk', None), creator = self.request.user)
   	def form_valid(self, form):
		log.debug("updated")
		app = form.save()
		return redirect(reverse('app-list', kwargs={'account_pk': app.account.id}))

class AppListView(ListView):
	model = App
	template_name = "kitchen/job/app_list.html"
	def get_queryset(self):
		account = get_object_or_404(Account, pk = self.kwargs.get('account_pk', None), users__in = [self.request.user.id])
		return App.objects.filter(account = account)
	def get_context_data(self, **kwargs):
		context = super(AppListView, self).get_context_data(**kwargs)
		context['account'] = get_object_or_404(Account,pk = self.kwargs.get('account_pk', None))
		return context
# -------------------------------------------------------------
# Jobs
# -------------------------------------------------------------
class JobCreateView(CreateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm

	def get_initial(self):
		initial = {}
		initial['creator'] = self.request.user
		initial['app'] = get_object_or_404(App,pk = self.kwargs.get('app_pk', None))
		return initial
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		print form.errors
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		log.debug("saved")
		job = form.save()
		job.save()

		return redirect(reverse('job-list', kwargs={'app_pk': job.app.id}))

class JobUpdateView(UpdateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		return UpdateView.form_invalid(self, form)
	def get_object(self):
		return get_object_or_404(Job, pk = self.kwargs.get('job_pk', None), creator = self.request.user)
	def form_valid(self, form):
		log.debug("updated")
		job = form.save()
		return redirect(reverse('job-list', kwargs={'app_pk': job.app.id}))

class JobListView(ListView):
	model = Job
	template_name = "kitchen/job/job_list.html"
	
	def get_queryset(self):
		app = get_object_or_404(App, pk = self.kwargs.get('app_pk', None), account__users__in = [self.request.user.id])
		return Job.objects.filter(app = app)

	def get_context_data(self, **kwargs):
		context = super(JobListView, self).get_context_data(**kwargs)
		context['app'] = get_object_or_404(App,pk = self.kwargs.get('app_pk', None))
		return context