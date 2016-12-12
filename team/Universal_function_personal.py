from .regular_part import f1_regular,f2_regular,f3_regular
from .function_input import *
from team.models import Personal

def Universal_function_Personal(change_high_x):
    check_for_more_gt_lt_eq = check_more_than_one_sign_like_greaterthan_lessthan_equal(change_high_x)

    change_into_lower_case = convert_all_string_to_lower_case(check_for_more_gt_lt_eq)

    change_high = convert_high_low_medium_into_maximum_min_medium_value(change_into_lower_case)

    replace_gt_lt = replace_operator_like_gt_lt_eq_in_standard_format(change_high)

    change_to_string = convert_unicode_to_string(replace_gt_lt)

    change_to_int = changetoint(change_to_string)

    mn = conevert_string_in_integer(change_to_int)

    mn1 = mn.split(" ")

    n9 = changetoint(mn1)

    def C(za):
        print 'fifth sql'

        v11 = Personal.objects.raw("SELECT * FROM team_Personal WHERE %s %s '%s'" % (za[0], za[1], za[2]))

        return v11

    def B(za):

        print "6th sql"
        v11 = Personal.objects.raw("SELECT * FROM team_Personal WHERE %s %s %d" % (za[0], za[1], za[2]))
        return v11

    def A(za):
        print "7th sql"
        v11 =Personal.objects.raw("SELECT * FROM team_Personal WHERE %s %s %d" % (za[0], za[1], za[2],za[0],za[3],za[4],za[5]))
        return v11

    if re.match(f1_regular, mn):

        my_1 = C
    if re.match(f2_regular, mn):

        my_1 = B
    if re.match(f3_regular,mn):
        my_1=A

    p = my_1(n9)

    output_come=[]

    for xy in p:

        output_come.append(xy)

    return output_come