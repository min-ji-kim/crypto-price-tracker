# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-02 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_total_price_krw'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='coin_name',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title',
            new_name='quantity',
        ),
    ]
