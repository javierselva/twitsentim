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

# This class will store the tweets corresponding to a concrete query
# The id of each tweet will be the same that in tweeter
#~ class Tweet(models.Model):
    #~ query_id = models.ForeignKey(Query)
    #~ tweet_text = models.CharField(max_length=140)
    #~ tweet_pol = models.CharField(max_length=4)
    #~ 
    #~ #This is used for when the system needs to print a Query object
    #~ def __str__(self):
        #~ return self.tweet_text

