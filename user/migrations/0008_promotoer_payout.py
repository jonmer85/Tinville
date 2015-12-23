# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_access_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoterPayout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('reference', models.CharField(max_length=128, verbose_name=b'Reference', blank=True)),
                ('promoter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tinvilleuser',
            name='promoter_balance',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
