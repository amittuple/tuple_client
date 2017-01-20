from django.db import models


class PersonalTable(models.Model):
    cu_id = models.TextField(primary_key=True)
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return str(self.cu_id)
    class Meta:
        managed = False
        db_table = 'personal_table'




class MasterTable(models.Model):
    cust_id = models.TextField(primary_key=True)
    churn = models.FloatField(max_length=200, blank=True, null=True)
    engagement = models.TextField(max_length=200, blank=True, null=True)
    cltv = models.FloatField(max_length=200, blank=True, null=True)
    value = models.TextField(max_length=200, blank=True, null=True)
    high_convertor = models.TextField(max_length=200, blank=True, null=True)
    cluster = models.IntegerField(max_length=200, blank=True, null=True)
    percent_cltv = models.IntegerField(max_length=200, blank=True, null=True)
    percent_churn = models.IntegerField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return str(self.cust_id)

    class Meta:
        managed = False
        db_table = 'master_table'