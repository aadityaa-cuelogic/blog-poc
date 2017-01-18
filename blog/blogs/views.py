from django.shortcuts import render, render_to_response

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from blogs.forms import RegistrationForm
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, "home.html")

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # return HttpResponse("You're looking at question %r" % form)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
        else:
            context = {'form':form }
            return render(request, 'register.html', context)

    else:
        context = {'form':RegistrationForm() }
        return render(request, 'register.html', context)

def register_success(request):
    return render_to_response('register_success.html', )
