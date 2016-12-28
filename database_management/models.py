# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class MasterView(models.Model):
    cust_id = models.IntegerField(blank=True, null=True)
    churn = models.FloatField(blank=True, null=True)
    engagement = models.TextField(blank=True, null=True)
    cltv = models.FloatField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    high_convertor = models.TextField(blank=True, null=True)
    cluster = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_view'
