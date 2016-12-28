from django.db import models
class Team_amit(models.Model):
    team_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)
class email_list_for_slack_1(models.Model):
    email_list_slack=models.CharField(max_length=9000)