# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team_amit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('team_id', models.CharField(max_length=20)),
                ('bot_user_id', models.CharField(max_length=20)),
                ('bot_access_token', models.CharField(max_length=100)),
            ],
        ),
    ]
