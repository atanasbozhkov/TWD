# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0010_auto_20150322_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='BurgerCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Burgers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('worst', models.BooleanField(default=False)),
                ('best', models.BooleanField(default=False)),
                ('category', models.OneToOneField(to='burger.BurgerCategories')),
                ('location', models.OneToOneField(to='burger.PointOfInterest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
