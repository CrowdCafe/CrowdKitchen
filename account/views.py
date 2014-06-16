# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
import logging
from django.contrib.auth.models import User
from django.core.context_processors import csrf 
from forms import LoginForm, UserCreateForm, AccountForm
from models import Account, Profile
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect    

from rest_framework.authtoken.models import Token
from django.views.generic.list import ListView

log = logging.getLogger(__name__)

def register_user(request):
    template_name = 'kitchen/crispy.html'

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()

            user = authenticate(username=username,
                                password=password)
            profile = Profile(user = user)
            profile.save()
            account = Account(creator = user)
            account.save()
            account.users.add(user)
            account.save()

            login(request, user)
            return redirect('/')
        return render(request,
                      template_name,
                      { 'form' : user_form })
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    print args
    return render(request, template_name, args)

def login_user(request):
    template_name = 'kitchen/crispy.html'

    if request.method == 'POST':
        #TODO - need to fix this part
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print user
        if user is not None:
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            return redirect('/')           
        else:
            return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

class AccountListView(ListView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        return context

class AccountCreateView(CreateView):
    model = Account
    template_name = "kitchen/crispy.html"
    form_class = AccountForm

    def get_initial(self):
        initial = {}
        initial['creator'] = self.request.user
        return initial
    def form_invalid(self, form):
        log.debug("form is not valid")
        print (form.errors)
        return CreateView.form_invalid(self, form)
    
    def form_valid(self, form):
        log.debug("saved")
        account = form.save()
        account.users.add(self.request.user)
        account.save()

        return redirect(reverse('account-list'))
def logout_user(request):
	logout(request)
	return redirect('/')    