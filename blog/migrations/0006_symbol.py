# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-22 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180402_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(max_length=200)),
                ('symbol', models.CharField(max_length=200)),
            ],
        ),
    ]