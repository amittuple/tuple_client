import csv
import time

from slackclient import SlackClient

from slack_function.function_for_slack import for_slack
from .models import Team_amit


def handle_command(command_1, channel,slack_client,token,command):
    if type(command_1)!=type([1,2,3]):
        # for image
        print command_1
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, attachments=[{
            "title": "click bellow and go to mailchimp",
            "text": command_1
        }])
        #  for button
        # slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text= "",attachments= [
        #
        # {
        #
        #     "fallback": "",
        #     "callback_id": "wopr_game",
        #     "color": "#3AA3E3",
        #     "attachment_type": "default",
        #     "actions": [
        #
        #         {
        #             "name": "maze",
        #             "text": "Falken's Maze",
        #             "type": "button",
        #             "value": command_1
        #         }
        #     ]
        # }
        # ]
        #
        # )
    else:
        from team.models import Personal
        personal_client=Personal._meta.get_fields()
        list_table=[]
        for x in personal_client:
            list_table.append(x.name)
        print list_table
        print 'amit_table'
        with open('output_amit.csv', "wb") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([list_table[4], list_table[2], list_table[3], list_table[5]])
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
        voice=0
        for x in input_slack_1:

            if x=='csv' or x=='excel' or x=='sheet':
                args_amit=['curl', '-F', 'file=@output_amit.csv', '-F', "channels="+ channel, '-F', 'token='+token, 'https://slack.com/api/files.upload']
                subprocess.call(args_amit)
                voice=1
        if voice==0:
            args_amit=['curl', '-F', 'file=@foutput.txt', '-F', "channels="+ channel, '-F', 'token='+token, 'https://slack.com/api/files.upload']
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