# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_dashboard_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='code',
            field=models.TextField(null=True),
        ),
    ]
