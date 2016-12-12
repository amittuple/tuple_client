from .models import Personal
from .models import master_table
import django_filters

class ProductFilter(django_filters.FilterSet):

    list1=master_table.objects.filters(cltv='*').filters(value=all).filters(engagement=all).filters(profile=all).filters(churn=all).filters(high_converter=all)
    list2=Personal.objects.filters(country=all).filters(name=all).filters(gender=all).filters(age=all)

    # def bot_pass(user_input):
    # name = django_filters.CharFilter(lookup_expr='iexact')



