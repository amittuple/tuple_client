from team.function_input import remove_extra_space
from .Universal_function_master import convert_all_string_to_lower_case

def chat_input(req):

    # remove extra space outside of the input
    list_from_user_input=req.strip("-")

    # split list from '-' in all string
    list_come_from_user_convert = list_from_user_input.split("-")

    # remove extra space in side the input
    remove_extra_added_space_in_input = remove_extra_space(list_come_from_user_convert)

    # convert all string to lowercase
    list_from_user_to_lowercase = convert_all_string_to_lower_case(remove_extra_added_space_in_input)


    return list_from_user_to_lowercase