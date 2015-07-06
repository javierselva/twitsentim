import get_tweets as gt
import get_polarity as gp
import tweet_summary as ts
import generate_graph as gg
import pickle
from pyrouge import Rouge155
from numpy import *
import re


def save_obj(obj, name ):
    with open('summary_test_files/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('summary_test_files/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def clean_tweets(tweets,to_clean=["urls","hashtags","mentions"]):
    
    reg_exp={'urls':'\s*https?://[\w.-/]+\s*','mentions':'\s*@[a-zA-Z0-9_]+\s*','hashtags':'\s*#[\w-]+\s*'}
    
    rex = re.compile('|'.join([reg_exp[taca] for taca in to_clean]))
    
    for tweet in tweets:
        tweet["text"]=rex.sub("",tweet["text"])
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

def rouge_test(num):
    r = Rouge155()
    r.system_dir = 'summary_test_files/summary_results_'+num+'/'
    r.model_dir = 'summary_test_files/summary_model_'+num+'/'
    r.system_filename_pattern = 'summary_flagged.(\d+).txt'
    r.model_filename_pattern = 'manual_summary.txt'

    output = r.convert_and_evaluate()
    fil = open("summary_test_files/summary_rouge_results_"+num+"/results.txt","a+")
    print(output)
    output_dict = r.output_to_dict(output)
    for version in ["1","2","3","4","l","w_1.2","s*","su*"]:
        for res in ["recall","precision","f_score"]:
            fil.write("%0.5f" % output_dict["rouge_"+version+"_"+res]+"\n")
    fil.close()
    
def process_rouge_output(num):
    fil = open("summary_test_files/summary_rouge_results_"+num+"/results.txt","r")
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td rowspan=2 align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td><td colspan=3>ROUGE-1</td><td colspan=3>ROUGE-2</td><td colspan=3>ROUGE-3</td><td colspan=3>ROUGE-4</td><td colspan=3>ROUGE-L</td><td colspan=3>ROUGE-W-1.2</td><td colspan=3>ROUGE-S*</td><td colspan=3>ROUGE-SU*</td><td rowspan=2 align=\"center\" valing=\"center\">Recuento</td></tr><tr style=\"background-color:#CCCCCC\" align=\"center\"><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td></tr>")
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    
    aux = fil.read().split("\n")[1:217]
    [aux.append("0.000000000000000000000") for x in range(24)]
    values=array(aux).reshape((10,24))
    max_val_ind = argmax(values,axis=0).tolist()
    
    
    for col in range(len(max_val_ind)):
        row=max_val_ind[col]
        values[row][col]="<b>"+values[row][col]+"</b>"
    
    
    for system in range(9):
        print("<tr><td style=\"background-color:#AAAAAA\">"+flag_key[system]+"</td>")
        for r in range(24):
            print("<td>"+values[system][r]+"</td>")
        print("<td align=\"center\">"+str(max_val_ind.count(system))+"</td>")
        print("</tr>")
        
    print("</table>")
    fil.close()

def launch_test(test_number,verbose=False):
    original_tweets = load_obj("summary_raw_"+test_number+"/clean_score_clas_tweet")
    
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td>Sistema empleado</td><td>Total score</td><td>Number of suc. tweets</td><td>Avg. RT count</td></tr>")
    
    for i in range(9):
        mrt=10
        summary = ts.summarize(tweets=original_tweets,flag=i,MAX_RES_TWEETS = mrt)
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.001")
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.002")
        
        rouge_test(test_number)
        
        total_score=0
        tweets_in_summary=0
        avg_retweets=0
        for tweet in summary:
            total_score+=tweet["score"]
            #~ avg_retweets+=tweet["retweet_count"]
            if tweet["score"]>6:
                tweets_in_summary+=1
        
        
        
        print("<tr align=\"center\"><td style=\"background-color:#AAAAAA\">",flag_key[i],"</td><td>",total_score,"</td><td>",tweets_in_summary,"</td></tr>")#,avg_retweets/mrt,"</td></tr>")
        
        if verbose:
            for tweet in summary:
                print("Score: ",tweet["score"],"\t Text: ",tweet["text"][:50],"\t Id: ",tweet["id"],"\t RT: ",tweet["retweet_count"])
    print("</table>")
    process_rouge_output(test_number)
    
if __name__ == "__main__":
    
    #~ raw_mixed_tweets = load_obj("raw_mixed_tweets")
    #~ 
    #~ modeled_mixed_tweets = load_obj("modeled_mixed_tweets")
    
    test_number = "02"
    description = ""
    
    launch_test("01")
    
    #~ process_rouge_output("01","pene")
    
    #LANZA TEST:
