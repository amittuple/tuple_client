from slack_function.function_amit_slack import Standard1
from .slack_master import slack_master_input
from .slack_personal import slack_function_Personal
from team.models import MasterTable, PersonalTable


def A12_slack(input_come):
    print input_come
    print "$$$$$$$$$$ input name )))))))))))))))"
    list_match = []
    for column_name in MasterTable._meta.get_fields():
        if column_name.name != 'id' and column_name.name != 'cust_id':
            list_match.append(column_name.name)

    new_list = []

    for y1 in input_come:

        if y1[0] in list_match:
            Universal_1 = slack_master_input(y1)
            new_list.append(Universal_1)

        else:

            Universal_p = slack_function_Personal(y1)
            new_list.append(Universal_p)

    after_insertion=Standard1(new_list)

    output_value=after_insertion_csv(after_insertion)

    return output_value

def after_insertion_csv(input_csv):

    csv_list=[]

    for x in input_csv:
        list_i=[]
        x = str(x)

        person1 = PersonalTable.objects.filter(cu_id=x)[0]
        fname = person1.firstname
        lname = person1.lastname
        email_name= person1.email_id

        if fname == None:
            list_i.append("N/A")
        else:
            list_i.append(fname)
        if lname==None:
            list_i.append("N/A")
        else:
            list_i.append(lname)
        if email_name==None:
            list_i.append("N/A")
        else:
            list_i.append(email_name)
        csv_list.append(list_i)
    return csv_list
