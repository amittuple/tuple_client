# table_dict should be in pattern like
# {
#     tablename:
#         column_name:
#             type:
#                column_type
# }

class BuildQuery:
    def __init__(self):
        pass
    def create_statement(self, table_dict):
        if table_dict is None:
            raise Exception("Table Dict Cannot Be None")
        table_name = table_dict.keys()[0]
        table_dict[table_name]


    def select_statement(self, tablename):
        if tablename is None:
            raise Exception("Tablename is Compulsory")
        if type(tablename) is not str:
            raise Exception("Tablename Should Be A String")
        return "SELECT * FROM " + str(tablename)


    def select_specific_columns(self, tablename, column_tuple):
        pass
