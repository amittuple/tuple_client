from celery import shared_task
from ConnectDatabase import connect_to_client_database, connect_to_this_database
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult
import subprocess
import time

import os
from tuple_client import settings

import ast

from mapper.views import get_table_name_model_meta_pair, get_table_name_model_pair
import yaml



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
                from_table.cur.copy_to(f, item['client_table_name'], columns=item['columns'])
                print 'copied to file'
                f.seek(0)
                to_table.cur.execute(item['create_query'])
                print 'created table'
                to_table.cur.copy_from(f, item['client_table_name'], columns=item['columns'])
                print 'insert into table'
                to_table.conn.commit()
                print 'commit'
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


@shared_task
def r_process(task_id):
    status = TaskResult.objects.get_task(task_id)
    if status is None:
        return None
    print status.status
    try:
        if str(status.status) == 'PENDING':
            time.sleep(60)
            r_process(task_id)
        elif str(status.status) == 'FAILURE':
            return None
        elif str(status.status) == 'SUCCESS':
            return r_execute(task_id)
    except Exception as e:
        print e
        time.sleep(60)
        r_process(task_id)


def r_execute(task_id):
    try:
        status = TaskResult.objects.get_task(task_id)
        result = ast.literal_eval(status.result)
        print result
        if result is None or result == '':
            return None
        for table in result:
            if table.has_key('table_name'):
                if table['table_name'] == 'TRANSACTION_MASTER':
                    if table['result'] == 'fail':
                        return None

        # Means Transaction Master Exists

        script_path = os.path.join(settings.BASE_DIR, 'R_Scripts')
        status = make_yml(script_path)
        if not status:
            return None

        # R Program
        is_event_log = False
        is_customer_master = False
        for table in result:
            if table.has_key('table_name'):
                if table['table_name'] == 'EVENT_LOG' and table['result'] == 'success':
                    is_event_log = True
                if table['table_name'] == 'CUSTOMER_MASTER' and table['result'] == 'success':
                    is_customer_master = True

        command = ['Rscript', os.path.join(script_path, 'Connection.R')]
        subprocess.call(command, universal_newlines=True)

        # Training
        if is_event_log:
            command = ['Rscript', os.path.join(script_path, 'Training/Event/CLTV_Final_Event.R')]
            subprocess.call(command, universal_newlines=True)
            command = ['Rscript', os.path.join(script_path, 'Training/Event/Churn_Event.R')]
            subprocess.call(command, universal_newlines=True)
            if is_customer_master:
                command = ['Rscript', os.path.join(script_path, 'Training/Event/Customer/High_Convertors_Primary.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Training/Event/Customer/High_Convertors_Secondary.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Training/Event/Customer/Clustering_H2O.R')]
                subprocess.call(command, universal_newlines=True)
        else:
            command = ['Rscript', os.path.join(script_path, 'Training/Trans/CLTV_Final_Trans.R')]
            subprocess.call(command, universal_newlines=True)
            command = ['Rscript', os.path.join(script_path, 'Training/Trans/Churn_Trans.R')]
            subprocess.call(command, universal_newlines=True)
            if is_customer_master:
                command = ['Rscript', os.path.join(script_path, 'Training/Trans/Customer/High_Convertors_Primary.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Training/Trans/Customer/High_Convertors_Secondary.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Training/Trans/Customer/Clustering_H2O.R')]
                subprocess.call(command, universal_newlines=True)

        # Scoring
        if is_event_log:
            command = ['Rscript', os.path.join(script_path, 'Scoring/Event/CLTV_Final_Event_Score.R')]
            subprocess.call(command, universal_newlines=True)
            command = ['Rscript', os.path.join(script_path, 'Scoring/Event/Churn_Event_Score.R')]
            subprocess.call(command, universal_newlines=True)
            if is_customer_master:
                command = ['Rscript', os.path.join(script_path, 'Scoring/Event/Customer/High_Convertors_Scoring.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R')]
                subprocess.call(command, universal_newlines=True)
        else:
            command = ['Rscript', os.path.join(script_path, 'Scoring/Trans/CLTV_Final_Trans_Score.R')]
            subprocess.call(command, universal_newlines=True)
            command = ['Rscript', os.path.join(script_path, 'Scoring/Trans/Churn_Trans_Score.R')]
            subprocess.call(command, universal_newlines=True)
            if is_customer_master:
                command = ['Rscript', os.path.join(script_path, 'Scoring/Trans/Customer/High_Convertors_Scoring.R')]
                subprocess.call(command, universal_newlines=True)
                command = ['Rscript', os.path.join(script_path, 'Scoring/Trans/Customer/Clustering_H2O_Scoring.R')]
                subprocess.call(command, universal_newlines=True)
        return 'SUCCESS'
    except Exception as e:
        print e
        return None


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
