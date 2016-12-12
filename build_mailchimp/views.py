from django.shortcuts import render, HttpResponseRedirect
from MailChimp.MailChimp import Mailchimp
from team.views import email_id_list
from django.core.urlresolvers import reverse
# Create your views here.
def build_mailchimp(request):
    obj = Mailchimp(request)
    try:
        email_list = request.session['email_list']
    except Exception as e:
        print e
        print 'No Email List Found'
        return HttpResponseRedirect(reverse('dashboard'))
    del request.session['email_list']
    res = obj.send_list_to_mailchimp(email_list, 'Temporary', 'Amit', 'amit@tuple.tech')
    return render(request, 'build_mailchimp/index.html', {
        'res': res
    })