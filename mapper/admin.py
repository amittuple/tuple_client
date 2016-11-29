from django.contrib import admin

from .models import *

admin.site.register(CustomerMasterMappingModel)
admin.site.register(TransactionMasterMappingModel)
admin.site.register(ProductMasterMappingModel)
admin.site.register(EventLogMappingModel)
admin.site.register(EventMasterMappingModel)
admin.site.register(CustomerContactMappingModel)


# Register your models here.
