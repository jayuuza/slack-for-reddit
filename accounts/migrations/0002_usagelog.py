# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-11 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_url', models.CharField(max_length=200)),
                ('slash_command', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Team')),
            ],
        ),
    ]
