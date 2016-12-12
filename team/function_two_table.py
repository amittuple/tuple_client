from .Universal_function_master import Universal_function
from .function_input import get_id, get_cu_id
from .Universal_function_personal import Universal_function_Personal
list_match_personal=['name','gender','age','country']

def A12(input_come, request):
    new_list = []

    for y1 in input_come:

        if y1[0] in list_match_personal:
            Universal = Universal_function_Personal(y1)

            Universal_1 = get_id(Universal)
            new_list.append(Universal_1)

        else:
            Universal_1 = Universal_function(y1)
            Universal = get_cu_id(Universal_1)
            new_list.append(Universal)
    request.session["master_list"]=new_list
    print 'newLISTFROM personal_master'
    print new_list
    return new_list