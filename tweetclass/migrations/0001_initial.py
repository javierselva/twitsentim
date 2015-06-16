# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('query_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Query_data',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('query_date', models.DateTimeField()),
                ('p_pos_p', models.IntegerField(default=0)),
                ('p_pos', models.IntegerField(default=0)),
                ('p_neu', models.IntegerField(default=0)),
                ('p_neg', models.IntegerField(default=0)),
                ('p_neg_p', models.IntegerField(default=0)),
                ('p_none', models.IntegerField(default=0)),
                ('query_id', models.ForeignKey(to='tweetclass.Query')),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tweet_id_t', models.CharField(max_length=100)),
                ('tweet_text', models.CharField(max_length=140)),
                ('tweet_pol', models.CharField(max_length=4)),
                ('query_id', models.ForeignKey(to='tweetclass.Query')),
            ],
        ),
    ]
