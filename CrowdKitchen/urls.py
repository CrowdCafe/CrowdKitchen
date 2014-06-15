from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import router#, account_router

urlpatterns = patterns('',
	url(r'api/', include('api.urls')),
	url(r'admin/', include(admin.site.urls)),
	url(r'', include('social_auth.urls')),
	url(r'', include('kitchen.urls')),
    #url(r'api/', include('api.urls')),
    url(r'users/', include('account.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    )
