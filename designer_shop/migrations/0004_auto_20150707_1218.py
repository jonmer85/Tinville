# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('designer_shop', '0003_featuredshop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='color',
            field=models.CharField(default=b'#5B595A', max_length=7, validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Invalid hex code')]),
            preserve_default=True,
        ),
    ]
