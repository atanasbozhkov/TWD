# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0007_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointOfInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('position', geoposition.fields.GeopositionField(max_length=42, blank=True)),
            ],
            options={
                'verbose_name_plural': 'points of interest',
            },
            bases=(models.Model,),
        ),
    ]
