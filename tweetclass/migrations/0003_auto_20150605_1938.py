# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetclass', '0002_remove_tweet_tweet_id_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query_data',
            name='p_neg',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='query_data',
            name='p_neg_p',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='query_data',
            name='p_neu',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='query_data',
            name='p_none',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='query_data',
            name='p_pos',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='query_data',
            name='p_pos_p',
            field=models.FloatField(default=0),
        ),
    ]
