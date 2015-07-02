import get_tweets as gt
import get_polarity as gp
import tweet_summary as ts
import pickle
from pyrouge import Rouge155
from numpy import *

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
        fil.write(tweet["text"] + "\n\n")
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

def rouge_test():
    r = Rouge155()
    r.system_dir = 'summary_test_files/summary_results_01/'
    r.model_dir = 'summary_test_files/summary_model_01/'
    r.system_filename_pattern = 'summary_flagged.(\d+).txt'
    r.model_filename_pattern = 'manual_summary.txt'

    output = r.convert_and_evaluate()
    print(output)
    output_dict = r.output_to_dict(output)

def process_rouge_output(num,name):
    fil = open("summary_test_files/summary_rouge_results_"+num+"/" + name + ".txt","r")
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td rowspan=2 align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td><td colspan=3>ROUGE-1</td><td colspan=3>ROUGE-2</td><td colspan=3>ROUGE-3</td><td colspan=3>ROUGE-4</td><td colspan=3>ROUGE-L</td><td colspan=3>ROUGE-W-1.2</td><td colspan=3>ROUGE-S*</td><td colspan=3>ROUGE-SU*</td></tr><tr style=\"background-color:#CCCCCC\" align=\"center\"><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td></tr>")
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    
    aux = fil.read().replace("\n\n","\n").replace("\n\n","\n").split("\n")[1:217]
    [aux.append("0.000000000000000000000") for x in range(24)]
    values=array(aux).reshape((10,24))
    max_val_ind = argmax(values,axis=0)
    #~ print(values)
    
    #~ values[0][0]="<b>"+values[0][0]
    
    for col in range(len(max_val_ind)):
        row=max_val_ind[col]
        values[row][col]="<b>"+values[row][col]+"</b>"
    
    #~ print(values)
    
    for system in range(9):
        print("<tr><td style=\"background-color:#AAAAAA\">"+flag_key[system]+"</td>")
        for r in range(24):
            print("<td>"+values[system][r]+"</td>")
        print("</tr>")
        
    print("</table>")
    

if __name__ == "__main__":
    
    #~ raw_mixed_tweets = load_obj("raw_mixed_tweets")
    #~ 
    #~ modeled_mixed_tweets = gt.clear_retweets(raw_mixed_tweets)
    #~ 
    #~ save_obj(modeled_mixed_tweets,"modeled_mixed_tweets")
    #~ 
    #~ store_tweets(modeled_mixed_tweets,"plain_mixed_tweets")
    
    process_rouge_output("01","pene")
    
    
    #~ raw_tweets=load_obj("raw_tweets")
    #~ clean_tweets=load_obj("clean_tweets")
    #~ clean_clas_tweets=load_obj("clean_clas_tweets")
    
    #~ raw_score_clas_tweet = load_obj("raw_score_clas_tweet")
    
    
    
    #LANZA TEST:
    
    #~ clean_score_clas_tweet = load_obj("summary_raw_01/clean_score_clas_tweet")
    #~ 
    #~ manual_summary=load_obj("summary_raw_01/manual_summary")
    #~ 
    #~ flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    #~ 
    #~ for i in range(9):
        #~ summary = ts.summarize(tweets=clean_score_clas_tweet,flag=i,MAX_RES_TWEETS = 10)
        #~ store_tweets(summary,"summary_results_01/summary_flagged.001")
        #~ store_tweets(summary,"summary_results_01/summary_flagged.002")
        #~ rouge_test()
        #~ total_score=0
        #~ tweets_in_summary=0
        #~ for tweet in summary:
            #~ total_score+=tweet["score"]
            #~ if tweet["score"]>6:
                #~ tweets_in_summary+=1
        #~ 
        #~ print("Sistema utilizado: ",flag_key[i],". \t Total score: ",total_score,"\t Number of suc. tweets: ",tweets_in_summary,"\n")
        #~ 
        #~ for tweet in summary:
            #~ print("Score: ",tweet["score"],"\t Text: ",tweet["text"][:50],"\t Id: ",tweet["id"])
    
