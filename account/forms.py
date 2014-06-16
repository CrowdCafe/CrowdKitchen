from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from crispy_forms.layout import Submit, Fieldset, Layout, Button, HTML
from django import forms
from models import Profile, Account
from django.forms.forms import Form
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

#NOTICE We need to use these forms https://github.com/django/django/blob/master/django/contrib/auth/forms.py

class UserCreateForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.form_class = 'form-vertical'

        super(UserCreateForm, self).__init__(*args, **kwargs)

class AccountForm(ModelForm):
    creator = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Account
        exclude = ('users','total_earnings','total_spendings')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Save'))
        # self.helper.action = self.helper.action + "?callback="+ kwargs['callback']
        super(AccountForm, self).__init__(*args, **kwargs)

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-vertical'
        self.helper.add_input(Submit('submit', 'Login'))
        # self.helper.action = self.helper.action + "?callback="+ kwargs['callback']
        super(LoginForm, self).__init__(*args, **kwargs)