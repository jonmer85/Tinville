# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_product_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'original', '400x400', allow_fullsize=False, free_crop=False, adapt_rotation=False, box_max_width=200, size_warning=False, help_text=None, box_max_height='', verbose_name='cropping', hide_image_field=False),
            preserve_default=True,
        ),
    ]
