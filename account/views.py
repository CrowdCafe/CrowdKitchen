# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
import logging
from forms import LoginForm

log = logging.getLogger(__name__)

def Logout(request):
	logout(request)
	return redirect('/')

def login(request):
    # if request.user.is_authenticated():
    #     return redirect('/')
    callback = request.GET.get('callback', '')
    if not callback.endswith("/"):
        callback=callback+"/"
    log.debug("callback %s",callback)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_app = user.crowduser.auth_apps.all()
                try:
                    app = App.objects.get(callback=callback)
                except Exception:
                    raise Http404
                token = Token.objects.get(user=user)

                if app not in auth_app:
                    log.debug("not in app")
                    return redirect(reverse(auth)+"?callback="+callback+"&token="+token.key)
                else:
                    log.debug("in app")
                # log.debug("Username %s",user.username)
                # get the app
                # apptoken = request.META.get('HTTP_AUTHORIZATION', b'')
                callback = request.GET.get('callback', '')
                if type(callback) == type(''):
                    raise Http404
                token = Token.objects.get(user=user)
                redirect_to = callback+"?token="+token.key
                return HttpResponseRedirect(redirect_to)
            else:
                messages.info(request,'username and password not valid')


                form.helper.form_action = reverse('login') + '?callback=' + callback
                render_to_response('ui/login.html',  {'form': form}, context_instance=RequestContext(request))
        else:
            form.helper.form_action = reverse('login') + '?callback=' + callback

            render_to_response('ui/login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        form.helper.form_action = reverse('login') + '?callback=' + callback
        # context = {'form': form,'callback':callback}
        # context = {}
        return render_to_response('kitchen/crispy.html',  {'form': form}, context_instance=RequestContext(request))

def auth(request):
    callback = request.GET.get('callback', '')
    token = request.GET.get('token', '')
    if not callback.endswith("/"):
        callback=callback+"/"
    if request.method == 'POST':
        token = Token.objects.get(key=token)
        app = App.objects.get(callback=callback)
        crowduser = token.user.crowduser
        crowduser.auth_apps.add(app)
        crowduser.save()
        redirect_to = callback+"?token="+token.key+"&id="+crowduser.user.pk
        return HttpResponseRedirect(redirect_to)
    else:
        app = App.objects.get(callback=callback)
        return render_to_response('kitchen/crispy.html',  {'app': app,'callback':callback,'token':token}, context_instance=RequestContext(request))