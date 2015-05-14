# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('designer_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name=b'aboutImgCropping',
            field=image_cropping.fields.ImageRatioField(b'aboutImg', '155x155', allow_fullsize=False, free_crop=False, adapt_rotation=False, box_max_width=200, size_warning=False, help_text=None, box_max_height='', verbose_name='aboutImgCropping', hide_image_field=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name=b'bannerCropping',
            field=image_cropping.fields.ImageRatioField(b'banner', '1779x364', allow_fullsize=False, free_crop=False, adapt_rotation=False, box_max_width=200, size_warning=False, help_text=None, box_max_height='', verbose_name='bannerCropping', hide_image_field=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name=b'mobileBannerCropping',
            field=image_cropping.fields.ImageRatioField(b'mobileBanner', '968x642', allow_fullsize=False, free_crop=False, adapt_rotation=False, box_max_width=200, size_warning=False, help_text=None, box_max_height='', verbose_name='mobileBannerCropping', hide_image_field=False),
            preserve_default=True,
        ),
    ]
