from django.shortcuts import get_object_or_404,render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Query, Query_data, Summary_tweet, Test_tweet

from .code import get_tweets,get_polarity,tweet_summary
from . import graph_data_generator, database_connector

import _thread

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
   
    # Get the tweets from tweeter
    print("about to get tweets")
    raw_tweets = get_tweets.get_tweets(query_text_search)
    print("already got them")
    
    # Get the class for every tweet
    print("about to clasify the tweets")
    clas_tweets = get_polarity.get_polarity([tw["text"] for tw in raw_tweets])
    print("already clasified them")
    
    # Get the summary tweets
    print("about to summarize tweets")
    sum_tweets = tweet_summary.summarize(raw_tweets,clas_tweets)
    print("already summarized them")
    
    # Store the polarity information in Query_data
    requested_query_data=database_connector.store_polarity(requested_query,clas_tweets)
    
    # Store the summary tweets in Summary_tweets
    database_connector.store_summary(requested_query_data,sum_tweets)
    
    # Store all the retrieved tweets
    _thread.start_new_thread( database_connector.store_tweets, (requested_query,raw_tweets,clas_tweets), )
    #~ add_data_to_database.store_data(raw_tweets,clas_tweets,requested_query)
    
    # Return the information about the query just made to the show_results page
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(requested_query_data.id,)))
    
# This is called every time a query has been processed
# It will show the results to the user
def show_results(request,requested_query_data_id):
    # Get the current Query_data object, the actual Query, and every Query_data related to that query
    current_query,query,all_results,sum_tweets=database_connector.retrieve_query(requested_query_data_id)
    
    # Prepare all the historic graphics
    print("drawing graph")
    graph_data_generator.generate_data(query.query_text,all_results)
    print("graph is ready")
    
    # Return the info to the website
    return render(request, 'tweetclass/show_results.html',{
        'query':query,
        'all_res':all_results,
        'current':current_query,
        'sum_twe':sum_tweets,
        'generic_image_path':"tweetclass/histogram_generic_"+query.query_text+".png",
        'summary_image_path':"tweetclass/histogram_summary_"+query.query_text+".png" })

def add_test(request):
    print(request.POST)
    tweets = Summary_tweet.objects.filter(query_id=request.POST["summary_tweet_id"])
    database_connector.store_feedback(tweets,[request.POST['choice'+str(cont)] for cont in range(1,len(tweets)+1)])
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(request.POST["summary_tweet_id"],)))
