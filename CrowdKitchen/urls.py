from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import router#, account_router

urlpatterns = patterns('',
	url(r'api/', include('api.urls')),
	url(r'admin/', include(admin.site.urls)),
	url(r'', include('social_auth.urls')),

    #url(r'api/', include('api.urls')),
    url(r'', include('account.urls')),
    url(r'', include('kitchen.urls')),

    )
