# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-01 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_fillstatus_preresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='multistatus',
            name='preResult',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='fillstatus',
            name='preResult',
            field=models.IntegerField(default=-1),
        ),
    ]
