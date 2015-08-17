from django.db import models
from django.utils import timezone

'''
In this file the different tables of the database are defined.
In order for these to be effective, we must makemigrations and then migrate.
These commands will generate the corresponding database in SQLite
'''

# The first class, just containing the text of the query
class Query(models.Model):
    query_text = models.CharField(max_length=200)
    
    #This is used for when the system needs to print a Query object
    def __str__(self):
        return self.query_text

# This second class will contain all the data about a query made in a concrete
# moment of time. (Date and polarity after classifying the obtained tweets)
class Query_data(models.Model):
    query_id = models.ForeignKey(Query)
    query_date = models.DateTimeField()
    p_pos_p = models.FloatField(default=0)
    p_pos = models.FloatField(default=0)
    p_neu = models.FloatField(default=0)
    p_neg = models.FloatField(default=0)
    p_neg_p = models.FloatField(default=0)
    p_none = models.FloatField(default=0)
    hm_tweets = models.IntegerField(default=0)

# This class will store the tweets that summarizes a concrete query
# The id of each tweet will be the same that in tweeter
class Summary_tweet(models.Model):
    query_id = models.ForeignKey(Query_data)
    tweet_id = models.CharField(max_length=21,default="000000000000")
    tag = models.CharField(max_length=3,default="ALL")
    tweet_text = models.CharField(max_length=500)
    tweet_pol = models.CharField(max_length=4)
    tweet_user = models.CharField(max_length=15,default="noName")
    
    #This is used for when the system needs to print a Summary_tweet object
    def __str__(self):
        return self.tweet_text+"\t"+self.tweet_pol

class Test_tweet(models.Model):
    tweet_text = models.CharField(max_length=140)
    tweet_pol = models.CharField(max_length=4)
    
    #This is used for when the system needs to print a Test_tweet object
    def __str__(self):
        return self.tweet_text
