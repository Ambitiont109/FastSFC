# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]
