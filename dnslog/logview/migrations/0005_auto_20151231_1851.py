# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0004_user_udomain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dnslog',
            name='log_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'time loged'),
        ),
        migrations.AlterField(
            model_name='weblog',
            name='log_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'time loged'),
        ),
    ]
