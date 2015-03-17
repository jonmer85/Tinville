# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_tinvilleuser_access_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinvilleuser',
            name='access_code',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
    ]
