# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0012_pointofinterest_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='categoryID',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lon',
        ),
    ]
