# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151103_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='alt_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
