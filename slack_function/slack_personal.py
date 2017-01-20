import re
from team.regular_part import f1_regular,f2_regular,f3_regular
from .function_amit_slack import convert_str_to_int,changetoint, get_id
from team.models import PersonalTable

def slack_function_Personal(change_high_x):
    print "########## enter into personal slack funciton personal table #########"

    change_to_int = changetoint(change_high_x)

    mn = convert_str_to_int(change_to_int)

    mn1 = mn.split(" ")

    n9 = changetoint(mn1)

    def C(za):
        v11 = PersonalTable.objects.raw("SELECT * FROM personal_table WHERE %s %s '%s'" % (za[0], za[1], za[2]))
        return v11

    def B(za):
        v11 = PersonalTable.objects.raw("SELECT * FROM personal_table WHERE %s %s %f" % (za[0], za[1], za[2]))
        return v11

    def A(za):
        v11 =PersonalTable.objects.raw("SELECT * FROM personal_table WHERE %s %s %f %s %s %f" % (za[0], za[1], za[2],za[0],za[3],za[4],za[5]))
        return v11

    if re.match(f1_regular, mn):
        afterRegular_match = C
    if re.match(f2_regular, mn):
        afterRegular_match = B
    if re.match(f3_regular,mn):
        afterRegular_match=A

    p = afterRegular_match(n9)

    output_come=[]

    for xy in p:

        output_come.append(xy)
    cuid_personal=get_id(output_come)
    # master_object_master= from_master_table_id_to_find_personal_object(cuid_personal)
    return cuid_personal
