from team.function_input import email_id_list
from .function_input import Standard, get_string,remove_unwanted_keyword
from .input_check_value import first_it_come_check
from .function_two_table import A12
from slack_bot.models import email_list_for_slack_1

def bot_user(request,input_from_tuple_mia):
    # remove unwanted keyword
    tuple_mia_input = remove_unwanted_keyword(input_from_tuple_mia)

    in_com = first_it_come_check(tuple_mia_input)

    if in_com=='amit_bot':

        # break in two more than one if it isqu possible
        break_into_more_than_one_part_if_possible = get_string(tuple_mia_input)
        # send to seprate of them
        send_into_seprate_them = A12(break_into_more_than_one_part_if_possible)
        # send_into_seprate_them = A12(break_into_more_than_one_part_if_possible, request)

        Study = Standard(send_into_seprate_them)

        request.session['request_session'] = Study

        email = email_id_list(Study)

        obj = email_list_for_slack_1()
        obj.email_list_slack = email
        obj.save()

        return "your data has been store if you want to send email_id to mailchimp then press 'send to mailchimp' in tuple-mia and login your mailchimp account and enjoy..."
    else:
        respo=in_com
        return respo
