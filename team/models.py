from django.db import models


class Personal(models.Model):
    cu_id = models.TextField(primary_key=True)
    # gender = models.CharField(max_length=200, blank=True, null=True)
    # age = models.IntegerField(max_length=200, blank=True, null=True)
    # country = models.TextField(max_length=200, blank=True, null=True)
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
        return str(self.cu_id)
    class Meta:
        managed = False
        db_table = 'team_personal'




class master_table(models.Model):
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
        db_table = 'team_master_table'

#store chat history
class chat_store(models.Model):
    chat_message=models.CharField(max_length=999)
    chat_time=models.CharField(max_length=999)
    chat_sendby=models.CharField(max_length=100)
