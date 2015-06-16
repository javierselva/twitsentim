from django.shortcuts import get_object_or_404,render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Query, Query_data, Tweet

from .code import get_tweets
from .code import get_polarity
from . import graph_data_generator
from . import database_connector

import _thread

'''
This file is used to generate almost everything on the site.
It defines what should be given to the user everytime he hits something
or makes a query. Is the skeleton of the app.
'''

# The first view we define: Index
# Is the fron page of the site and it just consists on a form to make the query.
def index(request):
    return render(request, 'tweetclass/index.html')

# This is called everytime the user makes a query
def query_page(request):
    # Get the query from the request
    query_text_search = request.POST['query_text']
    # If the query is empty, redirect the user.
    if query_text_search=="":
        return render(request,'tweetclass/index.html',{'error_message':"You didn't write a query."})
   
    # Try to get the object asociated with the query
    # If it doesn't exist it will be created
    requested_query = database_connector.connect_db(query_text_search=query_text_search,flag=0)
   
    # Get the tweets from tweeter
    print("about to get tweets")
    raw_tweets = get_tweets.get_tweets(query_text_search)
    print("already got them")
    
    # Get the class for every tweet
    print("about to clasify the tweets")
    clas_tweets = get_polarity.get_polarity([tweet for [idd,date,tweet] in raw_tweets])
    print("already clasified them")
    
    # Store the polarity information in Query_data
    requested_query_data=database_connector.connect_db(raw_tweets,clas_tweets,requested_query,"",1)
    
    # Store all the retrieved tweets
    _thread.start_new_thread( database_connector.connect_db, (raw_tweets,clas_tweets,requested_query,"",2), )
    #~ add_data_to_database.store_data(raw_tweets,clas_tweets,requested_query)
    
    # Return the information about the query just made to the show_results page
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(requested_query_data.id,)))
    
# This is made every time a query has been processed
# It will show the results to the user
def show_results(request,requested_query_data_id):
    # Get the current Query_data object, the actual Query, and every Query_data related to that query
    current_query,query,all_results=database_connector.connect_db(requested_query_data_id=requested_query_data_id,flag=3)
    
    # Prepare all the historic graphics
    print("drawing graph")
    graph_data_generator.generate_data(query.query_text,all_results)
    print("graph is ready")
    
    # Return the info to the website
    return render(request, 'tweetclass/show_results.html',{
        'query':query,
        'all_res':all_results,
        'current':current_query,
        'generic_image_path':"tweetclass/histogram_generic_"+query.query_text+".png",
        'summary_image_path':"tweetclass/histogram_summary_"+query.query_text+".png" })
