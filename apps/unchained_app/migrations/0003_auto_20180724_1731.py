# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0002_offer_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='password_hash',
        ),
    ]
