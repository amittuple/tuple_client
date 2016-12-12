# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContactMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerContactMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_id', models.CharField(blank=True, max_length=50, null=True)),
                ('email_id', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook_id', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMasterMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMasterMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSecondaryMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
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
        migrations.CreateModel(
            name='EventLogMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventLogMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_id', models.CharField(blank=True, max_length=50, null=True)),
                ('product_id', models.CharField(blank=True, max_length=50, null=True)),
                ('action_type', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventMasterMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventMasterMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('action_type', models.CharField(blank=True, max_length=50, null=True)),
                ('action_name', models.CharField(blank=True, max_length=50, null=True)),
                ('action_category_id', models.CharField(blank=True, max_length=50, null=True)),
                ('action_category_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMasterMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMasterMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('product_id', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
                ('subcategory_id', models.CharField(blank=True, max_length=50, null=True)),
                ('subcategory_name', models.CharField(blank=True, max_length=50, null=True)),
                ('category_id', models.CharField(blank=True, max_length=50, null=True)),
                ('category_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionMasterMappingMetaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_factor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionMasterMappingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_id', models.CharField(blank=True, max_length=50, null=True)),
                ('product_id', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.CharField(blank=True, max_length=50, null=True)),
                ('revenue', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='transactionmastermappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.TransactionMasterMappingModel'),
        ),
        migrations.AddField(
            model_name='productmastermappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.ProductMasterMappingModel'),
        ),
        migrations.AddField(
            model_name='eventmastermappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.EventMasterMappingModel'),
        ),
        migrations.AddField(
            model_name='eventlogmappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.EventLogMappingModel'),
        ),
        migrations.AddField(
            model_name='customersecondarymappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.CustomerSecondaryMappingModel'),
        ),
        migrations.AddField(
            model_name='customermastermappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.CustomerMasterMappingModel'),
        ),
        migrations.AddField(
            model_name='customercontactmappingmetamodel',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapper.CustomerContactMappingModel'),
        ),
    ]