from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from connect_client_db import models
import psycopg2
from ConnectDatabase import connect_to_client_database
from django.core.urlresolvers import reverse
from .tasks import database_migration, r_process
from django.contrib.auth.models import User
import yaml
import json
from mapper.views import get_table_name_model_pair, get_table_name_model_meta_pair, clear_mapping_session
import os

def create_queries_pool(column_map, client_table_structure):
    queries = []
    reverse_table_map = {}
    for our_table_name in column_map.keys():
        if column_map[our_table_name].keys()[0] == 'is_factor':
            client_table_name = column_map[our_table_name].keys()[1]
        else:
            client_table_name = column_map[our_table_name].keys()[0]
        reverse_table_map[client_table_name] = our_table_name

    for client_table_name, client_column_dict in client_table_structure.iteritems():
        select_query = 'SELECT '
        counter = 0
        insert_placeholder = ''
        create_query = 'CREATE TABLE ' + client_table_name + ' ( '
        insert_query = 'INSERT INTO ' + client_table_name + ' ( '
        columns = ()
        if client_column_dict is not None:
            for client_column_name in client_column_dict:
                create_query = create_query + ' ' + client_column_name + ' ' + client_column_dict[client_column_name]['type'] + ','
                columns = columns + (str(client_column_name),)
                counter += 1
                select_query = select_query + client_column_name + ','
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
            print reverse_table_map[client_table_name]
            print select_query
            print create_query
            print insert_query
            queries.append({
                'our_table_name': reverse_table_map[client_table_name],
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
        client_table_structure = request.session['client_table_structure']
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
        queries_pool = create_queries_pool(column_map, client_table_structure)
        task_id = database_migration.delay(queries_pool, str(user))
        r_process.delay(str(task_id))
        # make_yml()
        # clear_mapping_session(request)
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


def make_yml(file_url):
    try:
        final_map = {}
        final_map['table_map'] = {}
        final_map['column_map'] = {}
        final_map['is_factor'] = {}
        final_map['DATABASE'] = {
            'NAME': 'postgres_db',
            'HOST': 'localhost',
            'USER': 'postgres_user',
            'PASSWORD': 'admin',
            'PORT': '5432'
        }
        mapping_id = None
        for table_name, table_model in get_table_name_model_pair().iteritems():
            table_obj = table_model.objects.all()
            if len(table_obj) != 0:
                table_obj = table_obj[0]
                mapping_id = table_obj.id
                final_map['table_map'][table_name] = table_obj.client_table_name
                final_map['column_map'][table_name] = {}
                table_fields = table_model._meta.get_fields()
                for item in table_fields:
                    # To Exclude Id, Client, Client Table Name From Client HTML Page
                    if not str(item.name).__contains__('metamodel') and item.name !='client_table_name' and item.name != 'id':
                        final_map['column_map'][table_name][item.name] = getattr(table_obj, item.name)


                final_map['is_factor'][table_name] = []
                table_meta_model = get_table_name_model_meta_pair()[table_name]
                table_meta_obj = table_meta_model.objects.filter(mapping_id=mapping_id)
                if len(table_meta_obj) != 0:
                    for row in table_meta_obj:
                        if row.is_factor:
                            final_map['is_factor'][table_name].append(row.column_name)


        with open(os.path.join(file_url, 'MappingBuffer.yml'), 'w+') as yml_file:
            yaml.safe_dump(final_map, yml_file, default_flow_style=False)
        return True
    except Exception as e:
        print e
        return False




def prepare_all_model(table_map):
    our_model = {}

    table_name_model_pair = get_table_name_model_pair()

    for our_table_name, table_model in table_name_model_pair.iteritems():
        temporary_value = table_model._meta.get_fields()
        mapping_name = our_table_name
        our_model[mapping_name] = []
        for item in temporary_value:
            # To Exclude Id, Client, Client Table Name From Client HTML Page
            if not str(item.name).__contains__('metamodel') and item.name !='client_table_name' and item.name != 'id':
                our_model[mapping_name].append(item.name)
    return our_model
