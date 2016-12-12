from .regular_part import first_regular,second_regular,third_regular,forth_regular
from .function_input import *
from .function_for_slack import for_slack

def Universal_function(change_high_x):

    check_for_more_gt_lt_eq = check_more_than_one_sign_like_greaterthan_lessthan_equal(change_high_x)


    change_into_lower_case = convert_all_string_to_lower_case(check_for_more_gt_lt_eq)


    change_high = convert_high_low_medium_into_maximum_min_medium_value(change_into_lower_case)

    replace_gt_lt = replace_operator_like_gt_lt_eq_in_standard_format(change_high)

    change_to_string = convert_unicode_to_string(replace_gt_lt)

    change_to_int = changetoint(change_to_string)


    mn = conevert_string_in_integer(change_to_int)
    print 'amit'
    print mn
    print type(mn)

    mn1 = mn.split(" ")

    n9 = changetoint(mn1)
    print "n0"
    print n9

    def A(za):
        print 'first sql'
        print za
        #  here we use of this sql query for any single domain like (cltv or churn ) and provide here min value and max value
        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s %d AND %s %s %d  " % (
            za[0], za[1], za[2], za[0], za[3], za[4]))
        print v11
        return v11

    def B(za):
        #  here we use of this sql query for any single domain like cltv or churn or anything and provide equal value like this churn=0
        print 'second sql'
        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s %d" % (za[0], za[1], za[2]))

        return v11

    def C(za):
        print 'third sql'

        v11 = master_table.objects.raw("SELECT * FROM team_master_table WHERE %s %s '%s'" % (za[0], za[1], za[2]))
        return v11

    def D(za):
        print "forth sql"
        v11 = master_table.objects.raw(
            "SELECT * FROM team_master_table WHERE %s %s %d OR %s %s %d " % (za[0], za[1], za[2], za[0], za[4], za[5]))

        return v11

    if re.match(first_regular, mn):
        print "first regular expression "

        my = A
    if re.match(second_regular, mn):
        print 'second regular expression'

        my = B
    if re.match(third_regular, mn):

        print 'third regular enter'

        my = C
    if re.match(forth_regular, mn):
        print "forth regular expression"
        my = D

    p = my(n9)

    master_object=[]
    print "p"
    print p

    for x in p:
        master_object.append(x)

    return master_object