from random import choice
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

with open("spanish_stopwords.txt","r") as fil:
    stop_words = fil.read().split()

def remove_stopwords(tweet):
    return " ".join([word for word in tweet.split() if word not in stop_words])


def summarize(tweets=[],polarity=[],flag=1,rango=4,MAX_RES_TWEETS = 5,use_retweets=False,remove_stop=False,use_cross=False):
    #~ print (json.dumps(docs, indent=1, ensure_ascii=False))
    
    if flag==0:
        vec = CountVectorizer()
    elif flag==1: # Contadores binarios
        vec = CountVectorizer(binary=True)
    elif flag==2:
        vec = CountVectorizer(ngram_range=(1,rango))
    elif flag==3: # TF-IDF: con idf suavizado y normalización 'l2'(opción por defecto)
        vec = TfidfVectorizer()
    elif flag==4: # TF normalizado 'l1' (Contadores normalizados para sumar 1)
        vec = TfidfVectorizer(norm='l1', use_idf=False)
    elif flag==5: # TF normalizado 'l2' (Contadores normalizados para que el módulo del vector sea 1)
        vec = TfidfVectorizer(norm='l2', use_idf=False)    
    elif flag==6: # TF-IDF
        vec = TfidfVectorizer(norm=None, smooth_idf=False)
    elif flag==7: # TF-IDF con idf suavizado
        vec = TfidfVectorizer(norm=None, smooth_idf=True)
    elif flag==8: # TF-IDF: con idf suavizado y normalización 'l1'
        vec = TfidfVectorizer(norm='l1', smooth_idf=True)
        
    
    
    
    if remove_stop:
        X = vec.fit_transform([remove_stopwords(tweet["text"]) for tweet in tweets ])
    else:
        X = vec.fit_transform([tweet["text"] for tweet in tweets ])
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
    
    if use_retweets:
        #~ avg_rt=np.mean([tweet["retweet_count"] for tweet in tweets])
        retweets_ftw=[tweet["retweet_count"] for tweet in tweets]
        avg_rt=np.percentile(retweets_ftw,80)
        #~ print(retweets_ftw.count(0))
        for i in range(len(V)):
            if tweets[i]["retweet_count"]<avg_rt:
                V[i]*=0
    max_ind=[]
    
    if use_cross:
        avg_values = np.mean(V,axis=0)
        for tweet in V:
            #Si el valor no supera o iguala la media, lo ponemos a cero
            tweet *= tweet >= avg_values
        #~ for i in range(len(s)):
            #~ V[i]*=s[i]
        score_values = np.sum(V,axis=1)
        max_ind = np.argsort(-score_values)[:MAX_RES_TWEETS]
    else:
        incr=0
        
        while len(max_ind)<MAX_RES_TWEETS:
            max_ind = np.argmax(V[:,:MAX_RES_TWEETS+1+incr], axis=0)
            max_ind = list(set(max_ind)) # Avoid repetitions
            incr+=1
    #~ print("Max_Ind: ",max_ind)
    #~ print("V.shape: ",V.shape)
    
    i=MAX_RES_TWEETS-1
    res = []
    while i >= 0:
        r_ch=max_ind[i]
        if len(polarity)>0:
            tweets[r_ch]["polarity"]=polarity[r_ch]
        res.append(tweets[r_ch])
        i -= 1
    
    return res
