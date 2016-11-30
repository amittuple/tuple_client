from django.contrib import admin

from .models import *

admin.site.register(CustomerMasterMappingModel)
admin.site.register(TransactionMasterMappingModel)
admin.site.register(ProductMasterMappingModel)
admin.site.register(EventLogMappingModel)
admin.site.register(EventMasterMappingModel)
admin.site.register(CustomerContactMappingModel)

admin.site.register(CustomerMasterMappingMetaModel)
admin.site.register(TransactionMasterMappingMetaModel)
admin.site.register(ProductMasterMappingMetaModel)
admin.site.register(EventLogMappingMetaModel)
admin.site.register(EventMasterMappingMetaModel)
admin.site.register(CustomerContactMappingMetaModel)


# Register your models here.
