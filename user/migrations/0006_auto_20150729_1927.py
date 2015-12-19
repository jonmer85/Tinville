# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userpaymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinvilleuser',
            name='customer_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
