# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0003_auto_20150605_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='query_id',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
    ]
