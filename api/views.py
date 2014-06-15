from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template import RequestContext

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, YAMLRenderer, JSONPRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings

from account.models import Account, Profile
from django.contrib.auth.models import User
from kitchen.models import Job, Task, DataUnit

from serializers import AccountSerializer, ProfileSerializer, UserSerializer
from rest_framework import routers


import requests

class AccountView(viewsets.ModelViewSet):
    """
    CRUD of Account
    """
    model = Account
    serializer_class = AccountSerializer

    def pre_save(self, obj):
        # init values
        user = self.request.user
        obj.creator = user

    # used to filter out based on the url
    def get_queryset(self):
        return Account.objects.filter(creator=self.request.user)

class UserView(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        log.debug("it's the list")
        log.debug("pk %s", self.kwargs['task_pk'])
        ''' this checks if the user owns the task, if so then the instances are displayed,
        if it's not his task then there's an exeception.
         it's a dirty way to do auth'''

        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def get_queryset(self):
        return Account.objects.get(pk=self.kwargs['account_pk']).users


router = routers.SimpleRouter()
router.register(r'account', AccountView)
#account_router = routers.NestedSimpleRouter(router, r'account', lookup='account')
#account_router.register(r'user', UserView)