# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0008_auto_20150722_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary_tweet',
            name='tweet_text',
            field=models.CharField(max_length=500),
        ),
    ]
