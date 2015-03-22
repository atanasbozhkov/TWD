# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0014_remove_restaurant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='name',
            field=models.CharField(default=b'', help_text=b'Place Name', unique=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pointofinterest',
            name='name',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
