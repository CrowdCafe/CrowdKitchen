# TODO - needs to be rewritten
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

import views
urlpatterns = patterns('',
    # -------------------------------------------------------------------------------
    # APPS
    url(r'accounts/(?P<account_pk>\d+)/apps/$', login_required(views.AppListView.as_view()), name='app-list'),
    url(r'accounts/(?P<account_pk>\d+)/apps/create/$', login_required(views.AppCreateView.as_view()), name='app-create'),
    url(r'apps/(?P<app_pk>\d+)/update/$', login_required(views.AppUpdateView.as_view()), name='app-update'),
    # -------------------------------------------------------------------------------
    # JOBS
    url(r'apps/(?P<app_pk>\d+)/jobs/$', login_required(views.JobListView.as_view()), name='job-list'),
    url(r'apps/(?P<app_pk>\d+)/jobs/create/$', login_required(views.JobCreateView.as_view()), name='job-create'),
    url(r'jobs/(?P<job_pk>\d+)/update/$', login_required(views.JobUpdateView.as_view()), name='job-update'),
    # -------------------------------------------------------------------------------
    # UNITS
    url(r'jobs/(?P<job_pk>\d+)/units/$', login_required(views.UnitListView.as_view()), name='unit-list'),
  )
