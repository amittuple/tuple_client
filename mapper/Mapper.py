from mapper.TableMapper import TableMapper
# from mapper.ColumnMapper import ColumnMapper


class Mapper(TableMapper):
    def __init__(self):
        temp = TableMapper(self)
        print temp.tables()

    def mapping_exists(self):
        pass

    def clear_mapping_models(self):
        pass

    def clear_mapping_session(self):
        pass

    def columns_in_tables(self):
        pass

    def prepare_our_model(self):
        pass

    def prepare_client_model(self):
        pass

    def map(self):
        pass


    # def mapping_exists(self):
    #     try:
    #         for our_table_name, our_table_model in get_table_name_model_pair().iteritems():
    #             table_obj = our_table_model.objects.all()
    #             if len(table_obj) != 0:
    #                 return True
    #         return False
    #     except Exception as e:
    #         print e
    #         return None



