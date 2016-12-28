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
from mapper.models import *
import yaml


@shared_task
def test_combine():
    table = connect_to_this_database()
    try:
        query = create_fix_queries()
        print query
        table.cur.execute(query)
        table.conn.commit()
        return "SUCCESS"
    except Exception as e:
        print e
        table.conn.rollback()
        return None


@shared_task
def script_test():
    SCRIPT_PATH = os.path.join(settings.BASE_DIR, 'R_Scripts')
    with open(os.path.join(SCRIPT_PATH, 'RScriptTest.R'), 'w+') as f:
        f.writelines('load("/home/ubuntu/.RData")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'packages.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'utils.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'yml.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Connection.R')) + '")\n')
        
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/CLTV_Final_Event.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Churn_Event.R')) + '")\n')
        
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Primary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Secondary.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/Clustering_H2O.R')) + '")\n')

        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/CLTV_Final_Event_Score.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Churn_Event_Score.R')) + '")\n')
        
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R')) + '")\n')
        f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Customer/High_Convertors_Scoring.R')) + '")\n')
        
        f.writelines('save.image("/home/ubuntu/.RData")\n')
    return run()

def run():
    SCRIPT_PATH = os.path.join(settings.BASE_DIR, 'R_Scripts')
    command = ['Rscript', os.path.join(SCRIPT_PATH, 'RScriptTest.R')]
    return subprocess.call(command, universal_newlines=True)


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

        SCRIPT_PATH = os.path.join(settings.BASE_DIR, 'R_Scripts')
        status = make_yml(SCRIPT_PATH)
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


        with open(os.path.join(SCRIPT_PATH, 'RScript.R'), 'w+') as f:
            f.writelines('load("/home/ubuntu/.RData")\n')

            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'redirect_output.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'packages.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'utils.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'yml.R')) + '")\n')
            f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Connection.R')) + '")\n')

            # Training
            if is_event_log:
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/CLTV_Final_Event.R')) + '")\n')
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Churn_Event.R')) + '")\n')
                if is_customer_master:
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Primary.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/High_Convertors_Secondary.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Event/Customer/Clustering_H2O.R')) + '")\n')
            else:
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Trans/CLTV_Final_Trans.R')) + '")\n')
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Trans/Churn_Trans.R')) + '")\n')
                if is_customer_master:
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Primary.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Trans/Customer/High_Convertors_Secondary.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Training/Trans/Customer/Clustering_H2O.R')) + '")\n')

            # Scoring
            if is_event_log:
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/CLTV_Final_Event_Score.R')) + '")\n')
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Churn_Event_Score.R')) + '")\n')
                if is_customer_master:
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Customer/Clustering_H2O_Scoring.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Event/Customer/High_Convertors_Scoring.R')) + '")\n')
            else:
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Trans/CLTV_Final_Trans_Score.R')) + '")\n')
                f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Trans/Churn_Trans_Score.R')) + '")\n')
                if is_customer_master:
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Trans/Customer/Clustering_H2O_Scoring.R')) + '")\n')
                    f.writelines('source("' + str(os.path.join(SCRIPT_PATH, 'Scoring/Trans/Customer/High_Convertors_Scoring.R')) + '")\n')
            f.writelines('save.image("/home/ubuntu/.RData")\n')

        command = ['Rscript', os.path.join(script_path, 'RScript.R')]
        return subprocess.call(command, universal_newlines=True)
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


@shared_task
def combine_tables_when_r_finishes(task_id):
    status = TaskResult.objects.get_task(task_id)
    if status is None:
        return None
    print status.status
    try:
        if str(status.status) == 'PENDING':
            time.sleep(3600)
            combine_tables_when_r_finishes(task_id)
        elif str(status.status) == 'FAILURE':
            return None
        elif str(status.status) == 'SUCCESS':
            return combine()
    except Exception as e:
        print e
        time.sleep(3600)
        combine_tables_when_r_finishes(task_id)


def combine():
    table = connect_to_this_database()
    table_names = ['"Churn_Engagement"', 'cltv_value', 'high_conv', '"Predict_Period"', 'profile_clusters']
    try:
        for name in table_names:
            table.cur().execute('SELECT * FROM' + name + ' LIMIT 1')
    except Exception as e:
        print e
        if e.message.__contains__('relation'):
            table.conn.rollback()
            return 'SCRIPTS_RUN_TABLE_NONE'
        else:
            table.conn.rollback()
            return 'UNHANDLED_EXCEPTION'
    # This Means That All Tables Exists
    # now create master_view
    try:
        query = create_fix_queries()
        print query
        table.cur.execute(query)
        table.conn.commit()
        return 'SUCCESS'
    except Exception as e:
        print e
        table.conn.rollback()
        return None



def create_fix_queries():
    try:
        customer_master_mapping_obj = CustomerMasterMappingModel.objects.all()[0]
        customer_master = str(customer_master_mapping_obj.client_table_name)
        customer_master_cust_id = str(customer_master_mapping_obj.cust_id)

        customer_contact_mapping_obj = CustomerContactMappingModel.objects.all()[0]
        customer_contact = str(customer_contact_mapping_obj.client_table_name)
        customer_contact_cust_id = str(customer_contact_mapping_obj.cust_id)
        customer_contact_email_id = str(customer_contact_mapping_obj.email_id)
    except Exception as e:
        print e
        return None

    # FIX 0 Convert Churn_Engagement to churn_engagement To Remove Quotes Problem
    query = 'ALTER TABLE "Churn_Engagement" RENAME TO churn_engagement;'

    # FIX 1 If Team Master Already Exists Drop It
    query = query + "DROP TABLE IF EXISTS team_master_table;"

    # FIX 2 Create Master Table By Merging All Output Of Scoring + IDs From Customer Master Table
    query = query + "CREATE TABLE team_master_table AS"
    query = query + " (SELECT A."+customer_master_cust_id+", B.churn , B.engagement , C.cltv , C.value , D.high_conv , E.cluster"
    query = query + " FROM((SELECT "+customer_master_cust_id+" FROM "+customer_master+") A"
    query = query + " LEFT OUTER JOIN (SELECT cust,churn,engagement FROM churn_engagement) B ON B.cust = A."+customer_master_cust_id
    query = query + " LEFT OUTER JOIN (SELECT cust,cltv,value FROM cltv_value) C ON C.cust = A."+customer_master_cust_id
    query = query + " LEFT OUTER JOIN (SELECT cust,high_conv FROM high_conv) D ON D.cust = A."+customer_master_cust_id
    query = query + " LEFT OUTER JOIN (SELECT cust_id,CLUSTER FROM profile_clusters) E ON E.cust_id = A."+customer_master_cust_id+"));"

    # FIX 3 Change high_conv to high_convertor To Get Compatible With Personal
    query = query + 'ALTER TABLE team_master_table RENAME COLUMN high_conv to high_convertor;'

    # FIX 4 Change id to cust_id To Get Compatible With Personal
    query = query + 'ALTER TABLE team_master_table RENAME COLUMN id to cust_id;'

    # Now Create Personal Table
    # FIX 5
    query = query + 'DROP TABLE IF EXISTS team_personal;'

    # FIX 6 Change user_id data type to numeric because it will compared later with integer columns
    query = query + "ALTER TABLE contact ALTER COLUMN user_id TYPE NUMERIC USING user_id::NUMERIC;"

    # FIX 7 Create Personal Table By Merging Contact And Users
    query = query + "CREATE TABLE team_personal AS"
    query = query + " SELECT A."+customer_master_cust_id+", A.gender, A.age, A.country_code, B."+customer_contact_cust_id+", B."+customer_contact_email_id
    query = query + " FROM ((SELECT DISTINCT ON("+customer_master_cust_id+") "+customer_master_cust_id+", gender, AGE, country_code FROM "+customer_master+") A"
    query = query + " FULL OUTER JOIN (SELECT DISTINCT ON("+customer_contact_cust_id+") "+customer_contact_cust_id+", "+customer_contact_email_id+" FROM "+customer_contact+" where "+customer_contact_email_id+" <> '') B ON B."+customer_contact_cust_id+" = A."+customer_master_cust_id+");"

    # FIX 8 Change id to cu_id To Get Compatible With Amit's Code
    query = query + 'ALTER TABLE team_personal RENAME COLUMN id TO cu_id;'

    # FIX 9 Change country_code To country To Get Compatible With Amit's Code
    query = query + 'ALTER TABLE team_personal RENAME COLUMN country_code TO country;'

    # FIX 10 Change email to email_id To Get Compatible With Amit's Code
    query = query + 'ALTER TABLE team_personal RENAME COLUMN email TO email_id;'

    # FIX 11 Change user_id to name Because No Name Is Found( Remove Later Because Name Is Mandatory)
    query = query + 'ALTER TABLE team_personal RENAME COLUMN user_id TO name;'


    return query