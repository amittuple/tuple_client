from django.http import HttpResponse
from team.models import MasterTable
from team.models import PersonalTable
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

# first check the element have more than gt(>),lt(<),eq(=) then convert this to gt,lt,eq ....
def check_more_than_one_sign_like_greaterthan_lessthan_equal(check_more):
    check=[]
    # print check_more
    # print "check more"

    for x in check_more:
        if x=='eqeq' or x=='eqeqeq' :

            check.append('eq')
        elif x=='gtgt' or x=='gtgtgt':
            check.append('gt')
        elif x =='ltlt' or x=='ltltlt':
            check.append('lt')

        else:
            check.append(x)

    return check

# convert all string to lower_case....
def convert_all_string_to_lower_case(change_lower):

    change=[]
    for x in change_lower:

        a=x.lower()
        change.append(a)

    return change

# convert all unicode to string....
def convert_unicode_to_string(l):
    s = []
    for x in l:

        x1 = r"[a-z]+"
        if re.match(x1, x):
            x = str(x)
            s.append(x)
        else:
            s.append(x)

    return s

# convert high, low, medium in to specific value...... acording to attribute....
def convert_high_low_medium_into_maximum_min_medium_value(high_low_medium):

    cltv_max = 0
    churn_max = 0
    cluster_max = 0
    length_churn=[]
    length_churn_1=[]
    length_churn_2=[]
    length_cltv=[]
    length_cltv_1=[]
    length_cltv_2=[]
    cluster_length=[]
    master_table_list = MasterTable.objects.all()
    for row in master_table_list:
        if row.cltv != None:
            if row.cltv > cltv_max:
                cltv_max = row.cltv
        if row.churn != None:
            if row.churn > churn_max:
                churn_max=row.churn
        if row.cluster != None:
            if row.cluster > cluster_max:
                cluster_max = row.cluster
    for x in high_low_medium:

        if x=='cltv' :
            length_cltv.append('cltv')

        elif x == 'eq' or x=='gt':

            length_cltv.append('gt')
        elif x=='lt':
            length_cltv.append('lt')

        elif x =="high":

            hi=str(cltv_max*70/100)
            length_cltv.append(hi)

            return length_cltv
        else:

            for x1 in high_low_medium:

                if x1 == 'cltv':
                    length_cltv_1.append('cltv')
                elif x1 == 'eq' or x1=='lt':

                    length_cltv_1.append('lt')
                elif x1 =='gt':
                    length_cltv_1.append('gt')


                elif x1=='low':
                    lo=str(cltv_max*30/100)
                    length_cltv_1.append(lo)

                    return length_cltv_1

                else:

                    for x2 in high_low_medium:
                        if x2 == 'cltv':
                            length_cltv_2.append('cltv')
                        elif x2 == 'eq' or x2=='lt' or x2=='lt':

                            length_cltv_2.append('gt')
                        elif x2 == 'medium':


                            length_cltv_2.append(str(cltv_max*30/100))
                            length_cltv_2.append("lt")
                            length_cltv_2.append(str(cltv_max*70/100))

                            return length_cltv_2
                        else:

                            for x3 in high_low_medium:

                                if x3=='churn':
                                    length_churn.append('churn')
                                elif x3=='high_converter':
                                    length_churn.append('high_converter')
                                elif x3=='eq' or x3=='gt' :
                                    length_churn.append('gt')

                                elif x3 == 'high':
                                    length_churn.append(str(churn_max * 70 / 100))

                                    return length_churn
                                else:

                                    for x3 in high_low_medium:

                                        if x3 == 'churn':
                                            length_churn_1.append('churn')
                                        elif x3 == 'high_converter':
                                            length_churn_1.append('high_converter')
                                        elif x3 == 'eq' or x3=='lt':
                                            length_churn_1.append('lt')
                                        elif x3 == 'low':
                                            length_churn_1.append(str(churn_max * 30 / 100))
                                            return length_churn_1

                                        else:

                                            for x3 in high_low_medium:

                                                if x3 == 'churn':
                                                    length_churn_2.append('churn')
                                                elif x3 == 'high_converter':
                                                    length_churn_2.append('high_converter')
                                                elif x3 == 'eq':
                                                    length_churn_2.append('lt')
                                                elif x3 == 'medium':

                                                    length_churn_2.append(str(churn_max * 70 / 100))
                                                    length_churn_2.append('gt')
                                                    length_churn_2.append(str(churn_max * 30 / 100))
                                                    return length_churn_2
                                                else:

                                                    for x30 in high_low_medium:
                                                        if x30 == 'cluster':
                                                            cluster_length.append('cluster')
                                                        elif x30 == 'eq' or x30 == 'gt':
                                                            cluster_length.append('gt')
                                                        elif x30 == 'high':
                                                            cluster_length.append(cluster_max * 70 / 100)
                                                            return cluster_length
                                                        else:
                                                            for y10 in high_low_medium:
                                                                if y10 == 'cluster':
                                                                    cluster_length.append('cluster')
                                                                elif y10 == 'eq' or y10 == 'lt':
                                                                    cluster_length.append('lt')
                                                                elif y10 == 'low':
                                                                    cluster_length.append(cluster_max * 30 / 100)
                                                                    return cluster_length
                                                                else:

                                                                    for z10 in high_low_medium:
                                                                        if z10 == 'cluster':
                                                                            cluster_length.append('cluster')
                                                                        elif z10 == 'eq':
                                                                            cluster_length.append('gt')
                                                                        elif z10 == 'low':
                                                                            cluster_length.append(cluster_max * 30 / 100)
                                                                            cluster_length.append('lt')
                                                                            cluster_length.append(cluster_max * 70 / 100)
                                                                            return cluster_length
                                                                        else:

                                                                            print high_low_medium
                                                                            print '### amit ###'
                                                                            return high_low_medium




                                                    # return high_low_medium

#  convert gt,lt,eq in to >, <, =.....
def replace_operator_like_gt_lt_eq_in_standard_format(r):
    l = []
    for x in r:
        if x == 'gt':
            l.append('>')
        elif x == 'lt':
            l.append('<')
        elif x == 'eq':
            l.append('=')

        else:
            l.append(x)
    return l

#  break the coming input like [cltv < 2000 churn < 100] in two 2 sublist [[cltv < 2000],[churn < 100]]....
def get_string(input_list):
    list1=[]
    a = 0
    b = -1
    for x in input_list:
        b = b + 1

        if x in list_match:
            v=get_list(a, b-1, input_list)
            if v!=[]:
                list1.append(v)
                a = b
            continue
        else:
            if input_list.index(x) == len(input_list)-1:
                v2=get_list(a, b, input_list)
                list1.append(v2)

    return list1[1:]
def get_list(a, b, input_list):
    list = []

    if a == 0 and b == -1:
        return " "

    for x in range(len(input_list)):
        if x < b + 1 and x > a - 1:
            list.append(input_list[x])

    return list

#  collect integer form the input like cltv < 1000 choose 1000 from the list....
def changetoint(s):
    a = []

    for x in s:
        try:
            x = int(x)
            a.append(x)
        except:
            a.append(x)

    return a

#  change in to integer like '9000' to 9000....
def conevert_string_in_integer(a):
    m1 = ''
    i = 0
    for x in a:
        i = i + 1
        if i == 1:
            if isinstance(x, str):
                m1 = m1 + x
            else:
                m1 = m1 + str(x)
        else:
            if isinstance(x, str):
                m1 = m1 + " "
                m1 = m1 + x
            else:
                m1 = m1 + " "
                m1 = m1 + str(x)
    return m1

# here check the first element is /filter or not....
def input_comes_from_user(input_comes_fromuser):
    # print "slash check"
    if input_comes_fromuser[0] == '/filter':
        # print 'first element is slash_filter'
        return HttpResponse("choose filter: like profile or predictiond")

    else:
        # print "first element have not slash_filter"

        return input_comes_fromuser
# here intersect more than one inout like cltv < 1000 churn < 12 comapre here and find the intersection....
def Standard(stunt):

    a1=stunt[0]
    try:
        for a in stunt[1:]:

            a1=set(a1).intersection(a)
    except:

            pass

    b=list(a1)

    return b

# find the id of master_table table for intersection....
def get_id(input):

    list_1=[]
    for x in input:
        list_1.append(x.cu_id)

    return list_1

# find the id of personal table for intersection....
def get_cu_id(input):
    list_2=[]
    for x in input:

        list_2.append(x.cust_id)

    return list_2

# convert the list from id and cu_id to email_id....
def email_id_list(input):
    list_email=[]
    try:
        for x in input:
            person1 = PersonalTable.objects.filter(cu_id=x)[0]
            if person1.email_id!=None:
                    list_email.append(person1.email_id)
        return list_email
    except:
        return None

def remove_extra_space(space_input):
    list=[]
    for x in space_input:
        if x=='':
            print "found space"
        else:
            list.append(x)
    return list

remove_element=['is','to','good','best','the','for','some','top']
def remove_unwanted_keyword(input_keyword):
    remove_keyword=[]
    for x in input_keyword:
        if x in remove_element:
            print 'remove extra keyword'
        else:
            remove_keyword.append(x)
    return remove_keyword
def name_firstname_lastname(input_name):
   name=[]
   for x in input_name:
       x = str(x)
       person1 = PersonalTable.objects.filter(cu_id=x)[0]
       fname=person1.firstname
       lname=person1.lastname
       if fname!=None and lname==None:
           name.append(fname)
       elif fname==None and lname!=None:
           name.append(lname)
       elif fname!=None and lname!=None:
           name.append(fname+' '+lname)
       elif fname==None and lname==None:
           name.append(None)
   return name

def convert_flot(intput_float):
    list_float=[]

    for x in intput_float:
        try:
            x = float(x)
            list_float.append(x)
        except:
            list_float.append(x)

    return list_float