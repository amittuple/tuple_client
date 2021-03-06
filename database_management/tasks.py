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
def add(x,y):
    sum = x+y
    print sum
    return sum

@shared_task
def test_combine():
    table = connect_to_this_database()
    try:
        result = combine()
        return result
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

        command = ['Rscript', os.path.join(SCRIPT_PATH, 'RScript.R')]
        subprocess.call(command, universal_newlines=True)
        return combine()
    except Exception as e:
        print e
        print 'here'
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

def combine():
    table = connect_to_this_database()
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
        customer_master_mapping_obj = CustomerMasterMappingModel.objects.all()
        if len(customer_master_mapping_obj) != 0:
            customer_master_mapping_obj = CustomerMasterMappingModel.objects.all()[0]
            if customer_master_mapping_obj.cust_id == '' or customer_master_mapping_obj.cust_id == None:
                customer_master_mapping_obj = TransactionMasterMappingModel.objects.all()[0]
            else:
                customer_master_mapping_obj = CustomerMasterMappingModel.objects.all()[0]
        else:
            customer_master_mapping_obj = TransactionMasterMappingModel.objects.all()[0]

        customer_master = str(customer_master_mapping_obj.client_table_name)
        customer_master_cust_id = str(customer_master_mapping_obj.cust_id)

        customer_contact_mapping_obj = CustomerContactMappingModel.objects.all()
        if len(customer_contact_mapping_obj) != 0:
            customer_contact_mapping_obj = CustomerContactMappingModel.objects.all()[0]
            if customer_contact_mapping_obj.cust_id == '' or customer_contact_mapping_obj.cust_id == None:
                customer_contact_mapping_obj = TransactionMasterMappingModel.objects.all()[0]
                customer_contact_email_id = None
                customer_contact_phone_number = None
                customer_contact_firstname = None
                customer_contact_lastname = None
            else:
                customer_contact_mapping_obj = CustomerContactMappingModel.objects.all()[0]
                customer_contact_phone_number = str(customer_contact_mapping_obj.phone_number)
                customer_contact_email_id = str(customer_contact_mapping_obj.email_id)

                if customer_contact_mapping_obj.firstname == '' or customer_contact_mapping_obj.firstname == None:
                    customer_contact_firstname = None
                else:
                    customer_contact_firstname = customer_contact_mapping_obj.firstname


                if customer_contact_mapping_obj.lastname == '' or customer_contact_mapping_obj.lastname == None:
                    customer_contact_lastname = None
                else:
                    customer_contact_lastname = customer_contact_mapping_obj.lastname
        else:
            customer_contact_mapping_obj = TransactionMasterMappingModel.objects.all()[0]
            customer_contact_email_id = None
            customer_contact_phone_number = None
            customer_contact_firstname = None
            customer_contact_lastname = None

        customer_contact = str(customer_contact_mapping_obj.client_table_name)
        customer_contact_cust_id = str(customer_contact_mapping_obj.cust_id)

        customer_master_obj = {
            'customer_master': customer_master,
            'cust_id': customer_master_cust_id,
        }
        customer_contact_obj = {
            'customer_contact': customer_contact,
            'cust_id': customer_contact_cust_id,
            'email_id': customer_contact_email_id,
            'phone_number': customer_contact_phone_number,
            'firstname': customer_contact_firstname,
            'lastname': customer_contact_lastname
        }
        print 'customer_master'
        print customer_master_obj
        print 'customer_contact'
        print customer_contact_obj

    except Exception as e:
        print e
        return None

    # FIX 0 Create Empty R Tables If Tables Are Not Already There
    create_r_tables(customer_master, customer_master_cust_id)

    # FIX 1 If Team Master Already Exists Drop It
    query = "DROP TABLE IF EXISTS master_table;"

    # FIX 2.1 ALTER TYPES
    query = query + 'ALTER TABLE cltv_value ALTER COLUMN cust TYPE TEXT USING cust::TEXT;'
    query = query + 'ALTER TABLE churn_engagement ALTER COLUMN cust TYPE TEXT USING cust::TEXT;'
    query = query + 'ALTER TABLE high_conv ALTER COLUMN cust TYPE TEXT USING cust::TEXT;'
    query = query + 'ALTER TABLE profile_clusters ALTER COLUMN cust_id TYPE TEXT USING cust_id::TEXT;'


    # FIX 2 REWRITTEN
    query = query + "CREATE TABLE master_table ( cust_id TEXT, churn DECIMAL DEFAULT NULL, engagement TEXT DEFAULT NULL, percent_churn DECIMAL DEFAULT NULL, cltv DECIMAL DEFAULT NULL, value TEXT DEFAULT NULL, percent_cltv DECIMAL DEFAULT NULL, high_conv TEXT DEFAULT NULL, cluster DECIMAL );"
    query = query + "INSERT INTO master_table (cust_id) SELECT DISTINCT "+customer_master_cust_id+" FROM "+customer_master+";"
    query = query + "UPDATE master_table SET churn = c.churn FROM churn_engagement as c WHERE master_table.cust_id = c.cust;"
    query = query + "UPDATE master_table SET engagement = c.engagement FROM churn_engagement as c WHERE master_table.cust_id = c.cust;"
    query = query + "UPDATE master_table SET percent_churn = c.percent_churn FROM churn_engagement as c WHERE master_table.cust_id = c.cust;"
    query = query + "UPDATE master_table SET cltv = cv.cltv FROM cltv_value as cv WHERE master_table.cust_id = cv.cust;"
    query = query + "UPDATE master_table SET value = cv.value FROM cltv_value as cv WHERE master_table.cust_id = cv.cust;"
    query = query + "UPDATE master_table SET percent_cltv = cv.percent_cltv FROM cltv_value as cv WHERE master_table.cust_id = cv.cust;"
    query = query + "UPDATE master_table SET high_conv = h.high_conv FROM high_conv as h WHERE master_table.cust_id = h.cust;"
    query = query + "UPDATE master_table SET cluster = cr.cluster FROM profile_clusters as cr WHERE master_table.cust_id = cr.cust_id;"

    # FIX 2 Create Master Table By Merging All Output Of Scoring + IDs From Customer Master Table
    # query = query + "CREATE TABLE master_table AS"
    # query = query + " (SELECT A."+customer_master_cust_id+", B.churn , B.engagement, B.percent_churn, C.cltv , C.value, C.percent_cltv, D.high_conv , E.cluster"
    # query = query + " FROM((SELECT "+customer_master_cust_id+" FROM "+customer_master+") A"
    # query = query + " LEFT OUTER JOIN (SELECT cust,churn,engagement,percent_churn FROM churn_engagement) B ON B.cust = A."+customer_master_cust_id
    # query = query + " LEFT OUTER JOIN (SELECT cust,cltv,value,percent_cltv FROM cltv_value) C ON C.cust = A."+customer_master_cust_id
    # query = query + " LEFT OUTER JOIN (SELECT cust,high_conv FROM high_conv) D ON D.cust = A."+customer_master_cust_id
    # query = query + " LEFT OUTER JOIN (SELECT cust_id,cluster FROM profile_clusters) E ON E.cust_id = A."+customer_master_cust_id+"));"

    # FIX 3 Change high_conv to high_convertor To Get Compatible With Personal
    query = query + 'ALTER TABLE master_table RENAME COLUMN high_conv to high_convertor;'

    # # FIX 4 Change id to cust_id To Get Compatible With Personal
    # query = query + 'ALTER TABLE master_table RENAME COLUMN ' + customer_master_cust_id + ' to cust_id;'

    # FIX 4.1 Change Type Of id TO TEXT
    query = query + 'ALTER TABLE master_table ALTER COLUMN cust_id TYPE TEXT USING cust_id::TEXT;'


    # Now Create Personal Table
    query = query + create_personal_table(customer_master_obj, customer_contact_obj)

    # FIX 5
    # query = query + 'DROP TABLE IF EXISTS personal_table;'

    # FIX 6 Change user_id data type to numeric because it will compared later with integer columns
    # query = query + "ALTER TABLE contact ALTER COLUMN user_id TYPE NUMERIC USING user_id::NUMERIC;"

    # FIX 7 Create Personal Table By Merging Contact And Users
    # query = query + "CREATE TABLE personal_table AS"
    # query = query + " SELECT A."+customer_master_cust_id+", A.gender, A.age, A.country_code, B."+customer_contact_cust_id+", B."+customer_contact_email_id
    # query = query + " FROM ((SELECT DISTINCT ON("+customer_master_cust_id+") "+customer_master_cust_id+", gender, AGE, country_code FROM "+customer_master+") A"
    # query = query + " FULL OUTER JOIN (SELECT DISTINCT ON("+customer_contact_cust_id+") "+customer_contact_cust_id+", "+customer_contact_email_id+" FROM "+customer_contact+" where "+customer_contact_email_id+" <> '') B ON B."+customer_contact_cust_id+" = A."+customer_master_cust_id+");"

    # FIX 8 Change id to cu_id To Get Compatible With Amit's Code
    # query = query + 'ALTER TABLE personal_table RENAME COLUMN id TO cu_id;'

    # FIX 9 Change country_code To country To Get Compatible With Amit's Code
    # query = query + 'ALTER TABLE personal_table RENAME COLUMN country_code TO country;'

    # FIX 10 Change email to email_id To Get Compatible With Amit's Code
    # query = query + 'ALTER TABLE personal_table RENAME COLUMN email TO email_id;'

    # FIX 11 Change user_id to name Because No Name Is Found( Remove Later Because Name Is Mandatory)
    # query = query + 'ALTER TABLE personal_table RENAME COLUMN user_id TO name;'


    return query

def create_r_tables(customer_master, customer_master_cust_id):
    print 'r-table'
    table_obj = connect_to_this_database()
    table_names = ['churn_engagement', 'cltv_value', 'high_conv', 'profile_clusters']
    for table in table_names:
        try:
            table_obj.cur.execute("SELECT EXISTS(SELECT * FROM " + str(table) + ");")
        except Exception as e:
            print e
            table_obj.conn.rollback()
            if e.message.__contains__("relation"):
                query = None
                if str(table) == 'churn_engagement':
                    query = str('CREATE TABLE IF NOT EXISTS churn_engagement ( cust TEXT DEFAULT NULL, churn DOUBLE PRECISION DEFAULT NULL, engagement TEXT DEFAULT NULL percent_churn DOUBLE PRECISION DEFAULT NULL, );')
                    query = query + str('INSERT INTO churn_engagement ( SELECT ' + customer_master_cust_id + ' FROM ' + customer_master + ' as cust);')
                elif str(table) == 'cltv_value':
                    query = str('CREATE TABLE IF NOT EXISTS cltv_value ( cust TEXT DEFAULT NULL, cltv DOUBLE PRECISION DEFAULT NULL, value TEXT DEFAULT NULL percent_cltv DOUBLE PRECISION DEFAULT NULL, );')
                    query = query + str('INSERT INTO cltv_value ( SELECT ' + customer_master_cust_id + ' FROM ' + customer_master + ' as cust);')
                elif str(table) == 'high_conv':
                    query = str('CREATE TABLE IF NOT EXISTS high_conv ( cust TEXT DEFAULT NULL, high_conv TEXT DEFAULT NULL );')
                    query = query + str('INSERT INTO high_conv ( SELECT ' + customer_master_cust_id + ' FROM ' + customer_master + ' as cust);')
                elif str(table) == 'profile_clusters':
                    query = str('CREATE TABLE IF NOT EXISTS profile_clusters ( cust_id TEXT DEFAULT NULL, cluster INTEGER DEFAULT NULL );')
                    query = query + str('INSERT INTO profile_clusters ( SELECT ' + customer_master_cust_id + ' FROM ' + customer_master + ' as cust_id);')
                if query is not None:
                    table_obj.cur.execute(query)
                    table_obj.conn.commit()

# def create_personal_table():
#     query = 'DROP TABLE IF EXISTS personal_table;'
#     query = query + 'CREATE TABLE IF NOT EXISTS personal_table (cust_id TEXT DEFAULT NULL, gender TEXT DEFAULT NULL, age INTEGER DEFAULT NULL, country TEXT DEFAULT NULL, firstname TEXT DEFAULT NULL, lastname TEXT DEFAULT NULL, email_id TEXT DEFAULT NULL );'
#     query = query + 'INSERT INTO personal_table ( SELECT ' + customer_master_cust_id + ' FROM ' + customer_master + ' AS cust_id );'
#
#     if customer_contact_phone_number != None and customer_contact_email_id != None:
#         # contact - name, phone, email TO personal
#         query = query + 'UPDATE personal_table SET '
#         query = query + 'phone_number = A.' + customer_contact_phone_number + ','
#         if customer_contact_firstname == None and customer_contact_lastname == None:
#             query = query + 'email_id = A.' + customer_contact_email_id
#         elif customer_contact_firstname != None and customer_contact_lastname == None:
#             query = query + 'email_id = A.' + customer_contact_email_id + ','
#             query = query + 'firstname = A.' + customer_contact_firstname
#         elif customer_contact_lastname != None and customer_contact_firstname == None:
#             query = query + 'email_id = A.' + customer_contact_email_id + ','
#             query = query + 'lastname = A.' + customer_contact_lastname
#         else:
#             query = query + 'email_id = A.' + customer_contact_email_id + ','
#             query = query + 'firstname = A.' + customer_contact_firstname + ','
#             query = query + 'lastname = A.' + customer_contact_lastname
#         query = query + ' FROM ' + customer_contact
#         query = query + ' A WHERE personal_table.cust_id = '
#         query = query + customer_contact + '.' + customer_contact.customer_contact_cust_id + ';'
#
#     return query

def create_personal_table(customer_master_obj, customer_contact_obj):
    query = 'DROP TABLE IF EXISTS personal_table;'
    query = query + 'CREATE TABLE IF NOT EXISTS personal_table AS ( SELECT * FROM '+ customer_master_obj['customer_master'] +' );'
    query = query + 'ALTER TABLE personal_table ALTER COLUMN ' + customer_master_obj['cust_id'] + ' TYPE TEXT USING ' + customer_master_obj['cust_id'] + '::TEXT ;'

    if customer_contact_obj['customer_contact'] != None:
        # ALTER TABLE personal_table ADD COLUMN email_id TEXT;
        # UPDATE personal_table SET email_id = contact.email FROM contact WHERE id = contact.user_id;
        query = query + 'ALTER TABLE personal_table ADD COLUMN email_id TEXT DEFAULT NULL;'
        if customer_contact_obj['email_id'] != None:
            query = query + 'UPDATE personal_table SET email_id = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['email_id'] + ' FROM '
            query = query + customer_contact_obj['customer_contact'] + ' WHERE ' + customer_master_obj['cust_id'] + ' = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['cust_id'] + ';'

        # ALTER TABLE personal_table ADD COLUMN phone_number INTEGER;
        # UPDATE personal_table SET phone_number = contact.phone_number FROM contact WHERE id = contact.user_id;
        query = query + 'ALTER TABLE personal_table ADD COLUMN phone_number TEXT DEFAULT NULL;'
        if customer_contact_obj['phone_number'] != None:
            query = query + 'UPDATE personal_table SET phone_number = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['phone_number'] + ' FROM '
            query = query + customer_contact_obj['customer_contact'] + ' WHERE ' + customer_master_obj['cust_id'] + ' = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['cust_id'] + ';'

        query = query + 'ALTER TABLE personal_table ADD COLUMN firstname TEXT DEFAULT NULL;'
        if customer_contact_obj['firstname'] != None:
            # ALTER TABLE personal_table ADD COLUMN firstname TEXT;
            # UPDATE personal_table SET firstname = contact.firstname FROM contact WHERE id = contact.user_id;
            query = query + 'UPDATE personal_table SET firstname = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['firstname'] + ' FROM '
            query = query + customer_contact_obj['customer_contact'] + ' WHERE ' + customer_master_obj['cust_id'] + ' = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['cust_id'] + ';'

        query = query + 'ALTER TABLE personal_table ADD COLUMN lastname TEXT DEFAULT NULL;'
        if customer_contact_obj['lastname'] != None:
            # ALTER TABLE personal_table ADD COLUMN lastname TEXT;
            # UPDATE personal_table SET lastname = contact.lastname FROM contact WHERE id = contact.user_id;
            query = query + 'UPDATE personal_table SET lastname = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['lastname'] + ' FROM '
            query = query + customer_contact_obj['customer_contact'] + ' WHERE ' + customer_master_obj['cust_id'] + ' = '
            query = query + customer_contact_obj['customer_contact'] + '.' + customer_contact_obj['cust_id'] + ';'

    query = query + 'ALTER TABLE personal_table RENAME COLUMN ' + customer_master_obj['cust_id'] + ' TO cu_id;'
    return query



