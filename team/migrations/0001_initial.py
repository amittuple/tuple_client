# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-02 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='master_table',
            fields=[
                ('cust_id', models.IntegerField(primary_key=True, serialize=False)),
                ('churn', models.FloatField(blank=True, max_length=200, null=True)),
                ('engagement', models.TextField(blank=True, max_length=200, null=True)),
                ('cltv', models.FloatField(blank=True, max_length=200, null=True)),
                ('value', models.TextField(blank=True, max_length=200, null=True)),
                ('high_convertor', models.TextField(blank=True, max_length=200, null=True)),
                ('cluster', models.IntegerField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'team_master_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('cu_id', models.IntegerField(primary_key=True, serialize=False)),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.IntegerField(blank=True, max_length=200, null=True)),
                ('country', models.TextField(blank=True, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, max_length=200, null=True)),
                ('email_id', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'team_personal',
                'managed': False,
            },
        ),
    ]
