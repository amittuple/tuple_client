# To Made Dynamic
# Must Catch All Columns Thrown At It
# Mandatory 4 COlumns Rest Should be accepted if given
# See Text File For More Info
from django.db import models


class CustomerMasterMappingModel(models.Model):
    
    client_table_name = models.CharField(max_length=50, null = True, blank=True)
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    create_date = models.CharField(max_length=50, null = True, blank=True)
    birthday = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Master Mapping Table'

class CustomerMasterMappingMetaModel(models.Model):
    mapping = models.ForeignKey(CustomerMasterMappingModel)

    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Master Mapping Meta Table'


class TransactionMasterMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Transaction Master Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    product_id = models.CharField(max_length=50, null = True, blank=True)
    timestamp = models.CharField(max_length=50, null = True, blank=True)
    revenue = models.CharField(max_length=50, null = True, blank=True)
    quantity = models.CharField(max_length=50, null = True, blank=True)
    renewal = models.CharField(max_length=50, null = True, blank=True)

class TransactionMasterMappingMetaModel(models.Model):
    mapping = models.ForeignKey(TransactionMasterMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Transaction Master Mapping Meta Table'


class ProductMasterMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Product Master Mapping Table'
    product_id = models.CharField(max_length=50, null = True, blank=True)
    product_name = models.CharField(max_length=50, null = True, blank=True)
    subcategory_id = models.CharField(max_length=50, null = True, blank=True)
    subcategory_name = models.CharField(max_length=50, null = True, blank=True)
    category_id = models.CharField(max_length=50, null = True, blank=True)
    category_name = models.CharField(max_length=50, null = True, blank=True)

class ProductMasterMappingMetaModel(models.Model):
    mapping = models.ForeignKey(ProductMasterMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Product Master Mapping Meta Table'


class EventLogMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Log Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    product_id = models.CharField(max_length=50, null = True, blank=True)
    action_type = models.CharField(max_length=50, null = True, blank=True)
    timestamp = models.CharField(max_length=50, null = True, blank=True)

class EventLogMappingMetaModel(models.Model):
    mapping = models.ForeignKey(EventLogMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Log Mapping Meta Table'


class EventMasterMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Master Mapping Table'
    action_type = models.CharField(max_length=50, null = True, blank=True)
    action_name = models.CharField(max_length=50, null = True, blank=True)
    action_category_id = models.CharField(max_length=50, null = True, blank=True)
    action_category_name = models.CharField(max_length=50, null = True, blank=True)

class EventMasterMappingMetaModel(models.Model):
    mapping = models.ForeignKey(EventMasterMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Master Mapping Meta Table'


class CustomerContactMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Contact Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    email_id = models.CharField(max_length=50, null = True, blank=True)
    facebook_id = models.CharField(max_length=50, null = True, blank=True)
    phone_number = models.CharField(max_length=50, null = True, blank=True)


class CustomerContactMappingMetaModel(models.Model):
    mapping = models.ForeignKey(CustomerContactMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Contact Mapping Meta Table'

class CustomerSecondaryMappingModel(models.Model):
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Secondary Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)


class CustomerSecondaryMappingMetaModel(models.Model):
    mapping = models.ForeignKey(CustomerSecondaryMappingModel)
    column_name = models.CharField(max_length=50, null = True, blank=True)
    is_factor = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Secondary Mapping Meta Table'
