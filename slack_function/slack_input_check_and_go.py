from slack_function.function_amit_slack import changetoint
from team.function_input import convert_unicode_to_string, conevert_string_in_integer
import re

from team.models import PersonalTable,MasterTable


def first_it_come_slack_check(input_check):
   change_to_string = convert_unicode_to_string(input_check)

   change_to_int = changetoint(change_to_string)
   mn = conevert_string_in_integer(change_to_int)
   regular_expression = r"(([a-z][ ]?[?]?[_]?)+)$"

   personal_list = []
   m_list = []

   for column_name in PersonalTable._meta.get_fields():
       if column_name.name != 'id' and column_name.name != 'cu_id':
           personal_list.append(column_name.name)

   for column_name in MasterTable._meta.get_fields():
       if column_name.name != 'id' and column_name.name != 'cust_id':
           m_list.append(column_name.name)

   if re.match(regular_expression,mn):
       if input_check == [u'thanks'] or input_check == [u'thank', u'you']:
           return "WelCome"
       if input_check == [u'cluster']:
           return "Enter Value like ( Cluster < 100 OR Cluster < 100 > 20 )"
       if input_check == [u'engagement']:
           return "Enter Value like ( Engagement = low OR Engagement = high )"
       if input_check == [u'high_convertor']:
           return "Enter Value like ( High_Converter = low OR High_Converter = high OR High_Converter = medium )"
       if input_check == [u'email_id']:
           return "Enter Value Like ( Email_Id = tuple@gmail.com )"
       if input_check == [u'send']:
           return 'Select Platform: Mailchimp or Facebook or Adwords or Twitter or LinkedIn'

       if input_check == [u'filter']:
           return "Choose Filter: Profile or Predictions"

       if input_check == [u'predictions']:
           return "Choose Filter Level: " + " or ".join(m_list)

       if input_check == [u'profile']:
           return "Choose Filter Level: " + " or ".join(personal_list)

       if input_check == [u'country']:
           return 'Enter Value (country = india OR country = america)'

       if input_check == [u'cltv']:
           return "Enter Value (cltv = high OR cltv = low OR cltv = medium  OR  cltv > 10 < 20 OR cltv < 20)"

       if input_check == [u'churn']:
           return "Enter Value like (  churn = high OR churn = low OR churn = medium  OR  churn > 10 < 20 OR churn < 20)"

       if input_check == [u'age']:
           return "Enter Value( age > 10 < 20 OR age < 20 OR age > 12)"
       if input_check == [u'hello'] or input_check == [u'hi']:
           return "hello"
       if input_check == [u'how', u'are', u'you?'] or input_check == [u'how', u'r', u'u'] or input_check==[u'how',u'are',u'you']:
           return "i am fine and you"
       if input_check == [u'fine']:
           return "ok how can I assist you"
       else:
           return "I'm sorry, I don't understand! Sometimes I have an easier time with a few simple keywords.please type: help"

   return 'amit_bot'