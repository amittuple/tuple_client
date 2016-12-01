from celery import shared_task, task
from ConnectDatabase import connect_to_client_database, connect_to_this_database
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
from django.contrib.auth.models import User
import StringIO
# app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def add(x,y):
    print x+y
    return x+y


@shared_task
def database_migration(queries, user):
    user = User.objects.filter(username=user)
    from_table = connect_to_client_database(user)
    # psycopg2
    to_table = connect_to_this_database()
    success_fail_arr = []
    for item in queries:
        try:
            print item['our_table_name']
            print item['create_query']
            print item['select_query']

            with open('TableBuffer.buffer', 'w+') as f:
                from_table.cur.copy_to(f, item['client_table_name'])
                f.seek(0)
                to_table.cur.execute(item['create_query'])
                to_table.cur.copy_from(f, item['client_table_name'])
                to_table.conn.commit()
            success_fail_arr.append({
                'table_name': item['our_table_name'],
                'result': 'success',
                'reason': 'none'
            })
            print success_fail_arr
        except Exception as e:
            print e
            # if e.message.__contains__('current transaction is aborted, commands ignored until end of transaction block'):
            to_table.conn.rollback()
            from_table.conn.rollback()
            success_fail_arr.append({
                'table_name': item['our_table_name'],
                'result': 'fail',
                'reason': e.message
            })
            continue

    from_table.cur.close()
    to_table.cur.close()

    return success_fail_arr

