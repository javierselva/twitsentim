from random import choice
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def summarize(tweets,polarity,flag=2):
    #~ print (json.dumps(docs, indent=1, ensure_ascii=False))

    #~ print ('\nContadores binarios')
    if flag==0:
        vec = CountVectorizer()
    elif flag==1:
        vec = CountVectorizer(binary=True)
    elif flag==2:
        vec = TfidfVectorizer()
    X = vec.fit_transform([tweet["text"] for tweet in tweets ])
    voca = vec.get_feature_names()


    filas, columnas = X.shape
    A=np.zeros(shape=(filas, columnas))
    for fila in range(filas):
        vf = X.getrow(fila)
        _, cind = vf.nonzero()
        for columna in cind:
            A[fila, columna ] = X[fila, columna]

    #~ print (X)
    #~ print ('-'*20)
    #~ print (A)
    #~ print ('-'*20)
    #~ A = A.T
    #~ print (A)
    #~ print ('-'*20)
    #a = np.random.randn(9, 6) #+ 1j*np.random.randn(9, 6)

    #Reconstruction based on reduced SVD:
    U, s, V = np.linalg.svd(A,full_matrices=False)
    #~ S = np.diag(s)
    
    MAX_RES_TWEETS = 5
    
    
    max_ind = np.argmax(V[:,:MAX_RES_TWEETS+1], axis=0)
    
    
    print("Max_Ind: ",max_ind)
    print("V.shape: ",V.shape)
    
    
    #~ ind = range(0,len(tweets))
    i=MAX_RES_TWEETS-1
    res = []
    while i >= 0:
        r_ch=max_ind[i]
        tweets[r_ch]["polarity"]=polarity[r_ch]
        res.append(tweets[r_ch])
        i -= 1
    
    return res
