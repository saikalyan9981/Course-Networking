# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 10:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcourse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='events',
            options={'ordering': ['deadline_time']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['rating_likes']},
        ),
    ]
