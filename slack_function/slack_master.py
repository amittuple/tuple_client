from .function_amit_slack import changetoint,convert_str_to_int,get_cu_id, get_string_0
from team.regular_part import reg_one
import re,string
from team.models import MasterTable

def slack_master_input(inputLack_A13):
    print "########### enter into master slack funciton master table ##########"

    convert_strTo_int = convert_str_to_int(inputLack_A13)

    string_split=convert_strTo_int.split(" ")
    string_split_break=get_string_0(string_split)
    convert_STR=[]
    for x in string_split_break:
        s=" "
        for y in x:
            s=s+" "+y
        convert_STR.append(s)

    Str_List=[]
    for var in convert_STR:
        if var.find("high"):
            new_str=string.replace(var,'high',"'High'")
        elif var.find("low"):
            new_str=string.replace(var,'low',"'Low'")
        elif var.find("very low"):
            new_str=string.replace(var,'very low',"'Very Low'")
        elif var.find("very high"):
            new_str=string.replace(var,'very high',"'Very High'")
        elif var.find("medium"):
            new_str=string.replace(var,'medium',"'Medium'")
        Str_List.append(new_str)
        

    print Str_List
    print "******* Str_List )))))))))***********"
    changeToInt = changetoint(Str_List)

    def ext_my(za):

        print "*********** za ******************"
        v11 = MasterTable.objects.raw("SELECT * FROM master_table WHERE " +' AND '.join(za))
        return v11

    if re.match(reg_one,convert_strTo_int ):
        my_input = ext_my

    p = my_input(changeToInt)
    master_object = []
    for x in p:
        master_object.append(x)
    master_table_cust_id=get_cu_id(master_object)
    return master_table_cust_id