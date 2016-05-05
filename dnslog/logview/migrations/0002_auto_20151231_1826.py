# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dnslog',
            options={'ordering': ['log_time']},
        ),
        migrations.AlterField(
            model_name='weblog',
            name='http_host',
            field=models.TextField(verbose_name=b'http_host'),
        ),
        migrations.AlterField(
            model_name='weblog',
            name='http_user_agent',
            field=models.TextField(verbose_name=b'user_agent'),
        ),
    ]
