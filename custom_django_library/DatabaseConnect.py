import psycopg2
from connect_client_db import models

class connect_to_client_database:
    def __init__(self):
        self.conn = None
        self.cur = None
        try:
            database_info = models.ClientDbModel.objects.all()[0]
            if database_info.database_type == 'PostgreSQL':
                self.conn = psycopg2.connect(
                    database=database_info.database_name,
                    user=database_info.usern,
                    password=database_info.passw,
                    host=database_info.host,
                    port=database_info.port,
                    sslmode='require'
                )
                self.cur = self.conn.cursor()
            else:
                pass
                # other type of database
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

class connect_to_this_database:
    def __init__(self):
        self.conn = None
        self.cur = None
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
