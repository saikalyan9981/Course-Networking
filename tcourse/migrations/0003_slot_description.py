# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcourse', '0002_auto_20171026_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='description',
            field=models.CharField(default='', max_length=30),
        ),
    ]
