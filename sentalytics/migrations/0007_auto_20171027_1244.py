# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentalytics', '0006_auto_20171027_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='polarity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='sentalytics.Polarity'),
        ),
    ]
