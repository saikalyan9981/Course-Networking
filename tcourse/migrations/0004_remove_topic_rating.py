# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 13:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcourse', '0003_slot_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='rating',
        ),
    ]
