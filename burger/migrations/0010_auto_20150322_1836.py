# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0009_delete_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='location',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lat',
            field=models.CharField(default=b'', help_text=b'Latitude', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lon',
            field=models.CharField(default=b'', help_text=b'Longitude', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='desc',
            field=models.CharField(help_text=b'Description', max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(help_text=b'Place Name', max_length=128),
            preserve_default=True,
        ),
    ]
