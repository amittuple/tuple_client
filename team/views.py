from dashboard.views import dashboard
from .from_view_to_output import bot_user
from .team_input import chat_input
from build_mailchimp.views import *
from banana_py import Bananas_OAuth
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from slack_bot.models import email_list_for_slack_1

#  goto mailchimp.. if press /send in chatbot....
def to_mailchimp(request):
    print "to_mail chimp"

    try:
        email_mail = email_list_for_slack_1.objects.all()[0]
        if eval(email_mail.email_list_slack):
            # print request.session['email_list']
            pass
    except Exception as e:
        print e
        print 'No Email List Found'
        return HttpResponseRedirect(reverse(dashboard))
    return HttpResponseRedirect(u'%s' % (Bananas_OAuth().authorize_url()))

# this is use for the printing template in browser....
def ins(request):
    return render(request, 'html/index.html', {})

#  firstly input come here from the tuple-mia....
# tuple_mia
def visit(request, req):
    # go in to the team_input
    input_from_tuple_mia=chat_input(req)
    if input_from_tuple_mia==[u'send',u'mailchimp']:
        to_mailchimp()
    else:
        # go into from_view_to_output
        input_amit=bot_user(request,input_from_tuple_mia)
        # final output
        return HttpResponse(input_amit)