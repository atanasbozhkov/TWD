# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0013_auto_20150322_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='name',
        ),
    ]
