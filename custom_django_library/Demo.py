from DatabaseConnect import connect_to_this_database
from connect_client_db.models import ClientDbModel
from mapper.models import *
from team.models import PersonalTable, MasterTable
from team.model_extras import chat_store

class Demo:
    def __init__(self):
        self.this_db = connect_to_this_database()
        self.dashboard = {
            'MasterTable': MasterTable,
            'PersonalTable': PersonalTable
        }
        self.chatbot = {
            'ChatStore': chat_store
        }
        self.table_name_model_pair = {
                'TRANSACTION_MASTER': TransactionMasterMappingModel,
                'CUSTOMER_MASTER': CustomerMasterMappingModel,
                'CUSTOMER_SECONDARY': CustomerSecondaryMappingModel,
                'CUSTOMER_CONTACT': CustomerContactMappingModel,
                'EVENT_LOG': EventLogMappingModel,
                'EVENT_MASTER': EventMasterMappingModel,
                'PRODUCT_MASTER': ProductMasterMappingModel,
            }
        self.table_name_model_meta_pair = {
                'TRANSACTION_MASTER': TransactionMasterMappingMetaModel,
                'CUSTOMER_MASTER': CustomerMasterMappingMetaModel,
                'CUSTOMER_SECONDARY': CustomerSecondaryMappingMetaModel,
                'CUSTOMER_CONTACT': CustomerContactMappingMetaModel,
                'EVENT_LOG': EventLogMappingMetaModel,
                'EVENT_MASTER': EventMasterMappingMetaModel,
                'PRODUCT_MASTER': ProductMasterMappingMetaModel,
            }

    def clean_dashboard(self):
        for model_name, model in self.dashboard.iteritems():
            model.objects.all().delete()

    def clean_chat(self):
        for chat, chat_str in self.chatbot.iteritems():
            chat_str.objects.all().delete()

    def clean_db_settings(self):
        ClientDbModel.objects.all().delete()

    def clean_client_database(self):
        try:
            for our_table_name, our_table_model in self.table_name_model_pair.iteritems():
                table_obj = our_table_model.objects.all()
                if len(table_obj) != 0:
                    client_table_name = table_obj[0].client_table_name
                    table = connect_to_this_database()
                    table.cur.execute('DROP TABLE IF EXISTS ' + client_table_name)
                    table.conn.commit()
            return True
        except Exception as e:
            print e
            return False

    # CAUTION !!!
    # Clean Client Tables In Our Database Before Cleaning Mappings
    def clean_mappings(self):
        try:
            for our_table_name, our_table_model in self.table_name_model_pair.iteritems():
                our_table_model.objects.all().delete()
            for our_table_name, our_table_meta_model in self.table_name_model_meta_pair.iteritems():
                our_table_meta_model.objects.all().delete()
            return True
        except Exception as e:
            print e
            return False

    def clean_r_tables(self):
        try:
            tables = ['churn_engagement', 'high_conv', 'cltv_value', 'predict_period', 'profile_clusters']
            for table in tables:
                self.this_db.cur.execute('DROP TABLE IF EXISTS ' + str(table))
                self.this_db.conn.commit()
            return True
        except Exception as e:
            print e
            return False

    def clean_all(self):
        self.clean_chat()
        self.clean_dashboard()
        self.clean_r_tables()
        self.clean_client_database()
        self.clean_mappings()
        self.clean_db_settings()








