# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-25 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0004_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='zip',
        ),
        migrations.AddField(
            model_name='shipping',
            name='zipcode',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
