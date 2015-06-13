# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150302_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='tinvilleuser',
            name='customer_id',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
