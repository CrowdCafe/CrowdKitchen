# TODO - needs to be rewritten
from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^', include(views.router.urls)),
    #url(r'token/$', views.home, name='api-home'),
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    #url(r'user/$', views.getUser, name='api-user'),
)
