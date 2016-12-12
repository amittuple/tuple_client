from django.conf import settings
import requests, json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from team.function_for_slack import for_slack
from .models import Team_amit


def index(request):
    client_id = settings.CLIENT_ID
    print client_id
    print 'client_id'
    return render(request, 'slackbot/landing.html', {'client_id': client_id})


def slack_oauth(request):
    code = request.GET['code']
    print "amitttttt"
    params = {
        'code': code,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    # print "json responce"
    json_response = requests.get(url,params)
    data = json.loads(json_response.text)
    # print "jsonnnnn"
    print data

    Team_amit.objects.create(
        team_name=data['team_name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token']
    )

    return HttpResponseRedirect(reverse('TEST'))


def test_bot(self):
    import os
    import threading
    import time
    from slackclient import SlackClient
    # starterbot's ID as an environment variable
    BOT_ID = 'U37524MHA'

    # constants
    AT_BOT = "<@" + BOT_ID + ">"

    slack_client = SlackClient('xoxb-109172157588-FqPZCfs8KjC49ixXL2GbfGkk')

    def handle_command(command_1, channel):

        slack_client.api_call("chat.postMessage", channel=channel,
                              text=' '.join(command_1), as_user=True)

    def parse_slack_output(slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']
        return None, None

    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        def run_thread():
            while True:
                command, channel = parse_slack_output(slack_client.rtm_read())

                if command and channel:
                    command_1=for_slack(command)
                    print command_1
                    handle_command(command_1, channel)
                time.sleep(READ_WEBSOCKET_DELAY)

        t1=threading.Thread(target=run_thread)
        t1.start()

    else:
        print("Connection failed. Invalid Slack token or bot ID?")

    return HttpResponse('sucess')
