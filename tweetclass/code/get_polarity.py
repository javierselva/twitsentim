#! /usr/bin/python3
#!encoding:utf8

#~ from random import choice

######################
### APPEND LIBRARY ###
######################
import os
import sys
module_dir = os.path.dirname(__file__)
sys.path.append(module_dir + "/pyELiRF.zip")


######################
### LOAD PREDICTOR ###
######################
file_path = os.path.join(module_dir, 'predictor.b3')

try:
   import cPickle as pickle
except:
   import pickle
with open(file_path, 'rb') as fh:
    predictor = pickle.load(fh)
###############
### PREDICT ###
###############
from pyELiRF.twitter.twitter_ELiRF import clean_tweet

# Classification of the given tweets
# the result is la list the same length of the input, each element 
# containing any of the posible polarities
def get_polarity(tweets):
    #RANDOM CLASIFIER
    #~ classification = [choice(["P+","P","NEU","N","N+","NONE"]) for tweet in tweets]
    #~ return classification
    
    clean_sentences = [clean_tweet(s, mode=5) for s in tweets]
    pred = predictor.predict(clean_sentences)
    
    return pred.tolist()

