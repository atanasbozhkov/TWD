# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burger', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=512)),
                ('desc', models.CharField(max_length=128)),
                ('categoryID', models.OneToOneField(to='burger.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
