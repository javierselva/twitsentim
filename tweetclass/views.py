from django.shortcuts import get_object_or_404,render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Query, Query_data, Summary_tweet, Test_tweet

from .code import get_tweets,get_polarity,tweet_summary
from . import graph_data_generator, database_connector

import _thread
import time

'''
This file is used to generate almost everything on the site.
It defines what should be given to the user everytime he hits something
or makes a query. Is the skeleton of the app.
'''

# The first view we define: Index
# Is the front page of the site and it just consists on a form to make the query.
def index(request):
    return render(request, 'tweetclass/index.html')

# This is called everytime the user makes a query
def query_page(request):
    # Get the query from the request
    query_text_search = request.POST['query_text']
    print(request.POST)
    # If the query is empty, redirect the user.
    if query_text_search=="":
        return render(request,'tweetclass/index.html',{'error_message':"You didn't write a query."})
   
    # Try to get the object asociated with the query
    # If it doesn't exist it will be created
    requested_query = database_connector.obtain_query(query_text_search)
    s_t = time.time()
    # Get the tweets from tweeter
    print("about to get tweets")
    s = time.time()
    raw_tweets = get_tweets.get_tweets(query_text_search)
    e = time.time()
    print("already got them; took ",e-s)
    
    # Get the class for every tweet
    print("about to clasify the tweets")
    s = time.time()
    clas_tweets = get_polarity.get_polarity([tw["text"] for tw in raw_tweets])
    raw_tweets = tweet_summary.add_field("polarity",raw_tweets,clas_tweets)
    e = time.time()
    print("already clasified them; took ",e-s)
    
    # Get the summary tweets
    print("about to summarize tweets")
    s = time.time()
    sum_tweets = tweet_summary.summarize(raw_tweets,MAX_RES_TWEETS = int(len(raw_tweets)*0.01))
    sum_positive = tweet_summary.summarize([tweet for tweet in raw_tweets if tweet["polarity"]=="P+" or tweet["polarity"]=="P"],MAX_RES_TWEETS = 5)
    sum_negative = tweet_summary.summarize([tweet for tweet in raw_tweets if tweet["polarity"]=="N+" or tweet["polarity"]=="N"],MAX_RES_TWEETS = 5)
    e = time.time()
    print("already summarized them; took ",e-s)
    
    # Store the polarity information in Query_data
    print("-------------")
    s = time.time()
    requested_query_data=database_connector.store_polarity(requested_query,clas_tweets)
    
    # Store the summary tweets in Summary_tweets
    database_connector.store_summary(requested_query_data,sum_tweets,"ALL")
    database_connector.store_summary(requested_query_data,sum_positive,"POS")
    database_connector.store_summary(requested_query_data,sum_negative,"NEG")
    
    # Store all the retrieved tweets
    _thread.start_new_thread( database_connector.store_tweets, (requested_query,raw_tweets,clas_tweets), )
    e = time.time()
    #~ add_data_to_database.store_data(raw_tweets,clas_tweets,requested_query)
    print("it took ",e-s,"to store everything in the db")
    # Return the information about the query just made to the show_results page
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(requested_query_data.id,)))
    
# This is called every time a query has been processed
# It will show the results to the user
def show_results(request,requested_query_data_id):
    # Get the current Query_data object, the actual Query, and every Query_data related to that query
    current_query,query,all_results,sum_t_all,sum_t_pos,sum_t_neg=database_connector.retrieve_query(requested_query_data_id)
    
    # Prepare all the historic graphics
    print("drawing graph")
    graph_data_generator.generate_data(query.query_text,all_results)
    print("graph is ready")
    
    mul=3
    bars_size={}
    bars_size[0]=int(current_query.p_pos_p*mul)
    bars_size[1]=int(current_query.p_pos*mul)
    bars_size[2]=int(current_query.p_neu*mul)
    bars_size[3]=int(current_query.p_neg*mul)
    bars_size[4]=int(current_query.p_neg_p*mul)
    bars_size[5]=int(current_query.p_none*mul)
    
    sum_pol=[tweet.tweet_pol for tweet in sum_t_all]
    count_pol = [sum_pol.count("P+"),sum_pol.count("P"),sum_pol.count("NEU"),sum_pol.count("N"),sum_pol.count("N+"),sum_pol.count("NONE"),len(sum_pol)]
    
    val_max = max([
                    (current_query.p_pos_p,"VERY POSITIVE","#A7DB40"),
                    (current_query.p_pos,"POSITIVE","#D8E067"),
                    (current_query.p_neu,"NEUTRAL","#FFB81F"),
                    (current_query.p_neg,"NEGATIVE","#FF743D"),
                    (current_query.p_neg_p,"VERY NEGATIVE","#C4213D"),
                    (current_query.p_none,"NONE","#707070")])
    #~ print(bars_size)
    # Return the info to the website
    return render(request, 'tweetclass/show_results.html',{
        'query':query,
        'all_res':all_results,
        'current':current_query,
        'sizes':bars_size,
        'sum_t_all':sum_t_all,
        'sum_t_pos':sum_t_pos,
        'sum_t_neg':sum_t_neg,
        'sum_count':count_pol,
        'pol_win':val_max,
        'generic_image_path':"tweetclass/histogram_generic_"+query.query_text+".png",
        'summary_image_path':"tweetclass/histogram_summary_"+query.query_text+".png" })

def add_test(request):
    #~ print(request.POST)
    tweets = Summary_tweet.objects.filter(query_id=request.POST["summary_tweet_id"])
    all_tweets = tweets.filter(tag="ALL")
    pos_tweets = tweets.filter(tag="POS")
    neg_tweets = tweets.filter(tag="NEG")
    database_connector.store_feedback(all_tweets,[request.POST['choice'+str(cont)] for cont in range(1,len(all_tweets)+1)])
    database_connector.store_feedback(pos_tweets,[request.POST['choice2'+str(cont)] for cont in range(1,len(pos_tweets)+1)])
    database_connector.store_feedback(neg_tweets,[request.POST['choice3'+str(cont)] for cont in range(1,len(neg_tweets)+1)])
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(request.POST["summary_tweet_id"],)))
