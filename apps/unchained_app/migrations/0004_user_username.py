# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0003_auto_20180724_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
