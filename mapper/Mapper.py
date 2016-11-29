from mapper.TableMapper import TableMapper
# from mapper.ColumnMapper import ColumnMapper


class Mapper(TableMapper):
    def __init__(self):
        self.TableMapper = TableMapper()

    def extract_table_names_from_client_database(self, cursor):
        list_of_tables = []
        cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='public'")
        list_of_tables_temp = cursor.fetchall()
        for temp in list_of_tables_temp:
            for item in temp:
                list_of_tables.append(item)
        return list_of_tables

    def prepare_our_model(self):
        return self.TableMapper.tables()






temp = Mapper()
