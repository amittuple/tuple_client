from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transfer-database/$', views.transfer_database, name='transfer_database'),
]
