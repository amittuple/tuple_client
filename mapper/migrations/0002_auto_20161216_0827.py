# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-16 08:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermastermappingmodel',
            old_name='customer_id',
            new_name='cust_id',
        ),
    ]
