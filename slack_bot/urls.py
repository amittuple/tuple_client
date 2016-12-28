from django.conf.urls import url
import views
from slack_bot.startbot import createbot

createbot()
urlpatterns = [
    # url(r'^$', views.index),
    # url(r'^test/', views.test_bot, name='TEST'),
    url(r'^slack/oauth/', views.slack_oauth),
]
