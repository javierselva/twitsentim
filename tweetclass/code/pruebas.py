import time
import tweepy
import json
import pickle
import re
from copy import deepcopy

CONSUMER_KEY = "TNEMlsyO36DXIAjfMabHJhTyq"
CONSUMER_SECRET = "Jnw7eyaqMjP0RXaFRqwxRiIKySQ2HBlMDy5flsCcpcP9qzVaCS"
ACCES_KEY = "3293977216-ueXKhR68gsS4XkBSBxpIIXh6WxQ5ETSoTrrc2UF"
ACCES_SECRET = "ZB7EFTD2Ti6OY01FpyfYV8DvKuVt9YbI0e0sviZs1HsTs"

def get_tweet_api():
    #In this first call we need consumer keys
    #Firstly the key and secondly the secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #In this second call we need access tokens
    auth.set_access_token(ACCES_KEY, ACCES_SECRET)
    return tweepy.API(auth)

def clear_retweets_2(raw_tweets,max_t):
    #~ ret_ids=set([])
    modeled_tweets=[]#{}]*max_t
    #~ cont=0
    
    for tweet in raw_tweets:
        #~ try:#It was a retweet
            #~ aux_id = tweet.retweeted_status.id
            #~ if aux_id not in ret_ids:
                #~ modeled_tweets.append(extract_tweet_info(tweet.retweeted_status))
                #~ ret_ids.add(aux_id)
                #~ cont+=1
        #~ except:#It wasn't a retweet
            #~ aux_id = tweet.id
    #~ if aux_id not in ret_ids:
        modeled_tweets.append(extract_tweet_info(tweet))
    #~ ret_ids.add(aux_id)
                #~ cont+=1
            
    
    #~ print(cont)
    
    return modeled_tweets#[:cont]

#Returns a list of 100 tweets of the given query (id,date,text)
def get_tweets(query,types="mixed",MAX_TWEETS = 1000): 
    s=time.time()
    api = get_tweet_api()
    
    #~ result=[]
    result = api.search(q=query,count=500)
    #~ continue_id = ret[-1].id-1
    #~ cont=MAX_TWEETS/100
    #~ 
    #~ 
    #~ 
    #~ while cont>0:
        #~ result = result + ret
        #~ ret = api.search(q=query,count=100,max_id=continue_id)
        #~ continue_id = ret[-1].id-1
        #~ print("cont: ",cont," continue_id: ",continue_id)
        #~ cont-=1
    
    #The cursor allows to get mor than 100 tweets with only 1 instruction
    #~ result = tweepy.Cursor(api.search, q=query, count=100, lang="es", result_type=types).items(MAX_TWEETS)
    #~ e=time.time()
    #~ print("\t it took ",e-s," to download them")
    #~ result2=deepcopy(result)
    #~ s=time.time()
    
    print("it took ",time.time()-s)
    # if not tw.text.startswith("RT")]
    tweets =[ tw.id for tw in result]
    
    print(len(tweets))
    #~ aux = clear_retweets(tweets)
    #~ aux2 = clear_retweets_2(result,MAX_TWEETS)
    #~ print("\tLONGITUDES??", len(aux)," ",len(aux2))
    #~ print("\tSON IGUALES?? ",sorted(aux,key=lambda k: k['text']) == sorted(aux2,key=lambda k: k['text']))
    #~ e=time.time()
    #~ print("\t it took ",e-s," to process them")
    return tweets

get_tweets("rajoy")



