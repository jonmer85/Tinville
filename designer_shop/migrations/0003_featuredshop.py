# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer_shop', '0002_auto_20150203_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.ForeignKey(to='designer_shop.Shop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
