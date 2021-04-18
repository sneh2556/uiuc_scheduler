# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-26 19:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uiuc_scheduler', '0009_friendships'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendships',
            old_name='id',
            new_name='friendship_id',
        ),
        migrations.AlterField(
            model_name='friendships',
            name='friend_one_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_one_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendships',
            name='friend_two_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_two_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
