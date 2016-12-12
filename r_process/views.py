from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

def process(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    try:
        if not request.session['run_r_process']:
            return
    except Exception as e:
        print e
        return
    return render(request, '', {})
