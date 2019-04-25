# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151121_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='layout',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
