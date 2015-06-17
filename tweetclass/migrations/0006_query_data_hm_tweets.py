# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0005_summary_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='query_data',
            name='hm_tweets',
            field=models.IntegerField(default=0),
        ),
    ]
