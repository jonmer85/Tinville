# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20141204_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingevent',
            name='label_url',
            field=models.URLField(null=True, verbose_name=b'Label_Url'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shippingevent',
            name='tracking_code',
            field=models.TextField(null=True, verbose_name=b'tracking_code'),
            preserve_default=True,
        ),
    ]
