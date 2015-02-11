# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import designer_shop.models
from django.conf import settings
import django.core.validators
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, unique=True, max_length=100, verbose_name=b'Shop name', db_index=True)),
                ('slug', models.SlugField()),
                ('banner', models.ImageField(default=b'images/banner.jpg', max_length=255, upload_to=designer_shop.models.upload_to_banner)),
                ('mobileBanner', models.ImageField(default=b'images/mobilebanner.jpg', max_length=255, upload_to=designer_shop.models.upload_to_mobile_banner)),
                ('logo', models.ImageField(max_length=255, upload_to=designer_shop.models.upload_to_logo)),
                ('aboutImg', models.ImageField(max_length=255, upload_to=designer_shop.models.upload_to_about)),
                ('aboutContent', django_bleach.models.BleachField()),
                ('color', models.CharField(default=b'#663399', max_length=7, validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Invalid hex code')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
