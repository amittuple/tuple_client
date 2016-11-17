from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from connect_client_db import models
import psycopg2
from ConnectDatabase import connect_to_client_database
from django.core.urlresolvers import reverse
from .tasks import add, database_migration
from django.contrib.auth.models import User
# Create your views here.


# Create SQL Queries To Transfer Database
# def database_migration(column_map, from_table, to_table):
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
#
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
#                 from_table.cur.execute(select_query)
#                 data = from_table.cur.fetchall()
#                 if data:
#                     print our_table_name
#                 f = open(our_table_name+'.txt', 'w')
#                 from_table.cur.copy_to(f, client_table_name, columns=columns)
#                 f.close()
#
#                 # Open File And Write To Database
#                 f = open(our_table_name+'.txt', 'r')
#                 to_table.cur.execute(create_query)
#                 to_table.cur.copy_from(f, 'temp'+our_table_name)
#                 to_table.conn.commit()
#                 f.close()
#             except Exception as e:
#                 print e
#         else:
#             print 'No Column Mapped For '+ our_table_name


# Create SQL Queries To Transfer
# def database_migration(queries, user):
#     try:
#         user = User.objects.filter(username=user)
#         from_table = connect_to_client_database(user)
#         to_table = connect_to_client_database(user)
#         success_fail_arr = []
#         for item in queries:
#             print item['our_table_name']
#             print item['create_query']
#             print item['select_query']
#             from_table.cur.execute(item['select_query'])
#             from_table.cur.fetchall()
#             f = open(item['our_table_name'] + '.txt', 'w')
#             from_table.cur.copy_to(f, item['client_table_name'], columns=item['columns'])
#             f.close()
#
#             # Open File And Write To Database
#             f = open(item['our_table_name'] + '.txt', 'r')
#             to_table.cur.execute(item['create_query'])
#             to_table.cur.copy_from(f, 'temp' + item['our_table_name'])
#             to_table.conn.commit()
#             f.close()
#             # clear file
#             f = open(item['our_table_name'] + '.txt', 'w')
#             f.seek(0)
#             f.truncate()
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'success',
#                 'reason': 'none'
#             })
#             print success_fail_arr
#             f.close()
#
#     except IOError as e:
#         print e
#     except Exception as e:
#         if e.message.__contains__('already exists'):
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'fail',
#                 'reason': 'Already Exists'
#             })
#             # clear file
#             f.seek(0)
#             f.truncate()
#             f.close()
#             print 'already exists'
#         if e.message.__contains__('out of memory'):
#             success_fail_arr.append({
#                 'table_name': item['our_table_name'],
#                 'result': 'fail',
#                 'reason': 'out of memory'
#             })
#             # clear file
#             f.seek(0)
#             f.truncate()
#             f.close()
#             print 'Too Much Data'
#         else:
#             print e
#
#
#     # for our_table_name in column_map:
#     #         try:
#     #             # Extract Data And Write To File
#     #             from_table.cur.execute(select_query)
#     #             data = from_table.cur.fetchall()
#     #             if data:
#     #                 print our_table_name
#     #             f = open(our_table_name+'.txt', 'w')
#     #             from_table.cur.copy_to(f, client_table_name, columns=columns)
#     #             f.close()
#     #
#     #             # Open File And Write To Database
#     #             f = open(our_table_name+'.txt', 'r')
#     #             to_table.cur.execute(create_query)
#     #             to_table.cur.copy_from(f, 'temp'+our_table_name)
#     #             to_table.conn.commit()
#     #             f.close()
#     #         except Exception as e:
#     #             print e
#     #     else:
#             print 'No Column Mapped For '+ our_table_name

def create_queries_pool(column_map):
    queries = []
    for our_table_name in column_map:
        print
        select_query = 'SELECT '
        counter = 0
        insert_placeholder = ''
        for client_table_name, our_column_dict in column_map[our_table_name].iteritems():
            # These Query Will be Executed Once As This For Loop Will Be Executed Once
            # There Is A Fix To Remove For Loop
            create_query = 'CREATE TABLE ' + 'temp' + client_table_name + ' ( '
            insert_query = 'INSERT INTO ' + 'temp' + client_table_name + '('
            columns = ()
            for our_column_name, client_column_dict in our_column_dict.iteritems():
                if client_column_dict != None:
                    for client_column_name in client_column_dict:
                        print client_column_name
                        columns = columns + (str(client_column_name),)
                        counter += 1
                        select_query = select_query + client_column_name + ','
                        create_query = create_query + ' ' + client_column_name + ' ' + client_column_dict[client_column_name]['type'] + ','
                        insert_query = insert_query + client_column_name + ','
                        insert_placeholder += '%s,'
        select_query = select_query[:-1]
        create_query = create_query[:-1]
        insert_query = insert_query[:-1]
        print columns
        insert_placeholder = insert_placeholder[:-1]
        if counter > 0:
            select_query = select_query + ' FROM ' + client_table_name
            create_query += ' )'
            insert_query = insert_query + ') VALUES ( ' + insert_placeholder + ' ) RETURNING *'
            print select_query
            print create_query
            print insert_query
            queries.append({
                'our_table_name': our_table_name,
                'client_table_name': client_table_name,
                'select_query': select_query,
                'create_query': create_query,
                'insert_query': insert_query,
                'columns': columns
            })
    return queries

def celery_and_rabbit_server_check():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            d = { ERROR_KEY: 'No running Celery workers were found.' }
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the RabbitMQ server is running.'
        d = { ERROR_KEY: msg }
    except ImportError as e:
        d = { ERROR_KEY: str(e)}

    return d

def transfer_database(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    try:
        transfer_database_flag = request.session['transfer_database_flag']
        if not transfer_database_flag:
            raise KeyError
    except KeyError as e:
        print "First You Have To Review Your Database Transfer"
        return HttpResponseRedirect(reverse('mapping_review'))
    del request.session['transfer_database_flag']
    user = request.user
    try:
        d = celery_and_rabbit_server_check()
        print d
        column_map = request.session['column_map']
        # first create list of queries
        # transfer database for each query
        queries_pool = create_queries_pool(column_map)
        database_migration.delay(queries_pool, str(user))
        # database_migration.delay(column_map, str(user))
    except KeyError as e:
        print e
        print 'No Mapping Found Please Do Mapping Before'
        return HttpResponseRedirect(reverse('table_mapping'))
    except Exception as e:
        print e
        return HttpResponse(e)
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, 'database_management/transfer-database.html', {})
