from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from . import forms
def index(request):
    form = forms.LoginForm()
    print 'Start of Login View'
    if request.user.is_authenticated:
        print 'Goto Dashoard View'
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        print 'Incorrect Credentials'
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            print username
            print password
            user = authenticate(username=username, password=password)
            print user
            if user is not None:
                login(request, user)
                print 'Logged in successfully'
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                # Wrong Credentials
                print 'Wrong Credentials'
                return HttpResponseRedirect(reverse('login'))
    return render(request, 'login/index.html', {
        'form': form
    })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
