from .models import Query, Query_data, Summary_tweet, Test_tweet
import time
import threading
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
import pymongo
from .code import mongo_frontend as mf

'''
 This is used to connect to the database through a lock in order to 
 avoid  different threads to access at the same time.
''' 

# The acces to the database to obtain the query that was made
def obtain_query(query_text_search):
    try:
        #if it does exist we obtain the query id
        requested_query = Query.objects.get(query_text=query_text_search)
    except Query.DoesNotExist:
        #else create it and obtain the id 
        requested_query = Query(query_text=query_text_search)
    
    requested_query.save()
    
    return requested_query

# The results of the classification have to be stored
def store_polarity(requested_query,clas_tweets,raw_tweets):
    # hm will contain the total amount of tweets retreived for a concrete query
    retweet_count = [tweet["retweet_count"]+1 for tweet in raw_tweets]
    polarity={}
    for a,b in zip(clas_tweets,retweet_count):
        polarity[a]=polarity.get(a,0)+b
    hm = float(sum(retweet_count)) 
    print("storing results")
    requested_query_data=requested_query.query_data_set.create(
        query_date=timezone.now(),
        p_pos_p=round(polarity["P+"]*100.0/hm,2),
        p_pos=round(polarity["P"]*100.0/hm,2),
        p_neu=round(polarity["NEU"]*100.0/hm,2),
        p_neg=round(polarity["N"]*100.0/hm,2),
        p_neg_p=round(polarity["N+"]*100.0/hm,2),
        p_none=round(polarity["NONE"]*100.0/hm,2),
        hm_tweets=len(clas_tweets),
    )
    print("results stored")
    
    requested_query.save()
    
    return requested_query_data

# The tweets have to be stored in the database
def store_tweets(requested_query,raw_tweets,clas_tweets):
    time.sleep(2)
    cont=0
    print("about to save in the db")
    start = time.time()
    for tweet in raw_tweets:
        tweet["polarity"]=clas_tweets[cont]
        cont+=1
    mf.save_to_mongo(raw_tweets,"tweet",requested_query.query_text)
    end = time.time()
    print("%d tweets succesfully saved" % (cont) )

def get_last_query_data(q_text):
    query = Query.objects.get(query_text=q_text)
    all_results = query.query_data_set.all()
    ids=[result.id for result in all_results]
    return max(ids)

def retrieve_query(requested_query_data_id):
    current_query = Query_data.objects.get(pk=requested_query_data_id)
    query = get_object_or_404(Query,pk=current_query.query_id_id)
    all_results = query.query_data_set.all()
    sum_tweets = Summary_tweet.objects.filter(query_id=current_query.id )
    return current_query,query,all_results,sum_tweets.filter(tag="ALL"),sum_tweets.filter(tag="POS"),sum_tweets.filter(tag="NEG")

def store_summary(requested_query, tweets, tweet_tag):
    for tweet in tweets:
        #~ if not (requested_query.summary_tweet_set.filter(pk=tweet["id"]).exists()):
        requested_query.summary_tweet_set.create(
            tweet_id=tweet["id"],
            tweet_text=tweet["text"],
            tag = tweet_tag,
            tweet_pol=tweet["polarity"],
            tweet_user=tweet["user"]
            )
    requested_query.save()

def retrieve_query_list():
    return Query.objects.all()
        
def store_feedback(tweets,polarity):
    cont=0
    for tweet in tweets:
        Test_tweet(tweet_text=tweet.tweet_text,tweet_pol=polarity[cont]).save()
        cont+=1
