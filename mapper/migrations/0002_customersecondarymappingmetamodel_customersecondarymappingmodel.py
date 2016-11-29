# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerSecondaryMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
                ('mapping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.CustomerContactMappingModel')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSecondaryMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
