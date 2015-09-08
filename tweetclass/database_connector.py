'''
@file:      tweetclass/database_connector.py
@desc:      This file contains all the necessary functions for accessing the database.
            Everytime some function needs to retreive querys or store them, it is 
            through this file's functions.
@date:      2015
@author:    Javier Selva Castello
''' 

from .models import Query, Query_data, Summary_tweet, Test_tweet
import time
import threading
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
import pymongo
from .code import mongo_frontend as mf

'''
@name:      obtain_query
@desc:      Returns a Query object with the requested query text. If it doesn't exist, it is created
@params:    query_text_search      - a string containing the text of the query to be found
@return:    Query object with the text in "query_text_search"
'''
def obtain_query(query_text_search):
    try:
        # if it does exist we obtain the query id
        requested_query = Query.objects.get(query_text=query_text_search)
    except Query.DoesNotExist:
        # else create it and obtain the id 
        requested_query = Query(query_text=query_text_search)
    # save the changes (in case it was created)
    requested_query.save()
    
    return requested_query

'''
@name:      store_polarity
@desc:      Creates a Query_data with the polarity results for a given Query
@params:    requested_query     - the Query on which to add the Query_data object
            raw_tweets          - a list of tweets (dictionaries) the polarity of which has to be stored. 
                                  It has to contain at least the "polarity" and "retweet_count" fields
            clas_tweets         - a list of strings containing the polarity of each tweet contained in the list 
                                  "raw_tweets". If not provided, the polarities will be extracted from raw_tweets
@return:    Query_data object created with the percentage value of each polarity and its date
'''
# Even though the "clas_tweets" param could be extracted from "raw_tweets", as it has a polarity field, 
# this method is called from the "query_page" view, where the "clas_tweets" list is already created
def store_polarity(requested_query,raw_tweets,clas_tweets=[]):
    if len(clas_tweets)==0:
        clas_tweets = [tweet["polarity"] for tweeet in raw_tweets]
    # Create a list of the number of times the tweet exists
    retweet_count = [tweet["rt_corpus"] for tweet in raw_tweets]
    polarity={}
    # Each polarity is counted the amount of times the tweet is retweeted
    for a in ["P+","P","NEU","N","N+","NONE"]:
        polarity[a]=0
    for a,b in zip(clas_tweets,retweet_count):
        polarity[a]=polarity.get(a,0)+b
    # hm will contain the total amount of tweets retreived for a concrete query
    hm = float(sum(retweet_count)) 
    # Every polarity value is stored as a percentage with two decimals
    requested_query_data=requested_query.query_data_set.create(
        query_date=timezone.now(),
        p_pos_p=round(polarity["P+"]*100.0/hm,2),
        p_pos=round(polarity["P"]*100.0/hm,2),
        p_neu=round(polarity["NEU"]*100.0/hm,2),
        p_neg=round(polarity["N"]*100.0/hm,2),
        p_neg_p=round(polarity["N+"]*100.0/hm,2),
        p_none=round(polarity["NONE"]*100.0/hm,2),
        hm_tweets=len(clas_tweets), # The real amount of tweets is how many were clasified
    )
    # Save the changes (the created query_data)
    requested_query.save()
    
    return requested_query_data

'''
@name:      store_tweets
@desc:      Stores all the downloaded tweets for a given query
@params:    requested_query     - the Query on which to add the tweets in the database
            raw_tweets          - a list of tweets (dictionaries) to be stored.
@return:    nothing
'''
def store_tweets(requested_query,raw_tweets):
    # This method will be executed once the results page is displayed
    time.sleep(2)
    print("about to save in the db")
    mf.save_to_mongo(raw_tweets,"tweet",requested_query.query_text)
    print("%d tweets succesfully saved" % (len(raw_tweets)) )

'''
@name:      get_last_query_data
@desc:      Retreives the last Query_data id from a given Query
@params:    q_text  - string containing the query text
@return:    integer containing the last Query_data id
'''
def get_last_query_data(q_text):
    # Get the Query for the given query_text
    query = Query.objects.get(query_text=q_text)
    # Get all the Query_data objects for the Query
    all_results = query.query_data_set.all()
    # Get all the Query_data ids
    ids=[result.id for result in all_results]
    # As the id for a Query_data is auto incremented each time one is created, 
    # the last one will be the greatest
    return max(ids)

'''
@name:      retrieve_query
@desc:      Given a Query_data id, returns all the information available in the database for that query
@params:    requested_query_data_id - integer containing the id for which the information has to be retrieved
@return:    current_query   - the actual Query_data which id is the requested by parameter
            query           - the Query object referenced by the Query_data
            all_results     - a list of all the Query_datas for the Query "query"
            sum_tweets      - the three sumaries (generic, positive and negative) as a lists of Summary_tweets
'''
def retrieve_query(requested_query_data_id):
    current_query = Query_data.objects.get(pk=requested_query_data_id)
    query = get_object_or_404(Query,pk=current_query.query_id_id)
    all_results = query.query_data_set.all()
    sum_tweets = Summary_tweet.objects.filter(query_id=current_query.id )
    return current_query,query,all_results,sum_tweets.filter(tag="ALL"),sum_tweets.filter(tag="POS"),sum_tweets.filter(tag="NEG")

'''
@name:      store_summary
@desc:      Given a summary and its type (generic, positive or negative), it's stored on the database
@params:    requested_query - Query object related to which the summary has to be stored
            tweets          - a list of tweets (dictionaries) containing the summary tweets to be stored
            tweet_tag       - string containgin the type of summary being stored.
                              The different values expected are:
                                "ALL" - for a generic summary
                                "POS" - for a summary of the positive tweets
                                "NEG" - for a summary of the negative tweets
@return:    nothing
'''
def store_summary(requested_query, tweets, tweet_tag):
    for tweet in tweets:
        #~ if not (requested_query.summary_tweet_set.filter(pk=tweet["id"]).exists()): # thi
        requested_query.summary_tweet_set.create(
            tweet_id=tweet["id"],
            tweet_text=tweet["text"],
            tag = tweet_tag,
            tweet_pol=tweet["polarity"],
            tweet_user=tweet["user"]
            )
    if len(tweets)>0:
        requested_query.save()

'''
@name:      retrieve_query_list
@desc:      Generates a list of all the Querys ever made
@params:    none needed
@return:    a list of Query objects sorted by the amount of times it has been made
'''
def retrieve_query_list():
    querys = Query.objects.all()
    ret = []
    for query in querys:
        ret.append((query.query_data_set.count(),query.query_text))
    return sorted(ret,reverse=True)
    
'''
@name:      store_feedback
@desc:      Stores feedback tweets in the database
@params:    tweets      - a list of tweets (as Summary_tweets) to be stored
            polarity    - the feedbacked polarity as a list of strings
@return:    nothing
'''
def store_feedback(tweets,polarity):
    cont=0
    for tweet in tweets:
        Test_tweet(tweet_text=tweet.tweet_text,tweet_pol=polarity[cont]).save()
        cont+=1
