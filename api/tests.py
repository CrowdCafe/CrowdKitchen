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
        self.app = App.objects.create(account=self.account, creator=self.user, title='test')

        token = 'Token ' + token.key + '/' + self.app.token
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
        # mine: 200
        url = reverse('app-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"title": "test", "account": "test", "creator": "test"})

        # someone else trying to access mine
        client = APIClient()
        # another user SAME APP: OK
        user = User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '/' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #someoneelse : 404
        url = reverse('app-detail', kwargs={'pk': 2})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobTests(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        self.user =User.objects.create(username='test', password='test', email="test@test.com")
        # self.user
        token = Token.objects.get(user=self.user)
        self.client = APIClient()

        self.account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=self.account)
        self.app = App.objects.create(account=self.account, creator=self.user, title='test')

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
        self.assertGreater(len(response.data), 0)

    def test_detail(self):
        # create a job to test
        Job.objects.create(app=self.app, creator=self.user, title='job title 2',
                           description='job desc', category='CF', dataunits_per_page='2', device_type='AD',
                           webhook_url='http://example.com', userinterface_url="http://example.com/ui/")
        url = reverse('job-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'job title 2')

        # unexisting or of someone else: 404
        url = reverse('job-detail', kwargs={'pk': 2})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # setting back the correct url
        url = reverse('job-detail', kwargs={'pk': 1})
        client = APIClient()
        # another user SAME APP: OK
        user = User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '/' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # another user, another app: 404
        user = User.objects.create(username='test3', password='test3', email="test@test.com")
        account = Account.objects.create(title='test2', creator=user)
        Membership.objects.create(user=user, account=account)
        token = Token.objects.get(user=user)
        app = App.objects.create(account=account, creator=user, title='test4')
        token = 'Token ' + token.key + '/' + app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_create(self):
        # create not allowed : 405
        url = reverse('job-list')
        data = {'app': self.app.pk, 'creator': self.user.pk, 'title': 'api creation', 'description': 'api'}
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_add_data_unit(self):
        Job.objects.create(app=self.app, creator=self.user, title='job title 2',
                           description='job desc', category='CF', dataunits_per_page='2', device_type='AD',
                           webhook_url='http://example.com', userinterface_url="http://example.com/ui/")

        # add to a create Job: 201
        url = reverse('job-update-dataunit', kwargs={'pk': 1})
        # first element is an array
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(len(response.data),3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # add to an unexisting Job: 404
        url = reverse('job-update-dataunit', kwargs={'pk': 2})
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        client = APIClient()
        #  Another user, same APP: 201
        user =User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '/' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        url = reverse('job-update-dataunit', kwargs={'pk': 1})
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = client.post(url, data=data,format='json')
        self.assertEqual(len(response.data),3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Another user, different APP: 404
        user = User.objects.create(username='test4', password='test4', email="test@test.com")
        account = Account.objects.create(title='test4', creator=user)
        Membership.objects.create(user=user, account=account)
        token = Token.objects.get(user=user)
        app = App.objects.create(account=account, creator=user, title='test4')
        token = 'Token ' + token.key + '/' + app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        url = reverse('job-update-dataunit', kwargs={'pk': 1})
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
