from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.build_mailchimp, name='build_mailchimp')
]