# from django.shortcuts import render, HttpResponseRedirect
# from MailChimp.MailChimp import Mailchimp
# from team.views import email_id_list
# from django.core.urlresolvers import reverse
# # Create your views here.
# def build_mailchimp(request):
#     obj = Mailchimp(request)
#     try:
#         email_list = request.session['email_list']
#     except Exception as e:
#         print e
#         print 'No Email List Found'
#         return HttpResponseRedirect(reverse('dashboard'))
#     del request.session['email_list']
#     res = obj.send_list_to_mailchimp(email_list, 'Temporary', 'Adnan', 'adnan@tuple.tech')
#     print 'res'
#     print res['id']
#     create_campaign = obj.create_campaign_from_list(res['id'], 'Adnan', 'adnan@tuple.tech')
#     print 'create_campaign'
#     print create_campaign
#     return render(request, 'build_mailchimp/index.html', {
#         'res': res,
#         'create_campaign': create_campaign
#     })


from django.shortcuts import render, HttpResponseRedirect
from MailChimp.MailChimp import Mailchimp
from slack_bot.models import email_list_for_slack_1
from django.core.urlresolvers import reverse
def build_mailchimp(request):
    obj = Mailchimp(request)
    try:
        email_mail = email_list_for_slack_1.objects.all()[0]
        mail_email=eval(email_mail.email_list_slack)

    except Exception as e:
        print e
        print 'No Email List Found'
        return HttpResponseRedirect(reverse('dashboard'))
    # remove email form the data base ......
    email_list_for_slack_1.objects.all().delete()

    res = obj.send_list_to_mailchimp(mail_email, 'Temporary', 'Amit', 'amit@tuple.tech')
    return render(request, 'build_mailchimp/index.html', {
        'res': res
    })