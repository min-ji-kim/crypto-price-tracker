# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-02 11:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180402_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_price_krw',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
