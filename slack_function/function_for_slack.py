from custom_class.convert_string import convert_string
from .break_in_input_in_slack import A12_slack
from .slack_input_check_and_go import first_it_come_slack_check
from .function_amit_slack import get_string,change_gt_lt_and,convert_high_low_medium_value,convert_unicode_to_integer
from banana_py import Bananas_OAuth

def for_slack(input_slack):
    obj1 = convert_string()
    input_slack_01=input_slack.strip(" ")
    input_slack_1=input_slack_01.split(" ")
    remove_extra_space_from_input_1 = obj1.remove_extra_space_fromInput(input_slack_1)

    print remove_extra_space_from_input_1
    print "NNNNNNNNNNNNNNNNNNNNNNNNN _______________________ ****************"

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

            after_gating_string = convert_high_low_medium_value(remove_gt_lt_to_standard)

            convert_high_low_med = get_string(after_gating_string)
            print convert_high_low_med
            print "######### high low med"

            convert_unicodeto_int = convert_unicode_to_integer(convert_high_low_med)

            after_breaking_two_part_and_output  =  A12_slack(convert_unicodeto_int)

            return after_breaking_two_part_and_output
        else:
            amit_tuple = outpu_come_slack
            return amit_tuple