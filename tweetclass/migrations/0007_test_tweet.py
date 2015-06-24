# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0006_query_data_hm_tweets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_tweet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('tweet_text', models.CharField(max_length=140)),
                ('tweet_pol', models.CharField(max_length=4)),
            ],
        ),
    ]
