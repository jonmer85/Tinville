# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_promotoer_payout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinvilleuser',
            name='promoter_balance',
            field=models.DecimalField(default=Decimal('0'), max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
