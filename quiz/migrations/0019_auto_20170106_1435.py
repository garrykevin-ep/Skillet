# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20170106_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]