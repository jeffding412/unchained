# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unchained_app', '0013_auto_20180727_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='imageFile',
            field=models.FileField(default='', upload_to='apps/unchained_app/static/unchained_app/images2'),
            preserve_default=False,
        ),
    ]
