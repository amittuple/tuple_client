from django.contrib import admin
from .models import master_table
from .models import Personal
admin.site.register(Personal)
admin.site.register(master_table)

# Register your models here.