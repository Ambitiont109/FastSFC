# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_pipeline_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pipeline',
            old_name='schedule',
            new_name='actions',
        ),
    ]
