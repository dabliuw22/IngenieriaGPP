# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-18 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bienes', '0002_auto_20170518_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleordenproducto',
            old_name='productos',
            new_name='producto',
        ),
    ]