from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from database_management.ConnectDatabase import connect_to_client_database, connect_to_this_database
from .filters import get_item
from .models import *

from connect_client_db.views import client_has_db_config


# api functions


# Append List Generated By 'extract_column_name_list_of_table' to client
def attach_column_list_to_every_client_table(cursor, table_map):
    client_table_and_column_with_type = {}
    for key in table_map:
        if not table_map[key] == '':
            temporary_table = []
            temporary_table.append(table_map[key])
            column_name_list = extract_column_name_list_of_table(cursor, temporary_table)
            client_table_and_column_with_type[str(temporary_table[0])] = {}
            for item in column_name_list:
                client_table_and_column_with_type[str(temporary_table[0])][str(item[0])] = {
                    'type': str(item[1])
                }
    return client_table_and_column_with_type

# Extract Table Names From Client Database
def extract_table_name(cursor):
    list_of_tables = []
    cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='public'")
    list_of_tables_temp = cursor.fetchall()
    for temp in list_of_tables_temp:
        for item in temp:
            list_of_tables.append(item)
    return list_of_tables

# Extract Column Name List Of A Particular Table Of Client
def extract_column_name_list_of_table(cur, tablename):
    # tablename should be a tuple or list of element one
    if isinstance(tablename, basestring):
        raise Exception('tablename variable must be a tuple or list of single element')
    cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s', tablename)
    column_name_list = cur.fetchall()
    return column_name_list

# Returns Client Db Model Names And Their Corresponding Models

def get_our_table_name():
    return [
        'TRANSACTION_MASTER',
        'CUSTOMER_MASTER',
        'CUSTOMER_SECONDARY',
        'CUSTOMER_CONTACT',
        'EVENT_LOG',
        'EVENT_MASTER',
        'PRODUCT_MASTER'
    ]

def get_table_name_model_pair():
    table_name_model_pair = {
        'TRANSACTION_MASTER': TransactionMasterMappingModel,
        'CUSTOMER_MASTER': CustomerMasterMappingModel,
        'CUSTOMER_SECONDARY': CustomerSecondaryMappingModel,
        'CUSTOMER_CONTACT': CustomerContactMappingModel,
        'EVENT_LOG': EventLogMappingModel,
        'EVENT_MASTER': EventMasterMappingModel,
        'PRODUCT_MASTER': ProductMasterMappingModel,
    }
    return table_name_model_pair

# Returns Client Db Model Names And Their Corresponding Meta Models
def get_table_name_model_meta_pair():
    return {
        'TRANSACTION_MASTER': TransactionMasterMappingMetaModel,
        'CUSTOMER_MASTER': CustomerMasterMappingMetaModel,
        'CUSTOMER_SECONDARY': CustomerSecondaryMappingMetaModel,
        'CUSTOMER_CONTACT': CustomerContactMappingMetaModel,
        'EVENT_LOG': EventLogMappingMetaModel,
        'EVENT_MASTER': EventMasterMappingMetaModel,
        'PRODUCT_MASTER': ProductMasterMappingMetaModel,
    }

# Returns Dict Of System Table Name With Whether They Are Mandatory
def is_table_name_mandatory():
    return {
        'TRANSACTION_MASTER': True,
        'CUSTOMER_MASTER': False,
        'CUSTOMER_SECONDARY': False,
        'CUSTOMER_CONTACT': False,
        'EVENT_LOG': False,
        'EVENT_MASTER': False,
        'PRODUCT_MASTER': False,
    }

# Returns Dict Of System Table Name With Which Column Names Are Mandatory
def is_column_name_mandatory(table_map):
    our_model = prepare_our_model(table_map)
    to_return = {}
    for our_table_name in our_model:
        to_return[our_table_name] = {}
        for our_column_name in our_model[our_table_name]:
            to_return[our_table_name][our_column_name] = False

    if to_return.has_key('TRANSACTION_MASTER'):
        to_return['TRANSACTION_MASTER']['cust_id'] = True
        to_return['TRANSACTION_MASTER']['product_id'] = True
        to_return['TRANSACTION_MASTER']['timestamp'] = True
        to_return['TRANSACTION_MASTER']['revenue'] = True

    if to_return.has_key('CUSTOMER_MASTER'):
        to_return['CUSTOMER_MASTER']['cust_id'] = True

    if to_return.has_key('EVENT_LOG'):
        to_return['EVENT_LOG']['cust_id'] = True
        to_return['EVENT_LOG']['product_id'] = True
        to_return['EVENT_LOG']['timestamp'] = True

    if to_return.has_key('CUSTOMER_CONTACT'):
        to_return['CUSTOMER_CONTACT']['cust_id'] = True
        to_return['CUSTOMER_CONTACT']['email_id'] = True
        to_return['CUSTOMER_CONTACT']['phone_number'] = True

    if to_return.has_key('CUSTOMER_SECONDARY'):
        to_return['CUSTOMER_SECONDARY']['cust_id'] = True


    return to_return

# Append Column List To Respective Client table And Create Map
def prepare_our_model(table_map):
    our_model = {}

    table_name_model_pair = get_table_name_model_pair()

    for our_table_name, table_model in table_name_model_pair.iteritems():
        if not table_map[our_table_name] == '':
            temporary_value = table_model._meta.get_fields()
            mapping_name = our_table_name
            our_model[mapping_name] = []
            for item in temporary_value:
                # To Exclude Id, Client, Client Table Name From Client HTML Page
                if not str(item.name).__contains__('metamodel') and item.name !='client_table_name' and item.name != 'id':
                    our_model[mapping_name].append(item.name)
    return our_model




# Input Includes
# table_map = Mapping Of Our Table wrt To Client Table
# client_table_and_column_with_type = Mapping Of Client Table and Column List Along With There Data Types
# our_model = Mapping of Our Table and Our Columns
# request = Post Request That Contains The Client Specific Inputs
# ------------------------- NOTE: ----------------------- #
# request will be deprecated in next fix
def prepare_final_model(table_map, client_table_and_column_with_type, our_model, request):
    column_map = {}
    for our_table_name, our_column_list in our_model.iteritems():
        temp = {}
        column_map[our_table_name] = {}
        for our_column_name in our_column_list:
            temp[our_column_name] = {}
            if request.POST[our_table_name+'.'+our_column_name] == u'':
                temp[our_column_name] = None
            else:
                temp[our_column_name][request.POST[our_table_name+'.'+our_column_name]] = {}
                # if request.POST.has_key(our_table_name+'.'+our_column_name+'.is_factor'):
                #     if request.POST[our_table_name+'.'+our_column_name+'.is_factor'] == 'on':
                #         is_factor = True
                #     else:
                #         is_factor = False
                # else:
                #     is_factor = False
                temp[our_column_name][request.POST[our_table_name+'.'+our_column_name]] = {
                    'type': client_table_and_column_with_type[table_map[our_table_name]][request.POST[our_table_name+'.'+our_column_name]]['type'],
                    # 'is_factor': is_factor
                }
        column_map[our_table_name][table_map[our_table_name]] = {}
        column_map[our_table_name][table_map[our_table_name]] = temp
        # factor list
        column_map[our_table_name]['is_factor'] = {}
        if client_table_and_column_with_type.has_key(table_map[our_table_name]):
            for client_column_name in client_table_and_column_with_type[table_map[our_table_name]].keys():
                if request.POST.has_key(table_map[our_table_name]+'.'+'is_factor'+'.'+client_column_name):
                    if request.POST[table_map[our_table_name]+'.'+'is_factor'+'.'+client_column_name] == 'on':
                        column_map[our_table_name]['is_factor'][client_column_name] = True
    return column_map


# Column Mapping View
def column_mapping(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    obj = connect_to_client_database(user)
    try:
        table_map = request.session['table_map']
        for item in table_map:
            if is_table_name_mandatory()[item]:
                if table_map[item] == '' or table_map[item] == None:
                    print 'Please Fill Mandatory Fields First'
                    return HttpResponseRedirect(reverse('table_mapping'))
    except Exception as e:
        print e
        print 'No Table Map Found'
        return HttpResponseRedirect(reverse('table_mapping'))
    try:
        client_table_and_column_with_type = attach_column_list_to_every_client_table(obj.cur, table_map)
        print client_table_and_column_with_type
        request.session['client_table_structure'] = client_table_and_column_with_type
    #   Now For Our Database
        our_model = prepare_our_model(table_map)
    except KeyError as e:
        if e.message.__contains__('table_map'):
            print 'Table Mapping Should Be Done First'
            return HttpResponseRedirect(reverse('table_mapping'))
    except Exception as e:
        print e
    mandatory_columns = is_column_name_mandatory(table_map)
    if request.method == 'POST':
        for our_table_name in mandatory_columns:
            for our_column_name in mandatory_columns[our_table_name]:
                if mandatory_columns[our_table_name][our_column_name]:
                    if request.POST[our_table_name+'.'+our_column_name] == None or request.POST[our_table_name+'.'+our_column_name] == '':
                        print 'Not All Mandatory Columns Are Submitted'
                        return HttpResponseRedirect(reverse('column_mapping'))
        column_map = prepare_final_model(table_map, client_table_and_column_with_type, our_model, request)
        request.session['column_map'] = column_map
        return HttpResponseRedirect(reverse('mapping_review'))

    return render(request, 'mapper/column-mapping.html', {
        'client_table_and_column_with_type': client_table_and_column_with_type,
        'our_model': our_model,
        'table_map': table_map,
        'get_item': get_item,
        'is_column_name_mandatory': mandatory_columns,
    })


# Table Mapping View
def table_mapping(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    obj = connect_to_client_database(user)
    if not obj.isConnected():
        return HttpResponse('Client Database Connection Configuration Missing.')
    list_of_our_tables = get_our_table_name()
    # for item in get_table_name_model_pair():
    #     list_of_our_tables.append(item)
    list_of_tables = extract_table_name(obj.cur)
    obj.cur.close()
    obj.conn.close()
    if len(list_of_tables) == 0 or list_of_tables is None:
        return HttpResponse('No Tables Found In Database')
    # request.session['list_of_tables'] = list_of_tables

    # CODE TO SESSION TABLES LIST UNLESS AND UNTIL THE USER LOGIN AGAIN

    # try:
    #     list_of_tables = request.session['list_of_tables']
    # except KeyError as e:
    #     if e.message.__contains__('list_of_tables'):
    #         obj = connect_to_client_database(user)
    #         if not obj.isConnected():
    #             raise Exception('Client Database Connection Configuration Missing.')
    #         list_of_tables = extract_table_name(obj.cur)
    #         obj.cur.close()
    #         obj.conn.close()
    #         request.session['list_of_tables'] = list_of_tables
    # except Exception as e:
    #     print e

    if request.method == 'POST':
        table_map = {}
        for item in list_of_our_tables:
            if is_table_name_mandatory()[item]:
                if request.POST[item] == None or request.POST[item] == '':
                    print 'Mandatory Fields Are Not Filled'
                    return HttpResponseRedirect(reverse('table_mapping'))
            table_map[str(item)] = str(request.POST[item])
        request.session['table_map'] = table_map
        return HttpResponseRedirect(reverse('column_mapping'))

    return render(request, 'mapper/table-mapping.html', {
        'list_of_tables': list_of_tables,
        'list_of_headings': list_of_our_tables,
        'is_table_name_mandatory': is_table_name_mandatory(),
        'get_item': get_item
    })

# Save Mapping Into Model
# Parameters Include
# table_name_model_pair = Includes Client Db Model And Its Mapping
# column_map = Final Mapping Dictionary Of User Custom Mapping
# user = SimpleLazyObject of request.user
def save_mapping_into_model(table_name_model_pair, column_map):
    table_name_model_meta_pair=get_table_name_model_meta_pair()
    for our_table_name, client_table_list in column_map.iteritems():
        if client_table_list.has_key:
            if client_table_list.keys()[0] == 'is_factor':
                client_table_name = client_table_list.keys()[1]
            else:
                client_table_name = client_table_list.keys()[0]
            mapping_model_obj = table_name_model_pair[our_table_name]()
            for our_column_name, client_column_list in column_map[our_table_name][client_table_name].iteritems():
                # print our_column_name
                if client_column_list is not None:
                    # print client_column_list.keys()[0]
                    setattr(mapping_model_obj, our_column_name, client_column_list.keys()[0])
            # Not To Be Inputted By Client
            # setattr(obj, 'client', user)
            setattr(mapping_model_obj, 'client_table_name', client_table_name)
            try:
                if table_name_model_pair[our_table_name].objects.all().exists():
                    print our_table_name + ' Mapping Already Exists'
                    print 'Skip'
                else:
                    mapping_model_obj.save()
                    save_mapping_meta_into_model(our_table_name, table_name_model_meta_pair, column_map, mapping_model_obj)
            except Exception as e:
                print e
                # if e.message.__contains__('matching query'):
                #     obj.save()
                #     save_mapping_meta_into_model(table_name_model_meta_pair, column_map, obj.id)

# Store Model Mapping Meta In Database
def save_mapping_meta_into_model(our_table_name, table_name_model_meta_pair, column_map, mapping_obj):
    try:
        if table_name_model_meta_pair[our_table_name].objects.filter(mapping = mapping_obj).exists():
            print 'mapping meta already exists for this mapping'
            return None
    except Exception as e:
        print e
    for client_column_name, is_factor in column_map[our_table_name]['is_factor'].iteritems():
        obj = table_name_model_meta_pair[our_table_name]()
        setattr(obj,'mapping', mapping_obj)
        setattr(obj,'column_name', client_column_name)
        setattr(obj, 'is_factor', is_factor)
        obj.save()
        # for our_column_name, client_column_list in column_map[our_table_name][client_table_list.keys()[0]].iteritems():
        #     if client_column_list is not None:
        #         obj = table_name_model_meta_pair[our_table_name]()
        #         setattr(obj,'mapping', mapping_obj)
        #         setattr(obj,'column_name', client_column_list.keys()[0])
        #         setattr(obj, 'is_factor', client_column_list[client_column_list.keys()[0]]['is_factor'])
        #         obj.save()

# Mapping Review View
def mapping_review(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    try:
        column_map = request.session['column_map']
    except KeyError:
        print 'No Mapping Defined Please Do Mapping Before'
        return HttpResponseRedirect(reverse('column_mapping'))
    user = request.user
    if mapping_exists() is None:
        return HttpResponse('Bad Mapping Config')
    if request.method == 'POST':
        response = True
        if mapping_exists():
            response = clear_client_database(user)
        if not response:
            return HttpResponse('Not Able To Clear Database')
        mapping_clear = clear_mapping_model()
        if not mapping_clear:
            print 'Not Able To Clear Mapping Model. Please Contact Admin'
            return
        table_name_model_pair = get_table_name_model_pair()
        # table_name_model_meta_pair = get_table_name_model_meta_pair()
        save_mapping_into_model(table_name_model_pair, column_map)
        request.session['transfer_database_flag'] = True
        return HttpResponseRedirect(reverse('transfer_database'))
    return render(request, 'mapper/mapping-review.html', {
        'column_map': column_map,
        'get_item': get_item,
        'mapping_exists': mapping_exists()
    })

def mapping_exists():
    try:
        for our_table_name, our_table_model in get_table_name_model_pair().iteritems():
            table_obj = our_table_model.objects.all()
            if len(table_obj) != 0:
                return True
        return False
    except Exception as e:
        print e
        return None

def clear_mapping_session(request):
    try:
        del request.session['table_map']
        del request.session['column_map']
    except Exception as e:
        print e

def clear_mapping_model():
    try:
        for our_table_name, our_table_model in get_table_name_model_pair().iteritems():
            table_obj = our_table_model.objects.all()
            if len(table_obj) != 0:
                table_obj.delete()
        for our_table_name, our_table_meta_model in get_table_name_model_meta_pair().iteritems():
            table_obj = our_table_meta_model.objects.all()
            if len(table_obj) != 0:
                table_obj.delete()
        return True
    except Exception as e:
        print e
        return False

def clear_client_database(user):
    try:
        for our_table_name, our_table_model in get_table_name_model_pair().iteritems():
            table_obj = our_table_model.objects.all()
            if len(table_obj) != 0:
                client_table_name = table_obj[0].client_table_name
                table = connect_to_this_database()
                table.cur.execute('DROP TABLE IF EXISTS '+ client_table_name)
                table.conn.commit()
        return True
    except Exception as e:
        print e
        return False