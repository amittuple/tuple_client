from .regular_part import first_regular,second_regular,third_regular,forth_regular
from .models import master_table
import re
from .function_input import get_cu_id,email_id_list

def for_slack(input_slack):

    input_slack_1=input_slack.split(" ")

    input_slack_2=convert_unicode_to_string_slack(input_slack_1)

    n91=change_gt_lt_and(input_slack_2)

    n90=convert_unicode_to_integer(n91)

    n9=convert_str_to_int(n90)

    split_n9=n9.split(' ')

    n10=changetoint(split_n9)

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

    if re.match(first_regular, n9):
        print "first regular expression "

        my_input = A
    if re.match(second_regular, n9):
        print 'second regular expression'

        my_input = B
    if re.match(third_regular, n9):
        print 'third regular enter'

        my_input = C
    if re.match(forth_regular, n9):
        print "forth regular expression"
        my_input = D

    p = my_input(n10)
    print p
    master_object = []

    for x in p:
        master_object.append(x)
    print master_object
    print 'mster_object'

    master_object_get_cu_id=get_cu_id(master_object)
    print master_object_get_cu_id
    print 'get_cu_id'
    master_object_email_id=email_id_list(master_object_get_cu_id)
    print 'master_object_email_id'
    print master_object_email_id
    return master_object_email_id

# change gt lt to standard format
def change_gt_lt_and(input_check_gt):
    l = []
    for x in input_check_gt:
        if x == '&lt;' or x=='lt':
            l.append('<')
        elif x == '&gt;' or x=='gt':
            l.append('>')

        else:
            l.append(x)
    return l

# convert unicode to string
def convert_unicode_to_string_slack(l):
    s = []
    for x in l:
        x1 = r"[a-z]+"
        if re.match(x1, x):
            x = str(x)
            s.append(x)
        else:
            s.append(x)
    return s

# convrt unicode to integer
def convert_unicode_to_integer(s):
    a = []
    for x in s:
        try:
            x = int(x)
            a.append(x)
        except:
            a.append(x)

    return a
def changetoint(s):
    a = []
    for x in s:
        try:
            x = int(x)
            a.append(x)
        except:
            a.append(x)

    return a

def convert_str_to_int(input_str):
    m1 = ''
    i = 0
    for x in input_str:
        i = i + 1
        if i == 1:
            if type(x) == int:
                m1 = m1 + str(x)
            else:
                m1 = m1 + x
        else:
            if type(x) == int:

                m1 = m1 + " "
                m1 = m1 + str(x)
            else:
                m1 = m1 + " "
                m1 = m1 + x
    return m1.strip(' ')
