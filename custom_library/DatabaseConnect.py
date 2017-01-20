from DatabaseInfo import DatabaseInfo
import psycopg2

class DatabaseConnect:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, database_info):
        if not isinstance(database_info, DatabaseInfo):
            raise Exception('Please Provide A DatabaseInfo Instance')
            return
        try:
            self.conn = psycopg2.connect(
                database=database_info.database,
                user=database_info.username,
                password=database_info.password,
                host=database_info.host,
                port=database_info.port,
                sslmode='require'
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print e
            return None

    def connect_local(self):
        try:
            self.conn = psycopg2.connect(
                database='postgres_db',
                user='postgres_user',
                password='admin',
                host='localhost',
                port='5432',
                sslmode='require'
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print e
            return None


    def isConnected(self):
        if self.conn:
            return True
        else:
            return False

    def conn(self):
        return self.conn

    def cur(self):
        return self.cur

# obj1 = DatabaseInfo(
#     'postgres-client1.c3yxphqgag3s.ap-southeast-1.rds.amazonaws.com',
#     '5432',
#     'client1main',
#     'client1',
#     'client111'
# )

# obj2 = DatabaseConnect()
# obj2.connect(obj1)
# print obj2.cur
