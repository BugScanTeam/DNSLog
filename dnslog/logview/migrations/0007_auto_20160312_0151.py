# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0006_auto_20151231_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dnslog',
            old_name='http_host',
            new_name='host',
        ),
        migrations.RemoveField(
            model_name='weblog',
            name='http_host',
        ),
        migrations.AddField(
            model_name='weblog',
            name='path',
            field=models.TextField(default='test', verbose_name=b'path'),
            preserve_default=False,
        ),
    ]
