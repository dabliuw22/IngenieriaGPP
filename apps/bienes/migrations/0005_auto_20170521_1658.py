# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-21 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes', '0004_auto_20170520_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]