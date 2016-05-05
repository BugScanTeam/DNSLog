# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0003_auto_20151231_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='udomain',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
    ]
