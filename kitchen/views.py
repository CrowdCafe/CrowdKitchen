# TODO - needs to be rewritten
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Job, Task, DataItem, Attachment, Answer
from qualitycontrol.models import QualityControl
from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage

from forms import JobForm,QualityControlForm

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

import logging

import re
import csv
import urllib2
import StringIO
import scraperwiki 

log = logging.getLogger(__name__)

from utils import getGithubRepositoryFiles, saveDataItems, collectDataFromCSV,collectDataFromSocialNetwork,collectDataFromTwitter,simplifyInstagramDataset,collectDataFromInstagram

def JobDataUpload(request, pk):
	job = get_object_or_404(Job,pk = pk, owner =request.user)

	# -----------------------
	# Input dataset
	# -----------------------
	dataset = []
	if 'dataset_option_selected' in request.POST:
		dataset_option = request.POST['dataset_option_selected']
		if dataset_option == 'survey':
			dataset = [{'no data':'survey'}]
		elif dataset_option == 'dataset':
			if request.FILES:
				if 'dataset' in request.FILES:
				
					dataset_file = Attachment(job = job)
					dataset_file.file.save(str(job.id)+request.FILES['dataset'].name, request.FILES['dataset'])
					dataset_file.save()
					
					dataset = collectDataFromCSV(dataset_file.file.url)
		
		elif dataset_option == 'feed' and request.POST['feed_handler'] and request.POST['feed_amount'] and request.POST['feed-type']:	
			keyword = request.POST['feed_handler']
			amount = int(request.POST['feed_amount'])
			feed_type = int(request.POST['feed-type'])
			if feed_type == 0: # Twitter
				dataset = collectDataFromTwitter(keyword, amount)
			if feed_type == 2: # Instagram
				dataset = simplifyInstagramDataset(collectDataFromInstagram(keyword, amount))
	
		saveDataItems(job,dataset)
	return redirect(reverse('kitchen-job-data', kwargs={'pk': job.id}))

class JobCreation(CreateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm
	print 1

	def get_initial(self):
		initial = {}
		initial['owner'] = self.request.user
		return initial
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		print (form.errors)
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		log.debug("saved")
		job = form.save()
		job.save()
		job.refresh_template()
		quality = QualityControl(job = job)
		quality.save()

		return redirect(reverse('kitchen-job-data', kwargs={'pk': job.id}))

class JobUpdate(UpdateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm

	def get_initial(self):
		initial = {}
		initial['owner'] = self.request.user
		return initial

	def get_success_url(self):
		return reverse_lazy('kitchen-home')
	def form_invalid(self, form):
		log.debug("form is not valid")
		print (form.errors)
		return UpdateView.form_invalid(self, form)
	def get_queryset(self):
		return Job.objects.filter(pk=self.kwargs.get('pk', None),owner = self.request.user) # or request.POST
	def form_valid(self, form):
		log.debug("updated")
		job = form.save()
		job.refresh_template()
		return HttpResponseRedirect(self.get_success_url())

