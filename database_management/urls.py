from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transfer-database/$', views.transfer_database, name='transfer_database'),
    url(r'^transfer-failed/$', views.transfer_failed, name='transfer_failed'),
    url(r'^test-script/$', views.test_script, name='test_script')
]
