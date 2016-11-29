from mapper.models import *

class TableMapper:
    def __init__(self):
        self.our_tables = [
            'TRANSACTION_MASTER',
            'CUSTOMER_SECONDARY'
            'PRODUCT_MASTER',
            'EVENT_MASTER',
            'CUSTOMER_CONTACT',
            'EVENT_LOG',
            'CUSTOMER_MASTER',
        ]
        self.our_models = {
            'CUSTOMER_CONTACT': CustomerContactMappingModel,
            'CUSTOMER_MASTER': CustomerMasterMappingModel,
            'EVENT_LOG': EventLogMappingModel,
            'EVENT_MASTER': EventMasterMappingModel,
            'PRODUCT_MASTER': ProductMasterMappingModel,
            'TRANSACTION_MASTER': TransactionMasterMappingModel,
            'CUSTOMER_SECONDARY': CustomerSecondaryMappingModel,
        }
        self.our_meta_models = {
            'CUSTOMER_CONTACT': CustomerContactMappingMetaModel,
            'CUSTOMER_MASTER': CustomerMasterMappingMetaModel,
            'EVENT_LOG': EventLogMappingMetaModel,
            'EVENT_MASTER': EventMasterMappingMetaModel,
            'PRODUCT_MASTER': ProductMasterMappingMetaModel,
            'TRANSACTION_MASTER': TransactionMasterMappingMetaModel,
            'CUSTOMER_SECONDARY': CustomerSecondaryMappingMetaModel
        }
        self.our_mandatory_tables = {
            'CUSTOMER_CONTACT': False,
            'CUSTOMER_MASTER': False,
            'EVENT_LOG': False,
            'EVENT_MASTER': False,
            'PRODUCT_MASTER': False,
            'TRANSACTION_MASTER': True,
            'CUSTOMER_SECONDARY': False,
        }

    def tables(self):
        return self.our_tables

    def models(self):
        return self.our_models

    def meta_models(self):
        return self.our_meta_models

    def mandatory_tables(self):
        return self.our_mandatory_tables

    def is_table_mandatory(self, table_name):
        try:
            return self.our_mandatory_tables[table_name]
        except Exception as e:
            print e
            print 'No Such '+ table_name + ' Table Found In Dictionary'
            return None
