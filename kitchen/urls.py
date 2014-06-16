# TODO - needs to be rewritten
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    #url(r'apps/$', login_required(views.AppListView.as_view()), name='app-list'),
    #url(r'apps/create/$', login_required(views.AppCreateView.as_view()), name='app-create'),
    #url(r'apps/(?P<pk>\d+)/update/$', login_required(views.AppUpdateView.as_view()), name='app-update'),

    url(r'jobs/$', login_required(views.JobListView.as_view()), name='job-list'),
    url(r'jobs/create/$', login_required(views.JobCreateView.as_view()), name='job-create'),
    url(r'jobs/(?P<pk>\d+)/update/$', login_required(views.JobUpdateView.as_view()), name='job-update'),


  )
