from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
import requests
from .models import Team_amit
from .startbot import createbot


def index(request):
    client_id = settings.SLACK_CLIENT_ID
    return render(request, 'slackbot/landing.html', {'client_id': client_id})

def slack_oauth(request):
    code = request.GET['code']

    params = {
        'code': code,
        'client_id': settings.SLACK_CLIENT_ID,
        'client_secret': settings.SLACK_CLIENT_SECRET
    }
    print "code"
    print code
    print params
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    a=Team_amit.objects.all()
    already=0;
    r=''
    for x in a:
        if str(x.team_name) == data['team_name']:
              already=1
    if already ==1:

         r='Bot is already added to your Slack team!'
    else:
        Team_amit.objects.create(
            team_name=data['team_name'],
            team_id=data['team_id'],
            bot_user_id=data['bot']['bot_user_id'],
            bot_access_token=data['bot']['bot_access_token']
        )
        r='Bot added to your Slack team!'

    createbot()
    return HttpResponse(r)