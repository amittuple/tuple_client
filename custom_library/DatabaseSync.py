import subprocess
from DatabaseInfo import DatabaseInfo
from DatabaseConnect import DatabaseConnect

class DatabaseSync:

    def _buffer_path(self):
        return '~/Table.buffer'

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

    def sync_status(self, db_source, db_destination, table_name):
        table_name = (table_name,)
        dest = DatabaseConnect()
        dest.connect(db_destination)
        src = DatabaseConnect()
        src.connect(db_source)

        if dest.isConnected() and src.isConnected():
            # Check If Source Has Table
            src.cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public' and table_name='" + str(
                    table_name[0]) + "';")
            result = src.cur.fetchone()
            if result is None:
                print 'Table ' + str(table_name[0]) +' Not Found In Source'
                return None

            dest.cur.execute(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='" + str(
                    table_name[0]) + "';")
            dest_result = dest.cur.fetchall()
            src.cur.execute(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='" + str(
                    table_name[0]) + "';")
            src_result = src.cur.fetchall()

            for dest_obj in dest_result:
                if dest_obj in src_result:
                    pass
                else:
                    print 'Error In Column'
                    print dest_obj
                    return None
            return True
        else:
            return None

    def sync(self, db_source, db_destination, table_name):

        dest = DatabaseConnect()
        dest.connect(db_destination)
        dest.cur.execute('DROP TABLE IF EXISTS ' + table_name)
        dest.conn.commit()

        if isinstance(db_source, DatabaseInfo) and isinstance(db_destination, DatabaseInfo):
            command = self._get_command(db_source, table_name)
            subprocess.call(command, shell=True)
            command = self._set_command(db_destination)
            subprocess.call(command, shell=True)
        else:
            raise Exception('Please Provide A DatabaseInfo Instance')
            return

    def sync_complete(self, db_source, db_destination, table_list):
        for table in table_list:
            if self.sync_status(db_source, db_destination, table) is None:
                print 'Cannot Proceed'
                return
        for table in table_list:
            self.sync(db_source, db_destination, table, )



# client_db = DatabaseInfo(
#     'postgres-client1.c3yxphqgag3s.ap-southeast-1.rds.amazonaws.com',
#     '5432',
#     'client1main',
#     'client1',
#     'client111'
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
# obj = DatabaseSync()
# obj.sync_complete(client_db, our_db, ['trans'])