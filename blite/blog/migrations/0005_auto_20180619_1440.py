# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-19 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180619_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]