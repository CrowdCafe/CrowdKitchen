from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import router#, account_router
admin.autodiscover()

urlpatterns = patterns('',
	url(r'api/', include('api.urls')),
	url(r'', include('social_auth.urls')),

    #url(r'api/', include('api.urls')),
    url(r'', include('account.urls')),
    url(r'', include('kitchen.urls')),
    url(r'admin/', include(admin.site.urls)),


    )
