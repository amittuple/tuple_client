from dashboard.views import dashboard
from .from_view_to_output import bot_user
from .team_input import chat_input
from build_mailchimp.views import *
from banana_py import Bananas_OAuth
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from slack_bot.models import email_list_for_slack_1
from .models import chat_store
import json
import time
from .function_input import replace_operator_like_gt_lt_eq_in_standard_format,convert_unicode_to_string,conevert_string_in_integer,changetoint
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
# def visit(request, req):
#     # go in to the team_input
#     input_from_tuple_mia=chat_input(req)
#     if input_from_tuple_mia==[u'send',u'mailchimp']:
#         to_mailchimp()
#     else:
#         # go into from_view_to_output
#         input_amit=bot_user(request,input_from_tuple_mia)
#         # final output
#         return HttpResponse(input_amit)
#amit integ

#integrate
def visit(request, req):
    try:
        # go in to the team_input
        input_from_tuple_mia=chat_input(req)
        # store input in chat
        store_table  =  replace_operator_like_gt_lt_eq_in_standard_format(input_from_tuple_mia)
        store_input  =  convert_unicode_to_string(store_table)
        store_input_11 =  changetoint(store_input)
        store_input_1 =  conevert_string_in_integer(store_input_11)
        obj_chat = chat_store()
        obj_chat.chat_sendby = "user"
        obj_chat.chat_message = store_input_1
        obj_chat.chat_time = time.ctime()
        obj_chat.save()
        if input_from_tuple_mia == [u'mailchimp']:
            to_mailchimp(request)
        else:
            # go into from_view_to_output
            input_amit=bot_user(request,input_from_tuple_mia)
            # final output
            return HttpResponse(input_amit)
    except Exception as e:
        print e
        return HttpResponse('Sorry! Some Error Occured Please Try Again Later.')

def chat_view(request):
    obj_chat = chat_store.objects.all()
    if len(obj_chat)!=0:
        empty_list=[]
        for x in obj_chat:
            m = {
                'send_by':x.chat_sendby,
                'time'   : x.chat_time,
                'message':x.chat_message
                 }
            empty_list.append(m.copy())
        json_string = json.dumps(empty_list)
        return HttpResponse(json_string, content_type='application/json')
    else:
        empty_list = []
        amit_time = time.ctime()
        print amit_time
        m = {
            'send_by': "bot",
            'time': amit_time,
            'message': "Welcome to Tuple MIA. Write Something... "
        }
        empty_list.append(m.copy())
        json_string = json.dumps(empty_list)
        return HttpResponse(json_string, content_type='application/json')