# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-08 20:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default=b'', max_length=200)),
                ('open_id', models.CharField(default=b'', max_length=200)),
                ('is_buyer', models.BooleanField(default=False)),
                ('head_img', models.CharField(default=b'', max_length=200)),
                ('desc', models.TextField(default=b'')),
                ('goods', models.CharField(default=b'', max_length=200)),
                ('source', models.CharField(default=b'', max_length=200)),
                ('delivery', models.CharField(default=b'', max_length=20)),
                ('service', models.CharField(default=b'', max_length=20)),
                ('wx', models.CharField(default=b'', max_length=50)),
                ('qq', models.CharField(default=b'', max_length=20)),
                ('phone', models.CharField(default=b'', max_length=20)),
                ('email', models.CharField(default=b'', max_length=50)),
                ('www', models.CharField(default=b'', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
