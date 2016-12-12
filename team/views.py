from .Universal_function_master import *
from .function_two_table import A12
from django.http import HttpResponse
from build_mailchimp.views import *
from banana_py import Bananas_OAuth

#  goto mailchimp.. if press /send in chatbot....
def to_mailchimp(request):
    print "to_mail chimp"
    print request
    try:
        if request.session['email_list']:
            print request.session['email_list']
            print "OK"
            pass
    except Exception as e:
        print e
        print 'No Email List Found'
        return HttpResponseRedirect(reverse('dashboard'))
    return HttpResponseRedirect(u'%s' % (Bananas_OAuth().authorize_url()))

# this is use for the printing template in browser....
def ins(request):
    return render(request, 'html/index.html', {})

#  firstly input come here from the tuple-mia....
def visit(request, req):
    list_come_from_user_convert = req.split("-")
    list_from_user_to_lowercase=convert_all_string_to_lower_case(list_come_from_user_convert)
    list_from_user=input_comes_from_user(list_from_user_to_lowercase)

    if list_from_user[0] == '/send':
        print "/send available from user"
        return HttpResponseRedirect(reverse('to_mailchimp'))

    else:
        check_slash_filter_from_user = input_comes_from_user(list_from_user)
        got_string = get_string(check_slash_filter_from_user)
        got_string_12 = A12(got_string, request)

        Study = Standard(got_string_12)
        email = email_id_list(Study)
        request.session['email_list'] = email

        return HttpResponse("your data has been store if you want to send email_id to mailchimp then press '/send' in tuple-mia")