from team.function_input import email_id_list, name_firstname_lastname
from .function_input import Standard, get_string,remove_unwanted_keyword
from .input_check_value import first_it_come_check
from .function_two_table import A12
from .model_extras import chat_store
import time
from slack_bot.models import email_list_for_slack_1

def bot_user(request,input_from_tuple_mia):
    # remove unwanted keyword
    tuple_mia_input = remove_unwanted_keyword(input_from_tuple_mia)

    in_com = first_it_come_check(tuple_mia_input)

    if in_com=='amit_bot':

        # break in two more than one if it isqu possible
        break_into_more_than_one_part_if_possible = get_string(tuple_mia_input)
        # send to seprate of them
        print break_into_more_than_one_part_if_possible
        print "3###########  break_into_more_than_one_part_if_possible ########$$$$$$$"
        a12_obj = A12(break_into_more_than_one_part_if_possible)

        send_into_seprate_them = a12_obj

        print send_into_seprate_them
        print 'send to seprate them'
        # send_into_seprate_them = A12(break_into_more_than_one_part_if_possible, request)

        Study = Standard(send_into_seprate_them)
        poem=name_firstname_lastname(Study)
        request.session['request_session'] = Study
        request.session['request_name'] = poem
        email = email_id_list(Study)
        print 'email'
        print email
        email_list_for_slack_1.objects.all().delete()
        message = "Here's Your Result. If You Want To Send Email List To Mailchimp Then Type 'mailchimp' In Tuple MIA, Login You Mailchimp Account And Enjoy..."
        if email != None:
            if len(email) != 0:
                obj = email_list_for_slack_1()
                obj.email_list_slack = email
                obj.save()
        obj_chat = chat_store()
        obj_chat.chat_sendby="bot"
        obj_chat.chat_time=time.ctime()
        obj_chat.chat_message=message
        obj_chat.save()
        return message
    else:
        respo=in_com
        obj_chat = chat_store()
        obj_chat.chat_sendby="bot"
        obj_chat.chat_message=in_com
        obj_chat.chat_time=time.ctime()
        obj_chat.save()
        return respo