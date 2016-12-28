from .Universal_function_master import Universal_function
from .function_input import get_id, get_cu_id
from .Universal_function_personal import Universal_function_Personal
from .models import Personal
from .models import master_table

def A12(input_come):
# def A12(input_come, request):

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

    print list_match

    list_match_master = list_match


    new_list = []
    for y1 in input_come:
        if y1[0] in list_match_master:
            Universal_1 = Universal_function(y1)
            Universal = get_cu_id(Universal_1)
            new_list.append(Universal)
        else:
            Universal = Universal_function_Personal(y1)
            Universal_1 = get_id(Universal)
            new_list.append(Universal_1)
    return new_list