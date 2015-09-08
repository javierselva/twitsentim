'''
@file:      tweetclass/views.py
@desc:      This file is used to generate almost everything on the site.
            It defines what should be given to the user everytime he does an 
            action that requires processing. Is the skeleton of the app.
@author:    Javier Selva Castello
@date:      2015
'''

from django.shortcuts import get_object_or_404,render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Query, Query_data, Summary_tweet, Test_tweet

from .code import get_tweets,get_polarity,tweet_summary,generate_graph
from . import graph_data_generator, database_connector

import _thread
import time

# This view will be called everytime the user tries to acces the "Home" section of the app
# Is the front page of the site and it just consists on a form to make the query, and a list 
# of the 10 most popular querys
def index(request):
    # Get the list of querys
    querys = database_connector.retrieve_query_list()
    return render(request, 'tweetclass/index.html',{'querys':querys[:min(10,len(querys))],"error":False})
 
# This view will be called when accesing the "What's this" section of the app
# It just returns the "what's this" page
def whats_this(request):
    return render(request, 'tweetclass/whats_this.html')

# This view is the one that processes a query. It's called everytime a user makes a query
def query_page(request):
    s_t = time.time()
    # Get the query from the request
    query_text_search = request.POST['query_text']
    # If the query is empty, redirect the user.
    if query_text_search=="":
        querys = database_connector.retrieve_query_list()
        return render(request,'tweetclass/index.html',{'error':True,'querys':querys[:min(10,len(querys))]})
   
    # Try to get the object asociated with the query
    # If it doesn't exist it will be created
    requested_query = database_connector.obtain_query(query_text_search)
    
    # Get the tweets from Twitter
    print("___ #1 ABOUT TO GET TWEETS ___")
    s = time.time()
    raw_tweets = get_tweets.get_tweets(query_text_search)
    e = time.time()
    print("#1 already got them; took ",e-s)
    
    # Get the class for every tweet
    print("___ #2 ABOUT TO CLASIFY TWEETS ___")
    s = time.time()
    clas_tweets = get_polarity.get_polarity([tw["text"] for tw in raw_tweets])
    # Adds the polarity as a field in the tweet dictionaries
    tweet_summary.add_field("polarity",raw_tweets,clas_tweets)
    e = time.time()
    print("#2 already clasified them; took ",e-s)
    
    # Get the summary tweets
    print("___ #3 ABOUT TO SUMMARIZE TWEETS ___")
    s = time.time()
    # A summary of all the tweets
    sum_tweets = tweet_summary.summarize(tweets=raw_tweets,MAX_RES_TWEETS = max(int(len(raw_tweets)*0.01),6))
    # A summary of the positive tweets
    sum_positive = tweet_summary.summarize([tweet for tweet in raw_tweets if tweet["polarity"]=="P+" or tweet["polarity"]=="P"],MAX_RES_TWEETS = 5)
    # A summary of the negative tweets
    sum_negative = tweet_summary.summarize([tweet for tweet in raw_tweets if tweet["polarity"]=="N+" or tweet["polarity"]=="N"],MAX_RES_TWEETS = 5)
    e = time.time()
    print("#3 already summarized them; took ",e-s)
    
    
    print("-------------")
    s = time.time()
    # Store the polarity information in Query_data
    requested_query_data=database_connector.store_polarity(requested_query,raw_tweets,clas_tweets)
    
    # Store the summary tweets in Summary_tweets
    if len(sum_tweets)>0:
        database_connector.store_summary(requested_query_data,sum_tweets,"ALL")
    if len(sum_positive)>0:
        database_connector.store_summary(requested_query_data,sum_positive,"POS")
    if len(sum_negative)>0:
        database_connector.store_summary(requested_query_data,sum_negative,"NEG")
    
    # Store all the retrieved tweets
    _thread.start_new_thread( database_connector.store_tweets, (requested_query,raw_tweets), )
    e = time.time()
    #~ add_data_to_database.store_data(raw_tweets,clas_tweets,requested_query)
    print("it took ",e-s,"to store everything in the db")
    print("___ #5 EVERITHING TOOK: ",e-s_t)
    # Return the information about the query just made to the show_results page
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=(requested_query_data.id,)))
    
# This is called every time a query has been processed
# It will show the results to the user
def show_results(request,requested_query_data_id):
    show_feedback = True
    if requested_query_data_id.startswith("F"):
        requested_query_data_id = requested_query_data_id[1:]
        show_feedback = False
    
    # Get the current Query_data object, the actual Query, every Query_data related to that Query 
    # and every summary related to that Query_data
    current_query,query,all_results,sum_t_all,sum_t_pos,sum_t_neg=database_connector.retrieve_query(requested_query_data_id)
    
    general_sum = False
    positive_sum = False
    negative_sum = False
    
    count_pol=[]
    if len(sum_t_all)>0:
        # Transform the entities in the summary tweets to be html links
        get_tweets.transform_links_regex(sum_t_all)
        # Counts the amount of tweets for each polarity in the summary
        sum_pol=[tweet.tweet_pol for tweet in sum_t_all]
        count_pol = [sum_pol.count("P+"),sum_pol.count("P"),sum_pol.count("NEU"),sum_pol.count("N"),sum_pol.count("N+"),sum_pol.count("NONE"),len(sum_pol)]
        # Prepare the radial graphic for the summary
        print("drawing graph")
        generate_graph.radial_summary(count_pol[:-1],query.query_text)
        print("graph is ready")
        general_sum = True
        
    if len(sum_t_pos)>0:
        # Transform the entities in the summary tweets to be html links
        get_tweets.transform_links_regex(sum_t_pos)
        positive_sum = True
    
    if len(sum_t_neg)>0:
        # Transform the entities in the summary tweets to be html links
        get_tweets.transform_links_regex(sum_t_neg)
        negative_sum = True
    
    # Prepare the size of the bars that will show the polarity results
    mul=3
    bars_size={}
    bars_size[0]=int(current_query.p_pos_p*mul)
    bars_size[1]=int(current_query.p_pos*mul)
    bars_size[2]=int(current_query.p_neu*mul)
    bars_size[3]=int(current_query.p_neg*mul)
    bars_size[4]=int(current_query.p_neg_p*mul)
    bars_size[5]=int(current_query.p_none*mul)
    
    
    # Gets the polarity with a greater value, its name and the color it'll have on the results page
    val_max = max([
                    (current_query.p_pos_p,"VERY POSITIVE","#A7DB40"),
                    (current_query.p_pos,"POSITIVE","#D8E067"),
                    (current_query.p_neu,"NEUTRAL","#FFB81F"),
                    (current_query.p_neg,"NEGATIVE","#FF743D"),
                    (current_query.p_neg_p,"VERY NEGATIVE","#C4213D"),
                    (current_query.p_none,"NONE","#707070")])
                    
    # Return the info to the website
    return render(request, 'tweetclass/show_results.html',{
        'query':query,
        'current':current_query,
        'sizes':bars_size,
        'sum_t_all':sum_t_all,
        'hm_summary':len(sum_t_all),
        'summary_exist':[general_sum,positive_sum,negative_sum],
        'sum_t_pos':sum_t_pos,
        'sum_t_neg':sum_t_neg,
        'sum_count':count_pol,
        'pol_win':val_max,
        'show_feedback':show_feedback,
        'summary_image_path':"tweetclass/summary_pie_"+query.query_text+".png" })

# This view is for the historic results of a query. It will show the graphics to the user
def show_historic(request,requested_query_data_id):
    feedback = False
    if requested_query_data_id.startswith("F"):
        requested_query_data_id = requested_query_data_id[1:]
        feedback = True
    # If the history view is called from the index (from the top querys list) the id will be "000"
    if requested_query_data_id=='000':
        generic = True
        # Get the actual query_data_id, i.e. the Query_data form th last time the query was made
        requested_query_data_id = database_connector.get_last_query_data(request.POST["real_id"])
    else:
        generic = False
    
    # Get the current Query_data object, the actual Query, and every Query_data related to that query
    current_query,query,all_results,_,_,_=database_connector.retrieve_query(requested_query_data_id)
    
    # Prepare all the historic graphics
    if len(all_results)>1:
        print("drawing graph")
        graph_data_generator.generate_data(query.query_text,all_results)
        print("graph is ready")
        hist_available = True
    else:
        hist_available = False
    
    # Return the info to the website
    return render(request, 'tweetclass/show_historic.html',{
        'current':current_query,
        'query':query,
        'all_res':all_results,
        'hist_available': hist_available,
        'feedback':feedback,
        'is_generic':generic, # it is used to disable the "Results" link if the query is generic
        'generic_image_path':"tweetclass/histogram_generic_"+query.query_text+".png",
        'summary_image_path':"tweetclass/histogram_summary_"+query.query_text+".png" })

# This temporary view is called every time feedback is sent.
# It just saves the feedback and goes back to show results
def add_test(request):
    # Get the tweets that are being feedbacked
    tweets = Summary_tweet.objects.filter(query_id=request.POST["summary_tweet_id"])
    # Split them in generic summary, positive summary and negative summary
    all_tweets = tweets.filter(tag="ALL")
    pos_tweets = tweets.filter(tag="POS")
    neg_tweets = tweets.filter(tag="NEG")
    # Get the real polarities and store them
    database_connector.store_feedback(all_tweets,[request.POST['choice'+str(cont)] for cont in range(1,len(all_tweets)+1)])
    database_connector.store_feedback(pos_tweets,[request.POST['choice2'+str(cont)] for cont in range(1,len(pos_tweets)+1)])
    database_connector.store_feedback(neg_tweets,[request.POST['choice3'+str(cont)] for cont in range(1,len(neg_tweets)+1)])
    return HttpResponseRedirect(reverse('tweetclass:show_results',args=("F"+str(request.POST["summary_tweet_id"]),)))
