import csv
import time
import re
from slackclient import SlackClient

from slack_function.function_for_slack import for_slack
from .models import Team_amit

def handle_command(command_1, channel,slack_client,token,command):
    var_check=0
    var_check_1=0
    regular_expression = r"(([a-z][ ]?)+)$"
    if command=='help':
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "color": "#581845",
            "title": "To filter the master view for campaigns",
            "text": "```Command: @tuplemia filter```",
            "mrkdwn_in": ["text"]

        }])
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "color": "#581845",
            "title": "To choose filter - Select Profile or Predictions",
            "text": "```Example \n TupleMIA - Choose Filter: Profile or Predictions \n User - @tuplemia Profile```",
            "mrkdwn_in": ["text"]

        }])
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "color": "#581845",
            "title": "To choose filter levels - Select appropriate column from data",
            "text": "```Example \n TupleMIA - Choose Filter Level: Churn or CLTV or High Converter or Value or Engagement or Bio \n User - @tuplemia Churn```",
            "mrkdwn_in": ["text"]

        }])
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "color": "#581845",
            "title": "To apply appropriate filters - Enter required value",
            "text": "```Example \n TupleMIA - Enter Value like (  churn = high OR churn = low OR churn = medium  OR  churn > 10 < 20 OR churn < 20) \n User - @tuplemia churn = high```",
            "mrkdwn_in": ["text"]

        }])
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "color": "#581845",
            "title": "To send the data for campaigns - Choose Platform",
            "text": "```Example \n TupleMIA - Select Platform: Mailchimp or Facebook or Adwords or Twitter or LinkedIn \n User - @tuplemia MailChimp```",
            "mrkdwn_in": ["text"]

        }])
        var_check_1=1
    if var_check_1==0:

        if re.match(regular_expression, command):

            # if command=="cltv" or command=="send" or command=='churn'or command=="profile" or command=="predictions" or command=='value'or command=='name'or command=='age'or command=='high_converter'or command=='country'or command=='filter'or command=='help':
            slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text=command_1)
            var_check = 1
        if var_check == 0:
            if type(command_1) != type([1, 2, 3]):
                # for image

                slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
                    "title": "click below and go to mailchimp",
                    "text": command_1
                }])

            else:
                voice_0 = 0
                if command_1 == []:
                    slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text="no record found")
                    voice_0 = 1
                if voice_0 == 0:

                    from team.models import PersonalTable
                    personal_client = PersonalTable._meta.get_fields()
                    list_table = []
                    for x in personal_client:
                        list_table.append(x.name)
                    print list_table
                    print 'table list'
                    with open('output_amit.csv', "wb") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([list_table[1], list_table[2], list_table[3]])
                        print command_1
                        print 'command_1'
                        writer.writerows(command_1)

                    with open('output_amit.csv', 'rb') as fin, \
                            open('foutput.txt', 'wb') as fout:
                        reader = csv.DictReader(fin)
                        writer = csv.DictWriter(fout, reader.fieldnames, delimiter='|')
                        writer.writeheader()
                        writer.writerows(reader)
                    import subprocess
                    input_slack_01 = command.strip(" ")
                    input_slack_1 = input_slack_01.split(" ")
                    voice = 0
                    for x in input_slack_1:

                        if x == 'csv' or x == 'excel' or x == 'sheet':
                            args_amit = ['curl', '-F', 'file=@output_amit.csv', '-F', "channels=" + channel, '-F',
                                         'token=' + token, 'https://slack.com/api/files.upload']
                            subprocess.call(args_amit)
                            voice = 1
                    if voice == 0:
                        args_amit = ['curl', '-F', 'file=@foutput.txt', '-F', "channels=" + channel, '-F', 'token=' + token,
                                     'https://slack.com/api/files.upload']
                        subprocess.call(args_amit)


def parse_slack_output(slack_rtm_output,AT_BOT):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

import threading
class myThread (threading.Thread):
    l=[]
    def __init__(self, BOT_ID, BOT_TOKEN,SLACK_TEAM):
        threading.Thread.__init__(self)
        self.BOT_ID = BOT_ID
        self.TOKEN = BOT_TOKEN
        self.SLACK_TEAM=SLACK_TEAM
        myThread.l.append(self.SLACK_TEAM)
    def run(self):
        slack_client = SlackClient(self.TOKEN)
        AT_BOT = "<@" + self.BOT_ID + ">"
        if slack_client.rtm_connect():
            def run_thread():
                print("tuple_mia connected and running!")
                while True:
                    command, channel = parse_slack_output(slack_client.rtm_read(),AT_BOT)
                    if command and channel:
                        command_1=for_slack(command)
                        handle_command(command_1, channel,slack_client,self.TOKEN,command)
                    time.sleep(READ_WEBSOCKET_DELAY)
            t1 = threading.Thread(target=run_thread)
            t1.start()
        else:
            print("Connection failed. Invalid Slack token or bot ID?")

READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
def createbot():

    for x in Team_amit.objects.all():
        BOT_ID = x.bot_user_id
        SLACK_BOT_TOKEN =x.bot_access_token
        SLACK_TEAM =x.team_name
        v=0
        for y in myThread.l:
             if str(y)==str(SLACK_TEAM):
                print "i am in"
                v=1
        if v==1:
            continue
        myThread(BOT_ID,SLACK_BOT_TOKEN,SLACK_TEAM).start()