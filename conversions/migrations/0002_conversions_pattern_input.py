# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversions',
            name='pattern_input',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
