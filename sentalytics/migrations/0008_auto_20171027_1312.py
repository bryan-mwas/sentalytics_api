# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 10:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentalytics', '0007_auto_20171027_1244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ('created_at',)},
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='date',
            new_name='created_at',
        ),
    ]
