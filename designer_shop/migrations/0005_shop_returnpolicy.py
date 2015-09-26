# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('designer_shop', '0004_auto_20150707_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='returnPolicy',
            field=django_bleach.models.BleachField(null=True, verbose_name=b'Return policy', blank=True),
            preserve_default=True,
        ),
    ]
