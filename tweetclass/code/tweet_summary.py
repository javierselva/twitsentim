from random import choice
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import math
import os
import re
from copy import deepcopy

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "spanish_stopwords_2.txt")

with open(file_path,"r") as fil:
    stop_words = fil.read().split()

def add_field(field_name,tweets,field_content):
    cont=0
    for tweet in tweets:
        tweet[field_name]=field_content[cont]
        cont+=1
    return tweets

def clean_tweets(tweets,to_clean=["urls","hashtags","mentions"]):
    
    reg_exp={'urls':'\s*https?://[\w.-/]+\s*','mentions':'\s*@[a-zA-Z0-9_]+\s*','hashtags':'\s*#[\w-]+\s*'}
    
    rex = re.compile('|'.join([reg_exp[taca] for taca in to_clean]))
    
    tweets_text=[]
    
    for tweet in tweets:
        tweets_text.append(rex.sub(" ",tweet["text"]))
    
    return tweets_text

def prepare_metric(original_tweets):
    metric1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    metric2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    metric = [math.sqrt(m1*m2) for m1,m2 in zip(metric1,metric2)]
    max_met = max(metric)
    return add_field("metric",original_tweets,[met for met in metric])

def remove_stopwords(tweet):
    return " ".join([word for word in tweet.split() if word not in stop_words])

def summarize(tweets=[],system=5,wrange=4,MAX_RES_TWEETS = 10,use_retweets=True,remove_stop=True,use_cross=True,cleaning=1):
    
    if system==0:
        vec = CountVectorizer()
    elif system==1: # Contadores binarios
        vec = CountVectorizer(binary=True)
    elif system==2:
        vec = CountVectorizer(ngram_range=(1,wrange))
    elif system==3: # TF-IDF: con idf suavizado y normalización 'l2'(opción por defecto)
        vec = TfidfVectorizer()
    elif system==4: # TF normalizado 'l1' (Contadores normalizados para sumar 1)
        vec = TfidfVectorizer(norm='l1', use_idf=False)
    elif system==5: # TF normalizado 'l2' (Contadores normalizados para que el módulo del vector sea 1)
        vec = TfidfVectorizer(norm='l2', use_idf=False)    
    elif system==6: # TF-IDF
        vec = TfidfVectorizer(norm=None, smooth_idf=False)
    elif system==7: # TF-IDF con idf suavizado
        vec = TfidfVectorizer(norm=None, smooth_idf=True)
    elif system==8: # TF-IDF: con idf suavizado y normalización 'l1'
        vec = TfidfVectorizer(norm='l1', smooth_idf=True)
    
    if cleaning==1:
        cleaned_tweets = clean_tweets(tweets)
    elif cleaning==2:
        cleaned_tweets = clean_tweets(tweets,["urls","mentions"])
    else:
        cleaned_tweets = [tweet["text"] for tweet in tweets]
    
    
    if remove_stop:
        X = vec.fit_transform([remove_stopwords(tweet) for tweet in cleaned_tweets ])
    else:
        X = vec.fit_transform(cleaned_tweets)
    voca = vec.get_feature_names()


    filas, columnas = X.shape
    A=np.zeros(shape=(filas, columnas))
    for fila in range(filas):
        vf = X.getrow(fila)
        _, cind = vf.nonzero()
        for columna in cind:
            A[fila, columna ] = X[fila, columna]

    #Reconstruction based on reduced SVD:
    U, s, V = np.linalg.svd(A,full_matrices=False)
    
    #~ print("U: ",U.shape,"\t s: ",s.shape,"\t V: ",V.shape)
    #~ print("S: ",s)
    
    max_ind=[]
    
    if use_retweets and not use_cross:
        prepare_metric(tweets)
        for i in range(len(V)):
            V[i]*=tweets[i]["metric"]
    
    
    
    if use_cross:
        avg_values = np.mean(V,axis=0)
        for tweet in V:
            #Si el valor no supera o iguala la media, lo ponemos a cero
            tweet *= tweet >= avg_values
        #~ hm_sent = len(V)
        #~ for i in range(hm_sent):
            #~ V[i][:hm_sent]*=s
        
        score_values = np.sum(V,axis=1)
        if use_retweets:
            prepare_metric(tweets)
            for i in range(len(score_values)):
                score_values[i]*=tweets[i]["metric"]
        max_ind = np.argsort(-score_values)[:MAX_RES_TWEETS]
    else:
        incr=0
        
        while len(max_ind)<MAX_RES_TWEETS:
            max_ind = np.argmax(V[:,:MAX_RES_TWEETS+1+incr], axis=0)
            max_ind = list(set(max_ind)) # Avoid repetitions
            incr+=1
    
    i=MAX_RES_TWEETS-1
    res = []
    while i >= 0:
        r_ch=max_ind[i]
        res.append(deepcopy(tweets[r_ch]))
        i -= 1
    
    return res
