# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0009_auto_20150805_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary_tweet',
            name='tweet_user',
            field=models.CharField(default='noName', max_length=15),
        ),
    ]
