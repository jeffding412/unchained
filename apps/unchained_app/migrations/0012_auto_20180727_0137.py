# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 01:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0011_offer_seller'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reply',
            new_name='Message',
        ),
    ]