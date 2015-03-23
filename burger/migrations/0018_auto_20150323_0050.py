# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0017_auto_20150322_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(default=b'', help_text=b'Place Name', max_length=128),
            preserve_default=True,
        ),
    ]
