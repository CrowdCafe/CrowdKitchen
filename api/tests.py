"""
This file is the test case for the API.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from account.models import Account, Membership
from kitchen.models import App, Job


class AccountTests(APITestCase):
    '''
    testing the account
    '''

    def setUp(self):
        '''
         setup the enviroment
        '''
        User.objects.create(username='test', password='test', email="test@test.com")
        self.user = User.objects.get(username='test')
        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_me(self):
        """
        Ensure that a user can retrive his data
        """
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AppTests(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        User.objects.create(username='test', password='test', email="test@test.com")
        self.user = User.objects.get(username='test')
        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=self.account)
        app = App.objects.create(account=self.account, creator=self.user, title='test')

        token = 'Token ' + token.key + '/' + app.token
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_list(self):
        App.objects.create(account=self.account, creator=self.user, title='test 2')
        url = reverse('app-list')
        response = self.client.get(url)
        # check if the list has 1 element
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


        # check if the data are the same

    def test_detail(self):
        url = reverse('app-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        self.assertEqual(response.data, {"title": "test", "account": "test", "creator": "test"})


class JobTests(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        User.objects.create(username='test', password='test', email="test@test.com")
        self.user = User.objects.get(username='test')
        token = Token.objects.get(user=self.user)
        self.client = APIClient()

        account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=account)
        self.app = App.objects.create(account=account, creator=self.user, title='test')

        token = 'Token ' + token.key + '/' + self.app.token
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_list(self):
        Job.objects.create(app=self.app, creator=self.user, title='job title 1',
                           description='job desc', category='CF', dataunits_per_page='2', device_type='AD',
                           webhook_url='http://example.com', userinterface_url="http://example.com/ui/")
        Job.objects.create(app=self.app, creator=self.user, title='job title 2',
                           description='job desc', category='CF', dataunits_per_page='2', device_type='AD',
                           webhook_url='http://example.com', userinterface_url="http://example.com/ui/")
        url = reverse('job-list')
        response = self.client.get(url)
        # check if the list has 1 element
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_detail(self):
        Job.objects.create(app=self.app, creator=self.user, title='job title 2',
                           description='job desc', category='CF', dataunits_per_page='2', device_type='AD',
                           webhook_url='http://example.com', userinterface_url="http://example.com/ui/")
        url = reverse('job-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        # check if the list has 1 element
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'job title 2')

        # self.assertEqual(len(response.data), 2)

#
#
# class DataUnitTests(APITestCase):
#     pass
