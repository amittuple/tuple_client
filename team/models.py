from django.db import models
from django.core.validators import MaxValueValidator
class Personal(models.Model):
    cu_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    age=models.IntegerField()
    country=models.CharField(max_length=20)
    email_id=models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class master_table(models.Model):
    cltv=models.IntegerField(null=True,blank=True)
    value=models.CharField(max_length=100,null=True,blank=True)
    engagement=models.CharField(max_length=100,null=True,blank=True)
    profile=models.CharField(max_length=100,null=True,blank=True)
    high_converter=models.PositiveIntegerField(validators=[MaxValueValidator(100),],null=True,blank=True)
    churn=models.PositiveIntegerField(validators=[MaxValueValidator(100),],null=True,blank=True)
    personal=models.ForeignKey(Personal,on_delete=models.CASCADE)





    def __unicode__(self):
        return self.personal.name
