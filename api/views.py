import json
import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import routers, viewsets, status
from rest_framework import exceptions

from api.serializers import JobSerializer, Appserializer
from kitchen.models import Job, App, Unit
from serializers import UserSerializer


log = logging.getLogger(__name__)

# class AccountView(viewsets.ModelViewSet):
#     """
#     CRUD of Account
#     """
#     model = Account
#     serializer_class = AccountSerializer
#
#     def pre_save(self, obj):
#         # init values
#         user = self.request.user
#         obj.creator = user
#
#     # used to filter out based on the url
#     def get_queryset(self):
#         return Account.objects.filter(creator=self.request.user)
#
# class UserView(viewsets.ModelViewSet):
#     model = User
#     serializer_class = UserSerializer
#
#     def list(self, request, *args, **kwargs):
#         log.debug("it's the list")
#         log.debug("pk %s", self.kwargs['task_pk'])
#         ''' this checks if the user owns the task, if so then the instances are displayed,
#         if it's not his task then there's an exeception.
#          it's a dirty way to do auth'''
#
#         return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
#
#     def get_queryset(self):
#         return Account.objects.get(pk=self.kwargs['account_pk']).users

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def me(request):
    user_serilized = UserSerializer(request.user)
    return Response(user_serilized.data)


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    for the app, only readonly
    '''
    model = App
    serializer_class = Appserializer

    def get_queryset(self):
        #  the job of the user with the requested app
        return App.objects.filter(account__in=self.request.user.account_set.all())


class JobsViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    model = Job
    paginate_by = 10

    def get_queryset(self):
        #  the job of the user with the requested app
        # ASK: filtering only by app?
        return Job.objects.filter(app=self.request.app)

    def create(self, request):
        # disable this function
        raise exceptions.MethodNotAllowed('CREATE')

    def destroy(self, request, pk=None):
        # disable this function
        raise exceptions.MethodNotAllowed('DESTROY')

    # move this inside data unit (that should be subclass of JOB)
    @action()
    def update_unit(self, request, pk=None):
        job = get_object_or_404(Job, pk=pk, app=self.request.app)
        input = self.request.DATA
        units_id = []
        # it expect an array
        for d in input:
            du = Unit.objects.create(job=job, input_data=json.dumps(d))
            units_id.append(du.pk)
        # TODO: check if it converst units to array in json.
        return Response(units_id, status=status.HTTP_201_CREATED)


router = routers.SimpleRouter()
router.register(r'app', AppViewSet)
router.register(r'jobs', JobsViewSet)
#account_router = routers.NestedSimpleRouter(router, r'account', lookup='account')
#account_router.register(r'user', UserView)