# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0004_auto_20150616_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary_tweet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('tweet_text', models.CharField(max_length=140)),
                ('tweet_pol', models.CharField(max_length=4)),
                ('query_id', models.ForeignKey(to='tweetclass.Query_data')),
            ],
        ),
    ]
