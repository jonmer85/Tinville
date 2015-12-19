# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20150729_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tinvilleuser',
            old_name='access_code',
            new_name='promoter_code',
        ),
    ]
