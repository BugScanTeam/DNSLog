# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DNSLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('http_host', models.URLField(verbose_name=b'http_host')),
                ('remote_addr', models.GenericIPAddressField(verbose_name=b'remote_addr')),
                ('log_time', models.DateTimeField(verbose_name=b'time loged')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='WebLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('http_host', models.URLField(verbose_name=b'http_host')),
                ('remote_addr', models.GenericIPAddressField(verbose_name=b'remote_addr')),
                ('http_user_agent', models.CharField(max_length=256, verbose_name=b'user_agent')),
                ('log_time', models.DateTimeField(verbose_name=b'time loged')),
                ('user', models.ForeignKey(to='logview.User')),
            ],
            options={
                'ordering': ['log_time'],
            },
        ),
        migrations.AddField(
            model_name='dnslog',
            name='user',
            field=models.ForeignKey(to='logview.User'),
        ),
    ]
