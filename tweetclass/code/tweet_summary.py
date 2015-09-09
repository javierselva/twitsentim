'''
@file:      tweetclass/code/tweet_summary.py
@author:    Javier Selva Castello
@date:      2015
@desc:      This file contains all the necessary functions to produce a tweet's summary.
'''

from random import choice
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import math
import os
import re
from copy import deepcopy

#Set the path for the stopwords file
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "spanish_stopwords_2.txt")

#Open the stopword file and set stop_words as a list of stopwords
with open(file_path,"r") as fil:
    stop_words = fil.read().split()

'''
@name:      add_field
@desc:      Adds a (key,value) tuple to each dictionary contained in a list of dics
@params:    field_name      - a string containing the name of the field to be added (the key)
            tweets          - a list of diccionaries on which to add the field
            field_content   - a list containing the values to be added to each dictionary
@return:    nothing, as it modifies the list referenced in the param "tweets"
'''
def add_field(field_name,tweets,field_content):
    cont=0
    for tweet in tweets:
        tweet[field_name]=field_content[cont]
        cont+=1

'''
@name:      clean_tweets
@desc:      Ereases different twitter entities (urls, hashtags and/or mentions) from a list of tweets
@params:    tweets      - a list of dictionaries, each of which represeinting a tweet and containing 
                          at least the key "text
            to_clean    - a list with the one to three entities to remove from the tweets.
                          by default it is all of them
@return:    list of strings - a list of tweets (just the text) whitout the entities requested
'''
def clean_tweets(tweets,to_clean=["urls","hashtags","mentions"]):
    #reg_exp contains all the regex needed to find the different entities entities 
    reg_exp={'urls':'\s*https?://[\w.-/]+\s*','mentions':'(?:\s+|^)@[\w_]+\s*','hashtags':'\s*#[\w-]+\s*'}
    
    #compile the regular expressions to be found
    rex = re.compile('|'.join([reg_exp[taca] for taca in to_clean]))
    
    tweets_text=[]
    #erease all the entities from the original tweets and add the clean tweets to tweets_text
    for tweet in tweets:
        tweets_text.append(rex.sub(" ",tweet["text"]))
    
    return tweets_text

'''
@name:      prepare_metric
@desc:      Calculates the popularity metric value for each tweet
@params:    original_tweets - a list of tweets (in the form of dictionaries) containing at least 
                              the fields "followers", "friends", "retweet_count" and "favorite_count"
@returns:   nothing, as it modifies the list referenced in the param "original_tweets"
'''
def prepare_metric(original_tweets):
    #First part of the metric containing the relationship between followers and friends (F^2/f)
    metric1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    
    #Second part of the metric containing the relationship betweet retweets, favorites and followers (RT*1'5+Fav)/log(F)
    metric2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    
    #Third part of the metric where the first two become just one (sqrt(metric1*metric2))
    metric = [math.sqrt(m1*m2) for m1,m2 in zip(metric1,metric2)]
    max_met = max(metric)
    #Adds a the "metric" field to each tweet with the pertinent value
    add_field("metric",original_tweets,[met for met in metric])

'''
@name:      remove_stopwords
@desc:      Removes the stopwords in a tweet 
@params:    tweet - a string containing the tweet text from where to remove the stopwords
@returns:   string - the string without stopwords
'''
def remove_stopwords(tweet):
    return " ".join([word for word in tweet.split() if word not in stop_words])

'''
@name:      summarize
@desc:      Creates a tweet summary out of a list of tweets. All the default params where proved to output better 
            summaries. 
@params:    tweets          - a list of dictionaries containing all the tweet info necessary to generate the summary (at least the "text")
                              If use_retweets is enabled, the tweets should also contain the fields "followers", "friends", 
                              "retweet_count" and "favorite_count"
            system          - integer value between 0 and 8. The system indicates the values that the matrix will contain
                              to represent the importance of a concept in a sentence:
                                  0 - Counters
                                  1 - Binary Counters
                                  2 - N-gram Counter
                                  3 - TF-IDF: with smoothen IDF and 'l2' normalization
                                  4 - TF with 'l1' normalization (Normalized counters to sum up to 1)
                                  5 - TF with 'l1' normalization (Normalized counters in order to the vector's module to be 1)
                                  6 - TF-IDF
                                  7 - TF-IDF with smoothen IDF
                                  8 - TF-IDF: with smoothen IDF and 'l2' normalization
            wrange          - integer value greater or equal to 1. It is only used if system = 2, is the N in N-grams
            MAX_RES_TWEETS  - integer value containing the amount of tweets that will be in the summary result
            use_retweets    - boolean indicating whether the popularity values should be used or not for the summary generation
            remove_stop     - boolean indicating whether or not the stopwords should be removed from the tweets
            use_cross       - boolean indicating whether or not the cross method for tweet selection should be used
            cleaning        - integer containging the amount of "cleaning" (removing of entities) that should be made:
                                0 - No cleaning at all
                                1 - All the entities will be removed
                                2 - All the entities but hashtags will be removed
@returns:   a list of dicctionaries (tweets) of length MAX_RES_TWEETS containing the summary tweets
            If SVD does not converge, it returns an empty list
'''
def summarize(tweets,system=5,wrange=4,MAX_RES_TWEETS = 10,use_retweets=True,remove_stop=True,use_cross=True,cleaning=1):
    
    #Creates the vectorizer depending on the system choosen by param
    if system==0:   # Counters
        vec = CountVectorizer()
    elif system==1: # Binary Counters
        vec = CountVectorizer(binary=True)
    elif system==2: # N-gram Counter
        vec = CountVectorizer(ngram_range=(1,wrange))
    elif system==3: # TF-IDF: with smoothen IDF and 'l2' normalization
        vec = TfidfVectorizer()
    elif system==4: # TF with 'l1' normalization (Normalized counters to sum up to 1)
        vec = TfidfVectorizer(norm='l1', use_idf=False)
    elif system==5: # TF with 'l1' normalization (Normalized counters in order to the vector's module to be 1)
        vec = TfidfVectorizer(norm='l2', use_idf=False)    
    elif system==6: # TF-IDF
        vec = TfidfVectorizer(norm=None, smooth_idf=False)
    elif system==7: # TF-IDF with smoothen IDF
        vec = TfidfVectorizer(norm=None, smooth_idf=True)
    elif system==8: # TF-IDF: with smoothen IDF and 'l2' normalization
        vec = TfidfVectorizer(norm='l1', smooth_idf=True)
    
    #Cleans the tweet's text depending on the amount of cleaning specified by param
    if cleaning==1:     # Removes all entities
        cleaned_tweets = clean_tweets(tweets)
    elif cleaning==2:   # Removes all entities but hashtags
        cleaned_tweets = clean_tweets(tweets,["urls","mentions"])
    else:               # Removes no entities at all
        cleaned_tweets = [tweet["text"] for tweet in tweets]
    
    # Creates the sparese matrix containing the values setted by the system
    if remove_stop: # removing stopwords ...
        X = vec.fit_transform([remove_stopwords(tweet) for tweet in cleaned_tweets ])
    else:           # ... or not
        X = vec.fit_transform(cleaned_tweets)
    
    # Transforms the matrix from sparse to full
    filas, columnas = X.shape
    A=np.zeros(shape=(filas, columnas))
    for fila in range(filas):
        vf = X.getrow(fila)
        _, cind = vf.nonzero()
        for columna in cind:
            A[fila, columna ] = X[fila, columna]

    # Reconstruction based on reduced SVD
    try:
        U, s, V = np.linalg.svd(A,full_matrices=False) # V contains a relationship betweet tweets and concepts
    except:
        return []

    
    max_ind=[]
    
    # If the tweet extraction from the matrix is done by the cross method
    if use_cross:
        # Calculates the average value for each concept
        avg_values = np.mean(V,axis=0)
        for tweet in V:
            #If the value for a concept isn't greater or equal to the average of that concept, the value is set to zero
            tweet *= tweet >= avg_values
        # These lines where used before the cross method was modified
        # Them multiply the V matrix with the S matrix for a given number of columns
        #~ hm_sent = len(V)
        #~ for i in range(hm_sent):
            #~ V[i][:hm_sent]*=s
        
        #The score of every sentence is calculated
        score_values = np.sum(V,axis=1)
        # If using retweets the metric has to be prepared
        if use_retweets:
            prepare_metric(tweets)
            # If cross method is being used, the metric affects to the score of each tweet
            for i in range(len(score_values)):
                score_values[i]*=tweets[i]["metric"]
        # Get the indices of the tweets that will be part of the summary
        max_ind = np.argsort(-score_values)[:MAX_RES_TWEETS]
    # If the tweet extraction from the matrix is done by the 
    else:
        
        # If using retweets the metric has to be prepared
        if use_retweets:
            prepare_metric(tweets)
            # If the cross method is not being used, the metric affects to each row
            for i in range(len(V)):
                V[i]*=tweets[i]["metric"]
        
        incr=0
        # Iterate extracting the tweets that are more related to the most important concepts
        while len(max_ind)<MAX_RES_TWEETS:
            max_ind = np.argmax(V[:,:MAX_RES_TWEETS+1+incr], axis=0)
            max_ind = list(set(max_ind)) # Avoid repetitions
            incr+=1
    
    i=MAX_RES_TWEETS-1
    res = []
    while i >= 0:
        r_ch=max_ind[i]
        # Append the selected tweets to the result list
        res.append(deepcopy(tweets[r_ch])) # DeepCopy is needed in order to allow future modification of the tweets
        i -= 1
    
    return res
