'''
@file:      tweetclass/code/get_tweets.py
@desc:      This file contains all the necessary functions to download and procces the tweets
            from Twitter. To connect, the tweepy library is used.
@date:      2015
@author:    Javier Selva Castello
'''

import tweepy
import json
import pickle
import re
import time
from copy import deepcopy
from ..models import Summary_tweet

# These are the OAuth keys the application needs to connect to Twitter
CONSUMER_KEY = "TNEMlsyO36DXIAjfMabHJhTyq"
CONSUMER_SECRET = "Jnw7eyaqMjP0RXaFRqwxRiIKySQ2HBlMDy5flsCcpcP9qzVaCS"
ACCES_KEY = "3293977216-ueXKhR68gsS4XkBSBxpIIXh6WxQ5ETSoTrrc2UF"
ACCES_SECRET = "ZB7EFTD2Ti6OY01FpyfYV8DvKuVt9YbI0e0sviZs1HsTs"

'''
@name:      get_tweet_api
@desc:      This method sets the authentification process and returns an api object 
            with the OAuth configured.
@params:    none needed, the keys are global variables
@return:    api object on which make all the Twitter connections needed
'''
def get_tweet_api():
    #In this first call we need consumer keys
    #Firstly the key and secondly the secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #In this second call we need access tokens
    auth.set_access_token(ACCES_KEY, ACCES_SECRET)
    return tweepy.API(auth)

'''
@name:      transform_links_regex
@desc:      This function transforms all the entities within a tweet to make them "html" links.
                - The mentions will link to the mentioned user's profile
                - The hashtags will linkt the hashtag's page
                - The urls will link wherever they are suppoused to link
@params:    tweets  - a list of tweets (Summary_tweet objects) which entities are to be transformed
                      The tweets should at least contain the key "text"
@return:    nothing, the list of tweets is modified through the reference passed by param
'''
def transform_links_regex(tweets):
    # Prepare and compile the regular expressions
    rex_url = re.compile('\s*https?://[\w.-/]+\s*')
    rex_men = re.compile('(?:\s+|^)@[\w_]+\s*')
    rex_has = re.compile('\s*#[\w-]+\s*')
    
    # Process every tweet
    for tweet in tweets:
        t_text = tweet.tweet_text # Copy the text to an auxiliar variable
        # Transform the urls into links
        for url in set(rex_url.findall(t_text)):
            url = url.replace(" ","")
            t_text=t_text.replace(url,"<a href=\""+url+"\" target=\"_blank\"><font color=blue>"+url+"</font></a>")
        # Transform the mentions into links
        for mention in sorted(set(rex_men.findall(t_text)),key=len,reverse=False):
            mention = mention.replace(" ","")
            t_text=t_text.replace(mention,"<a href=\"http://twitter.com/"+mention[1:]+"\" target=\"_blank\"><font color=blue>"+mention+"</font></a>")
        # Transform the hashtags into links
        for hashtag in sorted(set(rex_has.findall(t_text)),key=len,reverse=False):
            hashtag = hashtag.replace(" ","")
            t_text=t_text.replace(hashtag,"<a href=\"http://twitter.com/hashtag/"+hashtag[1:]+"\" target=\"_blank\"><font color=blue>"+hashtag+"</font></a>")
        tweet.tweet_text=t_text # Modify the original text with the one modified
 
# This function does the same than the one above ("transform_links_regex")
# It is not used anymore given that some tweets have links that are not included
# in the entities, so the one above does a better job by looking for all of them
# with regular expressions 
#~ def transform_links_entities(tweets):
    #~ t_text=tweet.text.replace('\n',' ').replace('\r',' ')
    #~ print(t_text)
    #~ for tweet in tweets:
        #~ t_text = tweet["text"]
        #~ for url in tweet["entities"]["urls"]:
            #~ t_text=t_text.replace(url['url'],"<a href=\""+url['url']+"\" target=\"_blank\"><font color=blue>"+url['url']+"</font></a>")
        #~ for mention in tweet["entities"]["user_mentions"]:
            #~ t_text=t_text.replace("@"+mention['screen_name'],"<a href=\"http://twitter.com/"+mention['screen_name']+"\" target=\"_blank\"><font color=blue>@"+mention['screen_name']+"</font></a>")
        #~ for hashtag in tweet["entities"]["hashtags"]:
            #~ t_text=t_text.replace("#"+hashtag['text'],"<a href=\"http://twitter.com/hashtag/"+hashtag['text']+"\" target=\"_blank\"><font color=blue>#"+hashtag['text']+"</font></a>")
        #~ tweet["text"]=t_text

'''
@name:      extract_tweet_info
@desc:      Given a tweet as an object it returns a dictionary with the tweet content extracted
@params:    tweet   - tweet object as it comes when doing a request to Twitter
@return:    dictionary containing all the tweet necessary info
'''    
def extract_tweet_info(tweet):
    return {"id":str(tweet.id),
            "date":str(tweet.created_at),
            "text":tweet.text.replace('\n',' ').replace('\r',' '),
            "retweet_count":tweet.retweet_count,
            "favorite_count":tweet.favorite_count,
            "followers":tweet.user.followers_count,
            "friends":tweet.user.friends_count,
            "user":tweet.user.screen_name,
            "rt_corpus":1,}

'''
@name:      clear_retweets
@desc:      Given a Cursor, the function iterates extracting every tweet info and returns a list of tweets.
            It also removes any tweet that is a retweet of other tweet and places the original one in the 
            list instead.
@params:    raw_tweets  - Cursor containing the tweets of a given query
@return:    list of tweets (dictionaries) containing all the tweet processed data necessary for the app
'''
def clear_retweets(raw_tweets):
    # ret_ids will containg all the tweet ids that have already been treated
    ret_ids=set([])
    # modeled_tweets will contain all the tweets that will be returned in the 
    # format of a dictionary
    modeled_tweets=[]
    # This variable will contain the position in modeled_tweets where the
    # tweet with a concrete id is.
    where_is_it = {}
    cont = 0
    for tweet in raw_tweets:
        try:#It was a retweet
            aux_id = tweet.retweeted_status.id # tweet.retweeted_status is the original tweet if this one is a RT
            if aux_id not in ret_ids:
                # If it was a retweet and it hasn't been added yet, 
                # process and add the original tweet to the results list
                modeled_tweets.append(extract_tweet_info(tweet.retweeted_status))
                ret_ids.add(aux_id)
                where_is_it[aux_id] = cont
            else:
                # If it has been added, count the amount of times it appeared as a retweet
                modeled_tweets[where_is_it[aux_id]]["rt_corpus"]+=1
        except:#It wasn't a retweet
            aux_id = tweet.id
            if aux_id not in ret_ids:
                # If it wasn't a retweet and it hasn't been added yet, 
                # process and add the tweet to the results list
                modeled_tweets.append(extract_tweet_info(tweet))
                ret_ids.add(aux_id)
                where_is_it[aux_id] = cont
            #~ else:    # the "else" is not necessary because if a "no retweet" is already in the list
                        # it's not necessary to count it 
                #~ # If it has been added, count the amount of times it appeared
                #~ modeled_tweets[where_is_it[aux_id]]["rt_corpus"]+=1
        cont += 1
                
    return modeled_tweets

'''
@name:      get_tweets
@desc:      Given a query, it searches twitter for that query and returns a list of tweets (dictionaries) containing
            all the tweet info
@params:    query       - string containing the query to be made
            types       - string indicating the type of tweets to look for
                          Expected inputs:
                            - "mixed": popular and real time tweets
                            - "popular": only popular tweets
                            - "recent": only the most recent results
            MAX_TWEETS  - integer containing the amount of tweets to look for
@return:    list of tweets (dictionaries) with each field being one relevant feature of the tweet such as "text", "id" or "retweet_count"
'''
def get_tweets(query,types="mixed",MAX_TWEETS = 1000): 
    # Get the api object with the OAuth setted
    api = get_tweet_api()
    
    # Request the tweets of the given query to Twitter
    # The cursor allows to get mor than 100 tweets with only 1 instruction
    result = tweepy.Cursor(api.search, q=query, count=100, lang="es", result_type=types).items(MAX_TWEETS)
    
    #~ tweets =[ tw for tw in result]# if not tw.text.startswith("RT")]
    aux = clear_retweets(result)
    print(len(aux))
    return aux
