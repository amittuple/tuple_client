import re
from .regular_part import first_regular,second_regular,third_regular,forth_regular
from .function_input import check_more_than_one_sign_like_greaterthan_lessthan_equal
from .function_input import convert_all_string_to_lower_case,convert_high_low_medium_into_maximum_min_medium_value
from .function_input import replace_operator_like_gt_lt_eq_in_standard_format,convert_unicode_to_string,changetoint,conevert_string_in_integer
from .models import master_table

def Universal_function(change_high_x):
    print 'enter in the Universal_function'
    check_for_more_gt_lt_eq = check_more_than_one_sign_like_greaterthan_lessthan_equal(change_high_x)

    change_into_lower_case = convert_all_string_to_lower_case(check_for_more_gt_lt_eq)

    change_high = convert_high_low_medium_into_maximum_min_medium_value(change_into_lower_case)

    replace_gt_lt = replace_operator_like_gt_lt_eq_in_standard_format(change_high)

    change_to_string = convert_unicode_to_string(replace_gt_lt)

    change_to_int = changetoint(change_to_string)

    mn = conevert_string_in_integer(change_to_int)

    mn1 = mn.split(" ")

    n9 = changetoint(mn1)

    def A(za):

        #  here we use of this sql query for any single domain like (cltv or churn ) and provide here min value and max value
        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s %d AND %s %s %d  " % (
            za[0], za[1], za[2], za[0], za[3], za[4]))
        return v11

    def B(za):
        #  here we use of this sql query for any single domain like cltv or churn or anything and provide equal value like this churn=0
        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s %d" % (za[0], za[1], za[2]))

        return v11

    def C(za):

        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s '%s'" % (za[0], za[1], za[2]))
        return v11

    def D(za):
        v11 = master_table.objects.raw(
            "SELECT * FROM team_master_table WHERE %s %s %d OR %s %s %d " % (za[0], za[1], za[2], za[0], za[4], za[5]))

        return v11

    if re.match(first_regular, mn):
        my = A
    if re.match(second_regular, mn):

        my = B
    if re.match(third_regular, mn):
        my = C
    if re.match(forth_regular, mn):
        my = D

    p = my(n9)
    master_object=[]
    for x in p:
        master_object.append(x)

    return master_object