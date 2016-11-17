from celery import shared_task, task
from ConnectDatabase import connect_to_client_database
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
from django.contrib.auth.models import User
from rowstextio.rowstextio import RowsTextIO
import StringIO
# app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def add(x,y):
    print x+y
    return x+y

# @shared_task
# def database_migration(column_map, user):
#     user = User.objects.filter(username=user)
#     from_table = connect_to_client_database(user)
#     to_table = connect_to_client_database(user)
#     success_fail_arr = []
#     for our_table_name in column_map:
#         select_query = 'SELECT '
#         create_query = 'CREATE TABLE ' + 'temp' + our_table_name + ' ( '
#         insert_query = 'INSERT INTO ' + 'temp' + our_table_name + '('
#         counter = 0
#         insert_placeholder = ''
#         for client_table_name, our_column_dict in column_map[our_table_name].iteritems():
#             columns = ()
#             for our_column_name, client_column_dict in our_column_dict.iteritems():
#                 if client_column_dict != None:
#                     for client_column_name in client_column_dict:
#                         print client_column_name
#                         columns = columns + (str(client_column_name),)
#                         counter += 1
#                         select_query = select_query + client_column_name + ','
#                         create_query = create_query + ' ' + client_column_name + ' ' + client_column_dict[client_column_name]['type'] + ','
#                         insert_query = insert_query + client_column_name + ','
#                         insert_placeholder += '%s,'
#         select_query = select_query[:-1]
#         create_query = create_query[:-1]
#         insert_query = insert_query[:-1]
#         print columns
#         insert_placeholder = insert_placeholder[:-1]
#         if counter > 0:
#             select_query = select_query + ' FROM ' + client_table_name
#             create_query += ' )'
#             # insert_query = insert_query + ') VALUES ( ' + insert_placeholder + ' ) RETURNING *'
#             print select_query
#             print create_query
#
#             try:
#                 # Extract Data And Write To File
#                 # select_query
#                 # columns
#                 # create_query
#                 # our_table_name
#                 # client_table_name
#
#                 from_table.cur.execute(select_query)
#                 data = from_table.cur.fetchall()
#                 if data:
#                     print our_table_name
#                 f = open(our_table_name + '.txt', 'w')
#                 from_table.cur.copy_to(f, client_table_name, columns=columns)
#                 f.close()
#
#                 # Open File And Write To Database
#                 f = open(our_table_name + '.txt', 'r')
#                 to_table.cur.execute(create_query)
#                 to_table.cur.copy_from(f, 'temp' + our_table_name)
#                 to_table.conn.commit()
#                 f.close()
#
#                 # clear file
#                 f = open(our_table_name + '.txt', 'w')
#                 f.seek(0)
#                 f.truncate()
#
#                 success_fail_arr.append({
#                     'table_name': our_table_name,
#                     'result': 'success',
#                     'reason': 'none'
#                 })
#                 print success_fail_arr
#                 f.close()
#
#             except IOError as e:
#                 print e
#             except Exception as e:
#                 if e.message.__contains__('already exists'):
#                     success_fail_arr.append({
#                         'table_name': our_table_name,
#                         'result': 'fail',
#                         'reason': 'Already Exists'
#                     })
#                     # clear file
#                     f.seek(0)
#                     f.truncate()
#                     f.close()
#                     print 'already exists'
#                 if e.message.__contains__('out of memory'):
#                     success_fail_arr.append({
#                         'table_name': our_table_name,
#                         'result': 'fail',
#                         'reason': 'out of memory'
#                     })
#                     # clear file
#                     f.seek(0)
#                     f.truncate()
#                     f.close()
#                     print 'Too Much Data'
#                 else:
#                     print e
#         else:
#             print 'No Column Mapped For '+ our_table_name
#     print 'Successfully Completed'
#     return success_fail_arr




# @shared_task
# def database_migration(queries, user):
#     user = User.objects.filter(username=user)
#     from_table = connect_to_client_database(user)
#     to_table = connect_to_client_database(user)
#     success_fail_arr = []
#     for item in queries:
#         try:
#             print item['our_table_name']
#             print item['create_query']
#             print item['select_query']
#             f = RowsTextIO(from_table.cur, item['select_query'] + ' limit 1000')
#             to_table.cur.execute(item['create_query'])
#             to_table.cur.copy_expert('COPY ' + 'temp' + item['client_table_name'] + ' FROM STDIN CSV', f)
#             to_table.conn.commit()
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'success',
#                 'reason': 'none'
#             })
#             print success_fail_arr
#
#             # from_table.set_session(isolation_level=ISOLATION_LEVEL_SERIALIZABLE)
#             # from_table.cur.execute(item['select_query'])
#             # f = StringIO.StringIO()
#             # from_table.cur.copy_expert('COPY ( '+ item['select_query'] +' ) TO STDOUT', f, size=8192)
#             # to_table.cur.execute(item['create_query'])
#             # f.seek(0)
#             # to_table.cur.copy_from(f, 'temp' + item['our_table_name'])
#             # to_table.conn.commit()
#             # f.seek(0)
#             # f.truncate()
#             # f.close()
#             # print 'END'
#
#
#             # from_table.cur.execute(item['select_query'])
#             # from_table.cur.fetchall()
#             # f = StringIO.StringIO()
#             # # f = open(item['our_table_name'] + '.txt', 'w+')
#             # from_table.cur.copy_to(f, item['client_table_name'], columns=item['columns'])
#             # to_table.cur.execute(item['create_query'])
#             # # seek(0) to return file cursor to top otherwise it will read empty
#             # f.seek(0)
#             # to_table.cur.copy_from(f, 'temp' + item['our_table_name'])
#             # to_table.conn.commit()
#             # success_fail_arr.append({
#             #     'table_name': item['our_table_name'],
#             #     'result': 'success',
#             #     'reason': 'none'
#             # })
#             # print success_fail_arr
#             # f.seek(0)
#             # f.truncate()
#             # f.close()
#             # print 'END'
#         except Exception as e:
#             print e
#             to_table.conn.rollback()
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'fail',
#                 'reason': e.message
#             })
#             # if not f.closed:
#             #     f.seek(0)
#             #     f.truncate()
#             #     f.close()
#             continue
#
#     from_table.cur.close()
#     to_table.cur.close()
#
#     return success_fail_arr


# def table_next(table, query, buffer):
#     offset = 0
#     from_table.cur.execute(item['select_query'] + ' offset ' + offset + ' limit ' + limit )

@shared_task
def database_migration(queries, user):
    user = User.objects.filter(username=user)
    from_table = connect_to_client_database(user)
    to_table = connect_to_client_database(user)
    success_fail_arr = []
    for item in queries:
        try:
            print item['our_table_name']
            print item['create_query']
            print item['select_query']

            f = open('TableBuffer.buffer', 'w+')
            from_table.cur.copy_to(f, item['client_table_name'], columns=item['columns'])
            f.seek(0)
            to_table.cur.execute(item['create_query'])
            to_table.cur.copy_from(f, 'temp'+ item['client_table_name'])
            to_table.conn.commit()
            success_fail_arr.append({
                'table_name': item['our_table_name'],
                'result': 'success',
                'reason': 'none'
            })
            print success_fail_arr
            if not f.closed:
                f.seek(0)
                f.truncate()
                f.close()
            print 'END'
        except Exception as e:
            print e
            to_table.conn.rollback()
            success_fail_arr.append({
                'table_name': item['our_table_name'],
                'result': 'fail',
                'reason': e.message
            })
            if not f.closed:
                f.seek(0)
                f.truncate()
                f.close()
            continue

    from_table.cur.close()
    to_table.cur.close()

    return success_fail_arr

# def database_migration(queries, user):
#     user = User.objects.filter(username=user)
#     from_table = connect_to_client_database(user)
#     to_table = connect_to_client_database(user)
#     success_fail_arr = []
#     for item in queries:
#         try:
#             print item['our_table_name']
#             print item['create_query']
#             print item['select_query']
#
#             offset = 0
#             limit = 100
#             print item['select_query'] + ' offset ' + str(offset) + ' limit ' + str(limit)
#
#             # Bugging Purpose
#             # item['select_query'] = 'select row_number() OVER () as id from transaction_master'
#
#             from_table.cur.execute(item['select_query'] + ' offset ' + str(offset) + ' limit ' + str(limit))
#             to_table.cur.execute(item['create_query'])
#             print 'Looping Start'
#             row = from_table.cur.fetchall()
#             i = 1
#             while row:
#                 # print row
#                 f = open('temp-' + str(i) + item['our_table_name'] + '.txt', 'w+')
#                 from_table.cur.copy_to(f, item['client_table_name'], columns=item['columns'])
#                 # seek(0) to return file cursor to top otherwise it will read empty
#                 f.seek(0)
#                 # to_table.cur.copy_from(f, 'temp' + item['our_table_name'])
#                 offset+= 100
#                 # limit = 100
#                 # f.seek(0)
#                 # f.truncate()
#                 f.close()
#                 print item['select_query'] + ' offset ' + str(offset) + ' limit ' + str(limit)
#                 from_table.cur.execute(item['select_query'] + ' offset ' + str(offset) + ' limit ' + str(limit) )
#                 row = from_table.cur.fetchall()
#                 i+=1
#             to_table.conn.commit()
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'success',
#                 'reason': 'none'
#             })
#             print success_fail_arr
#             if not f.closed:
#                 f.seek(0)
#                 f.truncate()
#                 f.close()
#             print 'END'
#         except Exception as e:
#             print e
#             to_table.conn.rollback()
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'fail',
#                 'reason': e.message
#             })
#             if not f.closed:
#                 f.seek(0)
#                 f.truncate()
#                 f.close()
#             continue
#
#     from_table.cur.close()
#     to_table.cur.close()
#
#     # return success_fail_arr
