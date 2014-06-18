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
    
    #url(r'^auth/$',views.auth,name='auth'),
    url(r'^$',views.home),

    url(r'^user/login/$',views.login_user,name='login'),
    url(r'^user/register/$', views.register_user, name='register'),
    url(r'^user/logout/$', views.logout_user, name='logout'),
    

    url(r'^accounts/$', views.AccountListView.as_view(), name='account-list'),
    url(r'^accounts/create/$', views.AccountCreateView.as_view(), name='account-create'),
    url(r'^accounts/(?P<account_pk>\d+)/update/$', views.AccountUpdateView.as_view(), name='account-update'),

    url(r'^accounts/(?P<account_pk>\d+)/members/$', views.MembershipListView.as_view(), name='member-list'),
    url(r'^accounts/(?P<account_pk>\d+)/members/create/$', views.MembershipCreateView.as_view(), name='member-create'),
    url(r'^members/(?P<member_pk>\d+)/update/$', views.MembershipUpdateView.as_view(), name='member-update'),


)
