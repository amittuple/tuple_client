from mapper.TableMapper import TableMapper


class ColumnMapper:
    def __init__(self):
        self.column_list = None

    # def table_column_list(self, our_table_name):
    #     our_model = []
    #     table_model = self.table_obj.our_models[our_table_name]
    #     temporary_value = table_model._meta.get_fields()
    #     for item in temporary_value:
    #     # To Exclude Id, Client, Client Table Name From Client HTML Page
    #         if not str(item.name).__contains__('metamodel') and item.name !='client_table_name' and item.name != 'id':
    #             our_model.append(item.name)
    #     return our_model
