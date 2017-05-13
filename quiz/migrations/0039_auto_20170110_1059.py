# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0038_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='User',
        ),
        migrations.RemoveField(
            model_name='status',
            name='question_ptr',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]