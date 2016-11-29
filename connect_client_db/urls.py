from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'connect_client_db'),
    url(r'^connected', views.connected, name='connection_successfull'),
    url(r'^failed', views.failed, name='connection_failed'),
    url(r'^result$', views.result, name='result')
]
