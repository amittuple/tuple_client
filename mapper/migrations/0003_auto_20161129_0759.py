# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0002_customersecondarymappingmetamodel_customersecondarymappingmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersecondarymappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.CustomerSecondaryMappingModel'),
        ),
    ]
