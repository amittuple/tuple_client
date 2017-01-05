import re
from team.regular_part import f1_regular,f2_regular,f3_regular
from .function_amit_slack import convert_str_to_int,changetoint,convert_unicode_to_string_slack,convert_high_low_medium_value, \
    from_master_table_id_to_find_personal_object, get_id
from team.models import Personal

def slack_function_Personal(change_high_x):
    print "enter into personal slack funciton personal table"

    change_high = convert_high_low_medium_value(change_high_x)

    change_to_string = convert_unicode_to_string_slack(change_high)

    change_to_int = changetoint(change_to_string)

    mn = convert_str_to_int(change_to_int)

    mn1 = mn.split(" ")

    n9 = changetoint(mn1)

    def C(za):
        v11 = Personal.objects.raw("SELECT * FROM team_Personal WHERE %s %s '%s'" % (za[0], za[1], za[2]))

        return v11

    def B(za):
        v11 = Personal.objects.raw("SELECT * FROM team_Personal WHERE %s %s %d" % (za[0], za[1], za[2]))
        return v11

    def A(za):
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
    cuid_personal=get_id(output_come)
    master_object_master= from_master_table_id_to_find_personal_object(cuid_personal)
    return master_object_master
