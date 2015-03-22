# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0011_burgercategories_burgers'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointofinterest',
            name='restaurant',
            field=models.OneToOneField(default=b'', to='burger.Restaurant'),
            preserve_default=True,
        ),
    ]
