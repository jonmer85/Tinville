# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('designer_shop', '__first__'),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(default=None, to='designer_shop.Shop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productimage',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'original', '400x500', allow_fullsize=False, free_crop=False, adapt_rotation=False, box_max_width=400, size_warning=False, help_text=None, box_max_height=500, verbose_name='cropping', hide_image_field=False),
            preserve_default=True,
        ),
    ]
