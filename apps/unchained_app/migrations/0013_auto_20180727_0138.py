# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 01:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0012_auto_20180727_0137'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Reply',
        ),
    ]
