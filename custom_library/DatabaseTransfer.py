import subprocess
from DatabaseInfo import DatabaseInfo
from DatabaseConnect import DatabaseConnect

class DatabaseTransfer:        

    def from_db(self, database_info):
        return database_info

    def to_db(self, database_info):
        return database_info

    def _buffer_path(self):
        return '/home/ubuntu/Table.buffer'

    def _get_command(self, db_source, table_name):
        command = "PGPASSWORD='" + db_source.password
        command = command + "' pg_dump -C -h " + db_source.host
        command = command + " -U " + db_source.username + " " + db_source.database + " -t " + table_name
        command = command + " --no-owner --no-acl > " + self._buffer_path()
        return command

    def _set_command(self, db_destination):
        command = "PGPASSWORD='" + db_destination.password
        command = command + "' psql -h " + db_destination.host
        command = command + " -U " + db_destination.username
        command = command + " " + db_destination.database + " < " + self._buffer_path()
        return command

    def transfer_table(self, db_source, db_destination, table_name):
        command = self._get_command(db_source, table_name)
        subprocess.call(command, shell=True)
        command = self._set_command(db_destination)
        subprocess.call(command, shell=True)

    def transfer_table_in_schema(self, db_source, db_destination, schema):
        obj = DatabaseConnect()
        obj.connect(db_source)
        if obj.isConnected():
            obj.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='"+schema+"'")
            results = obj.cur.fetchall()
            if results is not None:
                for table_name in results:
                    table_name = str(table_name[0])
                    command = self._get_command(db_source, table_name)
                    subprocess.call(command, shell=True)
                    command = self._set_command(db_destination)
                    subprocess.call(command, shell=True)



# client_db = DatabaseInfo(
#     'postgres-client1.c3yxphqgag3s.ap-southeast-1.rds.amazonaws.com',
#     '5432',
#     'client1main',
#     'client1',
#     'client111'
# )

# client_db = DatabaseInfo(
#     '54.254.180.50',
#     '5432',
#     'postgres_db',
#     'postgres_user',
#     'admin'
# )
#
# our_db = DatabaseInfo(
#     'localhost',
#     '5432',
#     'postgres_db',
#     'postgres_user',
#     'admin'
# )
#
# obj = DatabaseTransfer()
#
#
# obj.transfer_table_in_schema(client_db, our_db, 'public')