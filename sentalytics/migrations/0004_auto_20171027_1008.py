# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentalytics', '0003_auto_20171027_1006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='geo',
            new_name='location',
        ),
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.TextField(),
        ),
    ]