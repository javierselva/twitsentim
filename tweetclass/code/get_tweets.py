import tweepy
import json

#Returns a list of 100 tweets of the given query (id,date,text)
def get_tweets(query): 
    #In this first call we need consumer keys
    #Firstly the key and secondly the secret
    auth = tweepy.OAuthHandler("TNEMlsyO36DXIAjfMabHJhTyq", "Jnw7eyaqMjP0RXaFRqwxRiIKySQ2HBlMDy5flsCcpcP9qzVaCS")
    #In this second call we need access tokens
    auth.set_access_token("3293977216-ueXKhR68gsS4XkBSBxpIIXh6WxQ5ETSoTrrc2UF", "ZB7EFTD2Ti6OY01FpyfYV8DvKuVt9YbI0e0sviZs1HsTs")
    api = tweepy.API(auth)

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
    MAX_TWEETS = 500
    result = tweepy.Cursor(api.search, q=query, count=100, lang="es").items(MAX_TWEETS)

    #~ print(len(result))
    tweets =[ {"id":str(tw.id),"date":str(tw.created_at),"text":tw.text.replace('\n',' ').replace('\r',' ')} for tw in result]# if not tw.text.startswith("RT")]
    #~ print(json.dumps(tws,indent=4,separators=(',',':')))
    #~ for tw in tweets:
        #~ print("User: ",tw["user"],"\n")
    #~ tweets = [[str(tweet.id), str(tweet.created_at), tweet.text.replace('\n',' ').replace('\r',' ')] for tweet in result]

    #~ for tweet in tweets:
        #~ print(tweet)
    return tweets
