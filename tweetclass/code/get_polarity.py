from random import choice

# Random classification of the given tweets
# the result is la list the same length of the input, each element 
# containing any of the posible polarities
def get_polarity(tweets):
    classification = [choice(["P+","P","NEU","N","N+","NONE"]) for tweet in tweets]
    return classification

#~ tweets=["a","b","c","a","b","c","a","b","c"]
#~ print(get_polarity(tweets))
