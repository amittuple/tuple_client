from django.shortcuts import HttpResponseRedirect
from .break_in_input_in_slack import A12_slack
from .slack_input_check_and_go import first_it_come_slack_check
from .function_amit_slack import remove_extra_space,get_string,Standard1, change_gt_lt_and
from banana_py import Bananas_OAuth

def for_slack(input_slack):
    input_slack_01=input_slack.strip(" ")
    input_slack_1=input_slack_01.split(" ")
    remove_extra_space_from_input_1   =   remove_extra_space(input_slack_1)

    remove_extra_space_from_input = []
    remove_element = ['is', 'to', 'good', 'best', 'the', 'for', 'some', 'top', 'in', 'text', 'txt', 'sheet','csv', 'excel']
    for x in remove_extra_space_from_input_1:
        if x in remove_element:
            print 'remove extra keyword'
        else:
            remove_extra_space_from_input.append(x)

    if remove_extra_space_from_input == [u'mailchimp']:
        return (u'%s' % (Bananas_OAuth().authorize_url()))


    else:
        remove_gt_lt_to_standard = change_gt_lt_and(remove_extra_space_from_input)

        outpu_come_slack=first_it_come_slack_check(remove_gt_lt_to_standard)

        if outpu_come_slack == 'amit_bot':

            input_slack_2 = get_string(remove_gt_lt_to_standard)

            inputLack_A12=A12_slack(input_slack_2)

            inputLack_A123=Standard1(inputLack_A12)
            return inputLack_A123
        else:
            amit_tuple = outpu_come_slack
            return amit_tuple

