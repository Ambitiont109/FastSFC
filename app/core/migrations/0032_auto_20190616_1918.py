# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20190524_0051'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='document',
            index_together=set([('company', 'cat')]),
        ),
    ]
