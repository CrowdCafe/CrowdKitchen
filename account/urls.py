from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required


import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    #url(r'^', include(router.urls)),
    #url(r'^user/$',create_user),
    url(r'^login/$',views.login_user,name='login'),
    #url(r'^auth/$',views.auth,name='auth'),
    url(r'^create/$', views.register_user, name='user-register'),
    url(r'^logout/', views.logout_user, name='logout'),
)
