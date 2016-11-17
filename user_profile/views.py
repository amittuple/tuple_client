from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

def dashboard(request):
    print 'Start of Dashoard View'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'user_profile/dashboard.html', {})
