from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^column-mapping/$', views.column_mapping, name='column_mapping'),
    url(r'^table-mapping/$', views.table_mapping, name='table_mapping'),
    url(r'^mapping-review/$', views.mapping_review, name='mapping_review'),
]
