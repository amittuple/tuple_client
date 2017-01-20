from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from . import forms
from django.contrib.auth.models import User
from user_profile.models import MembersList
from custom_django_library.Demo import Demo


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
            try:
                if username == 'demo' and password == 'investor':
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
                else:
                    return HttpResponseRedirect(reverse('login'))

            except Exception as e:
                print e
                return HttpResponseRedirect(reverse('login'))

    return render(request, 'login/index.html', {
        'form': form
    })


def logout_user(request):
    # To Clean Everything
    # Demo().clean_all()
    logout(request)
    return HttpResponseRedirect(reverse('login'))



def is_admin(user):
    return MembersList.objects.get(member=user).is_admin