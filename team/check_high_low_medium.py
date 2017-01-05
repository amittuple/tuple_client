from .models import master_table,Personal
list_match = []
personal_list = []
for column_name in Personal._meta.get_fields():
    if column_name.name != 'id' and column_name.name != 'cu_id':
        personal_list.append(column_name.name)
        list_match.append(column_name.name)

master_list = []
for column_name in master_table._meta.get_fields():
    if column_name.name != 'id' and column_name.name != 'cust_id':
        master_list.append(column_name.name)
        list_match.append(column_name.name)

def convert_high_low_medium_into_maximum_min_medium_value(high_low_medium):

    cltv_max = 0
    churn_max = 0

    length_churn=[]
    length_churn_1=[]
    length_churn_2=[]
    length_cltv=[]
    length_cltv_1=[]
    length_cltv_2=[]
    master_table_list = master_table.objects.all()
    for row in master_table_list:
        if row.cltv > cltv_max:
            cltv_max = row.cltv
        if row.churn > churn_max:
            churn_max=row.churn
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
                                                    return high_low_medium

#  check the data is multiple or single
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


