# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0007_test_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary_tweet',
            name='tag',
            field=models.CharField(max_length=3, default='ALL'),
        ),
        migrations.AddField(
            model_name='summary_tweet',
            name='tweet_id',
            field=models.CharField(max_length=21, default='000000000000'),
        ),
    ]
