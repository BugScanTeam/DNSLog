# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0005_auto_20151231_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dnslog',
            name='remote_addr',
        ),
        migrations.AddField(
            model_name='dnslog',
            name='type',
            field=models.TextField(default='A', verbose_name=b'dns type'),
            preserve_default=False,
        ),
    ]
