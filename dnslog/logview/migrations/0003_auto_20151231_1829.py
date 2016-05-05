# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0002_auto_20151231_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dnslog',
            name='http_host',
            field=models.TextField(verbose_name=b'http_host'),
        ),
    ]
