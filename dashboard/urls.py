from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    # url(r'^slackbot/', views.index, name='index'),
    ]