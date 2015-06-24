import get_tweets as gt
import get_polarity as gp
import tweet_summary as ts
import pickle

def save_obj(obj, name ):
    with open('summary_test_files/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('summary_test_files/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def clean_tweets(tweets):
    for tweet in tweets:
        tweet["text"]=" ".join([t for t in tweet["text"].split() if not t.startswith("@") and not t.startswith("http")])
    return tweets
    
def add_field(field_name,tweets,field_content):
    cont=0
    for tweet in tweets:
        tweet[field_name]=field_content[cont]
        cont+=1
    return tweets

def store_tweets(tweets,name):
    fil = open("summary_test_files/" + name + ".txt","w+")
    for tweet in tweets:
        fil.write(tweet["text"] + "\n")
    fil.close()

def load_tweets_score(tweets,name):
    fil = open("summary_test_files/" + name + ".txt","r")
    score=[]
    for tweet in tweets:
        fil.readline()
        score.append(int(fil.readline()))
    return score

def download_corpus(query):
    tweets=gt.get_tweets(query)
    save_obj(tweets,"raw_tweets")
    
    print("I have downloaded ",len(tweets),"tweets")
    
    cl_tw=clean_tweets(tweets)
    save_obj(cl_tw,"clean_tweets")
    
    clas_tw=add_field("polarity",cl_tw,gp.get_polarity(cl_tw))
    save_obj(clas_tw,"clean_clas_tweets")
    
    store_tweets(clas_tw,"plain_clean_tweets")
    
if __name__ == "__main__":
    raw_tweets=load_obj("raw_tweets")
    clean_tweets=load_obj("clean_tweets")
    clean_clas_tweets=load_obj("clean_clas_tweets")
    
    raw_score_clas_tweet = load_obj("raw_score_clas_tweet")
    clean_score_clas_tweet = load_obj("clean_score_clas_tweet")
    
    manual_summary=load_obj("manual_summary")
    
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    for i in range(9):
        summary = ts.summarize(tweets=clean_score_clas_tweet,flag=i)
        total_score=0
        for tweet in summary:
            total_score+=tweet["score"]
        
        print("Sistema utilizado: ",flag_key[i],". \t Total score: ",total_score,"\n")
        
        #~ for tweet in summary:
            #~ print("Score: ",tweet["score"],"\t Text: ",tweet["text"][:50],"\n")
