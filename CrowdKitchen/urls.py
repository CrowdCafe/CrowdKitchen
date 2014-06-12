from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'', include('kitchen.urls')),
    url(r'api/', include('api.urls')),
    url(r'user/', include('account.urls')),
    )
