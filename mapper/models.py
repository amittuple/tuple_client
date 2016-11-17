# To Made Dynamic
# Must Catch All Columns Thrown At It
# Mandatory 4 COlumns Rest Should be accepted if given
# See Text File For More Info
from django.db import models
from django.contrib.auth.models import User


class CustomerMasterMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)
    customer_id = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Master Mapping Table'


class TransactionMasterMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Transaction Master Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    product_id = models.CharField(max_length=50, null = True, blank=True)
    timestamp = models.CharField(max_length=50, null = True, blank=True)
    revenue = models.CharField(max_length=50, null = True, blank=True)


class ProductMasterMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Product Master Mapping Table'
    product_id = models.CharField(max_length=50, null = True, blank=True)
    product_name = models.CharField(max_length=50, null = True, blank=True)
    subcategory_id = models.CharField(max_length=50, null = True, blank=True)
    subcategory_name = models.CharField(max_length=50, null = True, blank=True)
    category_id = models.CharField(max_length=50, null = True, blank=True)
    category_name = models.CharField(max_length=50, null = True, blank=True)


class EventLogMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Log Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    product_id = models.CharField(max_length=50, null = True, blank=True)
    action_type = models.CharField(max_length=50, null = True, blank=True)
    timestamp = models.CharField(max_length=50, null = True, blank=True)


class EventMasterMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Event Master Mapping Table'
    action_type = models.CharField(max_length=50, null = True, blank=True)
    action_name = models.CharField(max_length=50, null = True, blank=True)
    action_category_id = models.CharField(max_length=50, null = True, blank=True)
    action_category_name = models.CharField(max_length=50, null = True, blank=True)


class CustomerContactMappingModel(models.Model):
    client = models.OneToOneField(User)
    client_table_name = models.CharField(max_length=50, null = True, blank=True)

    def __unicode__(self):
        return 'Customer Contact Mapping Table'
    cust_id = models.CharField(max_length=50, null = True, blank=True)
    email_id = models.CharField(max_length=50, null = True, blank=True)
    facebook_id = models.CharField(max_length=50, null = True, blank=True)
    phone_number = models.CharField(max_length=50, null = True, blank=True)
