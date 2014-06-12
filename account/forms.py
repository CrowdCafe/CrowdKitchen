from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from crispy_forms.layout import Submit, Fieldset, Layout
from django import forms
from django.forms.forms import Form


class UserForm(Form):
    username = forms.CharField(label=(u'Username'))
    email = forms.EmailField(label=(u'Email'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(Fieldset('Create User', 'username', 'email', 'password'))
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That username is already taken, please select another.")


class LoginForm(Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Login'))
        # self.helper.action = self.helper.action + "?callback="+ kwargs['callback']
        super(LoginForm, self).__init__(*args, **kwargs)