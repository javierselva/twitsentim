from random import choice

def summarize(tweets,polarity):
    ind = range(0,len(tweets))
    i=5
    res = []
    while i > 0:
        r_ch=choice(ind)
        tweets[r_ch]["polarity"]=polarity[r_ch]
        res.append(tweets[r_ch])
        i -= 1
    
    return res
