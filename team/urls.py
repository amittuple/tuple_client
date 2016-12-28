from django.conf.urls import url
from .views import to_mailchimp
import views


urlpatterns = [
       url(r'^$', views.ins,name='amit'),
       url(r'^mailchimp/',views.to_mailchimp,name='to_mailchimp'),

       # url(r'^reply/(?P<req>([a-z]+-([a-z]+|[=])-[0-9]+(-([a-z]+|[=])-[0-9]+)?(-[a-z]+)?(-([a-z]+|[=])-[0-9]+(-([a-z]+|[=])-[0-9]+))?)+)', views.visit,name='amit'),
       url(r'^reply/(?P<req>([/]?([a-z]*[-]?[a-z]*[-]?)*[-]?[0-9a-zA-Z]*[-]?[a-zA-Z\_]*[-]?([a-z]*)(-\w+)*[-]?([OR]|[or])*[-]*([a-z]+-\w+)?[-]?)+)', views.visit,name='amit'),
       # url(r'^reply/(?P<req>([/]?[a-z]*[-]?[a-z]*[-]?[0-9a-zA-Z]*[-]?[a-zA-Z\_]*[-]?([a-z]*)(-\w+)*[-]?([OR]|[or])*[-]*([a-z]+-\w+)?[-]?)+)', views.visit,name='amit'),
]