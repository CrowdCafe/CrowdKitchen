from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import create_user
from views import login, auth


import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    #url(r'^', include(router.urls)),
    url(r'^user/$',create_user),
    url(r'^login$',login,name='login'),
    url(r'^auth$',auth,name='auth'),
    url(r'^logout/', views.Logout, name='logout'),
)
