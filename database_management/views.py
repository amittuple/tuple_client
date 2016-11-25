from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from connect_client_db import models
import psycopg2
from ConnectDatabase import connect_to_client_database
from django.core.urlresolvers import reverse
from .tasks import add, database_migration
from django.contrib.auth.models import User


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
            create_query = 'CREATE TABLE ' + client_table_name + ' ( '
            insert_query = 'INSERT INTO ' + client_table_name + '('
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
        if d.has_key('ERROR'):
            print d['ERROR']
            return HttpResponseRedirect(reverse('transfer_failed'))
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



def transfer_failed(request):
    return render(request, 'database_management/transfer-failed.html', {})
