# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_productimage_cropping'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributeoption',
            name='parent',
            field=models.ForeignKey(related_name='child_colors', verbose_name=b'Parent attribute', blank=True, to='catalogue.AttributeOption', null=True),
            preserve_default=True,
        ),
    ]
