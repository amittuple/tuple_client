from django.contrib import admin
from .models import MasterTable, PersonalTable
from .model_extras import chat_store
admin.site.register(PersonalTable)
admin.site.register(chat_store)
admin.site.register(MasterTable)

# Register your models here.
