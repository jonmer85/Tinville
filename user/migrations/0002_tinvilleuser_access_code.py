# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tinvilleuser',
            name='access_code',
            field=models.CharField(default=b'ABC12', max_length=5),
            preserve_default=True,
        ),
    ]
