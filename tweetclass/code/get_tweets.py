import tweepy
import json
import pickle

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

def transform_links(tweet):
    t_text=tweet.text.replace('\n',' ').replace('\r',' ')
    print(t_text)
    for url in tweet.entities["urls"]:
        t_text=t_text.replace(url['url'],"<a href=\""+url['url']+"\" target=\"_blank\"><font color=blue>"+url['url']+"</font></a>")
    for mention in tweet.entities["user_mentions"]:
        t_text=t_text.replace("@"+mention['screen_name'],"<a href=\"http://twitter.com/"+mention['screen_name']+"\" target=\"_blank\"><font color=blue>@"+mention['screen_name']+"</font></a>")
    for hashtag in tweet.entities["hashtags"]:
        t_text=t_text.replace("#"+hashtag['text'],"<a href=\"http://twitter.com/hashtag/"+hashtag['text']+"\" target=\"_blank\"><font color=blue>#"+hashtag['text']+"</font></a>")
    
    return t_text
    
def get_retweets(tweets_id):
    api = get_tweet_api()
    return [api.get_status(idn) for idn in tweets_id]
    
def extract_tweet_info(tweet):
    return {"id":str(tweet.id),
            "date":str(tweet.created_at),
            "text":transform_links(tweet),
            "retweet_count":tweet.retweet_count,
            "favorite_count":tweet.favorite_count,
            "followers":tweet.user.followers_count,
            "friends":tweet.user.friends_count}

def clear_retweets(raw_tweets):
    ret_ids=set([tweet.id for tweet in raw_tweets])
    modeled_tweets=[]
    cont=0
    
    for tweet in raw_tweets:
        try:#It was a retweet
            aux_id = tweet.retweeted_status.id
            if aux_id not in ret_ids:
                modeled_tweets.append(extract_tweet_info(tweet.retweeted_status))
                ret_ids.add(aux_id)
                cont+=1
        except:#It wasn't a retweet
            modeled_tweets.append(extract_tweet_info(tweet))
    
    #~ print(cont)
    
    return modeled_tweets

#Returns a list of 100 tweets of the given query (id,date,text)
def get_tweets(query,types="mixed",MAX_TWEETS = 2000): 
    api = get_tweet_api()

    #~ query = "obama"
    
    #~ result=[]
    #~ ret = api.search(q=query,count=100)
    #~ continue_id = ret[-1].id-1
    #~ cont=0
    #~ 
    #~ while cont<1:
        #~ result = result + ret
        #~ ret = api.search(q=query,count=10,max_id=continue_id)
        #~ continue_id = ret[-1].id-1
        #~ print("cont: ",cont," continue_id: ",continue_id)
        #~ cont+=1
    
    #The cursor allows to get mor than 100 tweets with only 1 instruction
    result = tweepy.Cursor(api.search, q=query, count=100, lang="es", result_type=types).items(MAX_TWEETS)

    #~ tweets2 = [tweet for tweet in result]
    #~ 
    #~ print(len(tweets2))
    #~ 
    #~ save_obj(tweets2,"raw_"+types+"_tweets")
    
    #~ print(len(result))
    tweets =[ tw for tw in result]# if not tw.text.startswith("RT")]
    #~ print(json.dumps(tws,indent=4,separators=(',',':')))
    #~ for tw in tweets:
        #~ print(tw["text"],"\n")
    #~ tweets = [[str(tweet.id), str(tweet.created_at), tweet.text.replace('\n',' ').replace('\r',' ')] for tweet in result]

    #~ for tweet in tweets:
        #~ print(tweet)
    return clear_retweets(tweets)
