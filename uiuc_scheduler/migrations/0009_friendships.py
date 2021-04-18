# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-28 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiuc_scheduler', '0008_auto_20200430_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='friendships',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('friend_one_id', models.IntegerField()),
                ('friend_two_id', models.IntegerField()),
            ],
            options={
                'db_table': 'friendships',
            },
        ),
    ]
