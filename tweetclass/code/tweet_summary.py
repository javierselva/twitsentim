from random import choice
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def summarize(tweets=[],polarity=[],flag=0,rango=4):
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
    
    MAX_RES_TWEETS = 5
    
    max_ind = np.argmax(V[:,:MAX_RES_TWEETS+1], axis=0)
    
    #~ print("Max_Ind: ",max_ind)
    #~ print("V.shape: ",V.shape)
    
    i=MAX_RES_TWEETS-1
    res = []
    while i >= 0:
        r_ch=max_ind[i]
        tweets[r_ch]["polarity"]=polarity[r_ch]
        res.append(tweets[r_ch])
        i -= 1
    
    return res
