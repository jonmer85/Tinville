# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20160126_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinvilleuser',
            name='promoter_code',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
