# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='story',
            field=models.ForeignKey(default='', to='dashboard.Story', related_name='comments'),
        ),
    ]
