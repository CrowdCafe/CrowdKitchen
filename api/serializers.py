# TODO - needs to be rewritten
from kitchen.models import App, Job

from django.contrib.auth.models import User
from account.models import Profile, Account
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    shortname = serializers.CharField(source='shortname', read_only=True)
    fullname = serializers.CharField(source='fullname', read_only=True)
    class Meta:
        model = Profile
        fields = ('id','shortname','fullname')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','profile')

class AccountSerializer(serializers.ModelSerializer):
    #creator = UserSerializer(many = False)
    #users = UserSerializer(many = True)
    
    class Meta:
		model = Account
		fields = ('id','title')