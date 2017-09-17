# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-20 15:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('locaciones', '0001_initial'),
        ('bienes', '0003_auto_20170518_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locaciones.Ciudad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orden',
            name='productos',
            field=models.ManyToManyField(blank=True, related_name='ordenes_producto', through='bienes.DetalleOrdenProducto', to='bienes.Producto'),
        ),
        migrations.AlterField(
            model_name='orden',
            name='servicios',
            field=models.ManyToManyField(blank=True, related_name='ordenes_servicio', to='bienes.Servicio'),
        ),
    ]
