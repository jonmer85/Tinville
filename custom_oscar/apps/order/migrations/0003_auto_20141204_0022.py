# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20141007_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentevent',
            name='group',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shippingevent',
            name='group',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shippingevent',
            name='reference',
            field=models.CharField(default=b'', max_length=128, verbose_name=b'Reference', blank=True),
            preserve_default=True,
        ),
    ]
