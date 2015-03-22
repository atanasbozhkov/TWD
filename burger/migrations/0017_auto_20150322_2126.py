# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0016_restaurant_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='picture',
            field=models.ImageField(upload_to=b'restaurant_images', blank=True),
            preserve_default=True,
        ),
    ]
