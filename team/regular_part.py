import re
first_regular = r"([a-z\_]+ ([>]|[<]) [0-9]+ ([<]|[>]) [0-9]+)$"
second_regular = r"([a-z\_]+ ([=]|[<]|[>]) [0-9]+)$"
third_regular = r'([a-z\_]+ ([=]|[<]|[>]) [a-z]+)$'
forth_regular = r'([a-z\_]+ ([<]|[>]) \w+ ([OR]|[or])*[ ]([<]|[>]) \w+)$'

f1_regular=r'([a-z]+ [=] [a-z]+)$'
f2_regular = r"([a-z]+ ([=]|[<]|[>]) [0-9]+)$"
f3_regular = r'([a-z]+ ([=]|[<]|[>]) [0-9]+ [a-z]+ ([=]|[<]|[>]) [0-9]+)$'
