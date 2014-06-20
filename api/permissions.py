'''
This file contains the permission rules for the api.

'''

__author__ = 'stefano'


import logging

from rest_framework.permissions import SAFE_METHODS


from rest_framework import permissions


log = logging.getLogger(__name__)


class IsOwner(permissions.BasePermission):
    '''
        check if user is owner of the object
    '''
    def has_permission(self, request, view, obj=None):
        # log.debug("check permission")
        #if it's a task instance check ownership of the task
        if obj is None:
            # log.debug("obj is none")
            return True
        elif hasattr(obj, 'task'):
            # log.debug('is an instance')
            # log.debug("%s %s" % (obj.task.owner, request.user))
            return obj.task.owner == request.user and obj.task.app == request.app
        #if it's a task check ownership
        elif hasattr(obj, 'owner'):
            # log.debug('is a task')
            return obj.owner == request.user and obj.app == request.app
        else:
            log.debug('is smt else')
            return False


class IsExecutor(permissions.BasePermission):
    '''
    check if user is worker of the object.
    '''
    def has_object_permission(self, request, view, obj):
        #if it's a task instance check ownership of the task
        if hasattr(obj, 'executor'):
            return obj.task.executor == request.user
        else:
            return False


# class IsFromApp(permissions.BasePermission):
#     def has_permission(self, request, view, obj=None):
#         if request.method in SAFE_METHODS:
#             return True
#         apptoken = request.app.token
#         if apptoken is None:
#             return False
#         try:
#             pass
#             #     enable this
#             #     App.objects.get(token=apptoken,owner=request.user)
#             return True
#         except Exception as e:
#             return False