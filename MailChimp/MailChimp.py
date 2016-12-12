from django.shortcuts import render
from requests.auth import HTTPBasicAuth
import requests
import json
import simplejson

class Mailchimp:
    def __init__(self, request):
        try:
            self.api_endpoint = request.session['mailchimp_details']['api_endpoint']
            self.base_url = self.api_endpoint+'/3.0/'
            self.api_key = request.session['mailchimp_details']['access_token'] + '-' + request.session['mailchimp_details']['dc']
            self.usern = request.session['mailchimp_details']['login']['login_name']
            self.auth = HTTPBasicAuth(self.usern, self.api_key)
            self.list_url = self.base_url + 'lists'
        except Exception as e:
            print e
            print 'Bad Mailchimp Configuration'

    def get_all_list(list_url, auth):
        try:
            # get list
            res = requests.get(list_url, auth=auth)
            js = json.dumps(res.json())
            # print js
            return js
        except Exception as e:
            print e
            return None

    def add_list(self, list_name, sender_name, sender_email):
        try:
            data = {
                "name":list_name,
                "contact":{
                    "company":"Tuple Technologies",
                    "address1":"675 Ponce De Leon Ave NE",
                    "address2":"Suite 5000",
                    "city":"Atlanta",
                    "state":"GA",
                    "zip":"30308",
                    "country":"US",
                    "phone":""
                },
                "permission_reminder":"Youre receiving this email because you signed up for updates about Freddies newest hats.",
                "campaign_defaults":{
                    "from_name": sender_name,
                    "from_email": sender_email,
                    "subject":"",
                    "language":"en"
                },
                "email_type_option":True
            }
            res = requests.post(self.list_url, auth=self.auth, data=json.dumps(data))
            js = json.dumps(res.json())
            # print js
            return js
        except Exception as e:
            print e
            return None

    def add_member_to_list(self, list_id, email, status):
        try:
            data = {
                "email_address": email,
                "status": status
            }
            # print list_id
            # print data
            # print list_url+'/'+list_id+'/'+'members'
            res = requests.post(self.list_url+'/'+list_id+'/'+'members', auth=self.auth, data=json.dumps(data))
            js = json.dumps(res.json())
            print js
            return js
        except Exception as e:
            print e
            return None

    def get_dict_of_email_and_subscribtion_status(list_url, list_id, auth):
        try:
            res = requests.get(list_url+'/'+list_id+'/'+'members', auth=auth)
            js = json.dumps(res.json())
            # print js
            return js
        except Exception as e:
            print e
            return None

    def send_list_to_mailchimp(self, list, list_name, sender_name, sender_email):
        self.list_url
        self.auth
        try:
            get_added_list_response = self.add_list(list_name, sender_name, sender_email)
            res = json.loads(get_added_list_response)
            list_id = res["id"]
            for each_member in list:
                print each_member
                self.add_member_to_list(list_id, email=each_member, status='subscribed')
        except Exception as e:
            print e


# # MailChimp Collection
# def build_mailchimp(request):
#     api_endpoint = request.session['mailchimp_details']['api_endpoint']
#     base_url = api_endpoint+'/3.0/'
#     api_key = request.session['mailchimp_details']['access_token'] + '-' + request.session['mailchimp_details']['dc']
#     usern = request.session['mailchimp_details']['login']['login_name']
#     auth = HTTPBasicAuth(usern, api_key)
#     list_url = base_url+'lists'
#     # print list_url
#     # Get All Lists
#     try:
#     collection_of_lists = get_all_list(list_url, auth)
#     val = json.loads(collection_of_lists)
#     specific_list = 'Freddie Favorite Hats'
#     # specific_list = 'TemporaryList'
#     specific_id = None
#     for list in val['lists']:
#         if list['name'] == specific_list:
#             specific_id = list['id']
#     add_member_response = add_member(list_url, specific_id, auth, 'adnankhan.295@gmail.com', 'subscribed')
#     # print add_member_response
#     dict_of_email = {}
#     # dict_of_email = get_dict_of_email_and_subscribtion_status(list_url, specific_id, auth)
#     # val2 = json.loads(dict_of_email)
#     # print val2
#     return render(request, 'build_mailchimp/build-mailchimp.html', {
#         'collection_of_lists': collection_of_lists,
#         'add_member_response': dict_of_email
#     })

