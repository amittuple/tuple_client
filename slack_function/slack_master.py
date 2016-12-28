from .function_amit_slack import convert_high_low_medium_value,convert_unicode_to_string_slack,convert_unicode_to_integer,changetoint,convert_str_to_int, \
    from_master_table_id_to_find_personal_object,get_cu_id

from team.regular_part import first_regular,second_regular,third_regular,forth_regular
import re
from team.models import master_table

def slack_master_input(inputLack_A13):

    print "enter into master slack funciton"

    input_slack_4=convert_high_low_medium_value(inputLack_A13)

    input_slack_5=convert_unicode_to_string_slack(input_slack_4)

    n90=convert_unicode_to_integer(input_slack_5)

    n9=convert_str_to_int(n90)

    split_n9=n9.split(' ')

    n10=changetoint(split_n9)

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

    if re.match(first_regular, n9):
        my_input = A
    if re.match(second_regular, n9):
        my_input = B
    if re.match(third_regular, n9):
        my_input = C
    if re.match(forth_regular, n9):
        my_input = D

    p = my_input(n10)

    master_object = []

    for x in p:
        master_object.append(x)
    cuid=get_cu_id(master_object)
    master_object_master= from_master_table_id_to_find_personal_object(cuid)

    return master_object_master
