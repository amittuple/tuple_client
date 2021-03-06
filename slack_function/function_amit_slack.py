from team.models import PersonalTable,MasterTable
import re

list_match = []
personal_list = []
for column_name in PersonalTable._meta.get_fields():
    if column_name.name != 'id' and column_name.name != 'cu_id':
        personal_list.append(column_name.name)
        list_match.append(column_name.name)

master_list = []
for column_name in MasterTable._meta.get_fields():
    if column_name.name != 'id' and column_name.name != 'cust_id':
        master_list.append(column_name.name)
        list_match.append(column_name.name)

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

def changetoint(s09):
    a = []
    for x in s09:
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

def Standard1(stunt):

    a1=stunt[0]
    try:
        for a in stunt[1:]:

            a1=set(a1).intersection(a)

    except:

            pass

    b=list(a1)
    return b

def convert_high_low_medium_value(high_low_medium):

    cltv_max = 0
    churn_max = 0

    length_churn=[]
    length_churn_1=[]
    length_churn_2=[]
    length_cltv=[]
    length_cltv_1=[]
    length_cltv_2=[]
    master_table_list = MasterTable.objects.all()
    for row in master_table_list:
        if row.cltv > cltv_max:
            cltv_max = row.cltv
        if row.churn > churn_max:
            churn_max=row.churn
    for x in high_low_medium:

        if x=='cltv' :
            length_cltv.append('cltv')

        elif x == '=' or x=='gt':

            length_cltv.append('>')
        elif x =="high":

            hi=str(cltv_max*70/100)
            length_cltv.append(hi)

            return length_cltv
        else:
             for x1 in high_low_medium:

                if x1 == 'cltv':
                    length_cltv_1.append('cltv')
                elif x1 == '=' or x1=='&lt;':

                    length_cltv_1.append('<')
                elif x1 =='&gt;':
                    length_cltv_1.append('>')


                elif x1=='low':
                    lo=str(cltv_max*30/100)
                    length_cltv_1.append(lo)

                    return length_cltv_1

                else:
                    for x2 in high_low_medium:
                        if x2 == 'cltv':
                            length_cltv_2.append('cltv')
                        elif x2 == '=' or x2=='&lt;' :

                            length_cltv_2.append('>')
                        elif x2 == 'medium':


                            length_cltv_2.append(str(cltv_max*30/100))
                            length_cltv_2.append("<")
                            length_cltv_2.append(str(cltv_max*70/100))

                            return length_cltv_2
                        else:
                            for x3 in high_low_medium:

                                if x3=='churn':
                                    length_churn.append('churn')
                                elif x3=='high_converter':
                                    length_churn.append('high_converter')
                                elif x3=='=' or x3=='&gt;' :
                                    length_churn.append('>')

                                elif x3 == 'high':
                                    length_churn.append(str(churn_max * 70 / 100))

                                    return length_churn
                                else:
                                    for x3 in high_low_medium:

                                        if x3 == 'churn':
                                            length_churn_1.append('churn')
                                        elif x3 == 'high_converter':
                                            length_churn_1.append('high_converter')
                                        elif x3 == 'eq' or x3=='&lt;':
                                            length_churn_1.append('<')
                                        elif x3 == 'low':
                                            length_churn_1.append(str(churn_max * 30 / 100))
                                            return length_churn_1

                                        else:
                                            for x3 in high_low_medium:

                                                if x3 == 'churn':
                                                    length_churn_2.append('churn')
                                                elif x3 == 'high_converter':
                                                    length_churn_2.append('high_converter')
                                                elif x3 == '=':
                                                    length_churn_2.append('<')
                                                elif x3 == 'medium':

                                                    length_churn_2.append(str(churn_max * 70 / 100))
                                                    length_churn_2.append('>')
                                                    length_churn_2.append(str(churn_max * 30 / 100))
                                                    return length_churn_2
                                                else:
                                                    return high_low_medium

def get_string(input_list):
    list1=[]
    a = 0
    b = -1
    for x in input_list:
        b = b + 1

        if x in personal_list:
            v=get_list(a, b-1, input_list)
            if v!=[]:
                list1.append(v)
                a = b
            continue
        else:
            if input_list.index(x) == len(input_list)-1:
                v2=get_list(a, b, input_list)
                list1.append(v2)
    return list1
def get_list(a, b, input_list):
    list = []

    if a == 0 and b == -1:
        return " "

    for x in range(len(input_list)):
        if x < b + 1 and x > a - 1:
            list.append(input_list[x])

    return list

def remove_extra_space(space_input):
    list=[]
    for x in space_input:
        if x=="":
            print "found space"
        else:
            list.append(x)
    return list

def get_id(input):

    list_1=[]
    for x in input:
        list_1.append(x.cu_id)

    return list_1

def get_cu_id(input):
    list_2=[]

    for x in input:

        list_2.append(x.cust_id)

    return list_2


def get_string_0(input_list):
    list_000=[]
    a = 0
    b = -1
    for x in input_list:
        b = b + 1

        if x in master_list:
            v=get_list_0(a, b-1, input_list)
            if v!=[]:
                list_000.append(v)
                a = b
            continue
        else:
            if input_list.index(x) == len(input_list)-1:
                v2=get_list_0(a, b, input_list)
                list_000.append(v2)
    return list_000[1:]
def get_list_0(a, b, input_list):
    list00 = []

    if a == 0 and b == -1:
        return " "

    for x in range(len(input_list)):
        if x < b + 1 and x > a - 1:
            list00.append(input_list[x])

    return list00