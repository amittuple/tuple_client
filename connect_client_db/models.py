from django.db import models


class ClientDbModel(models.Model):
    database_name = models.CharField(max_length=50, null = True, blank=True)
    database_type = models.CharField(max_length=200, null = True, blank=True)
    host = models.CharField(max_length=200, null = True, blank=True)
    usern = models.CharField(max_length=16, null = True, blank=True)
    passw = models.CharField(max_length=50, null = True, blank=True)
    port = models.IntegerField(null = True, blank=True)

    def __unicode__(self):
        return str('%s' % self.database_name)
