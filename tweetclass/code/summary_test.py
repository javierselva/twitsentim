import get_tweets as gt
import get_polarity as gp
import tweet_summary as ts
import generate_graph as gg
import pickle
from pyrouge import Rouge155
from numpy import *
import re
import json


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
    with open("summary_test_files/" + name + ".txt","w+") as fil:
        for tweet in tweets:
            fil.write(tweet["text"] + "\n")

def clear_file(name):
    with open("summary_test_files/" + name + ".txt","w+") as fil:
        fil.write("")

def load_tweets_score(tweets,name):
    with open("summary_test_files/" + name + ".txt","r") as fil:
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
    output_dict = r.output_to_dict(output)
    with open("summary_test_files/summary_rouge_results_"+num+"/results.txt","a+") as fil:
    #~ print(output)
        for version in ["1","2","3","4","l","w_1.2","s*","su*"]:
            for res in ["recall","precision","f_score"]:
                fil.write("%0.5f" % output_dict["rouge_"+version+"_"+res]+"\n")
    
def process_rouge_output(num):
    fil = open("summary_test_files/summary_rouge_results_"+num+"/results.txt","r")
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td rowspan=2 align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td><td colspan=3>ROUGE-1</td><td colspan=3>ROUGE-2</td><td colspan=3>ROUGE-3</td><td colspan=3>ROUGE-4</td><td colspan=3>ROUGE-L</td><td colspan=3>ROUGE-W-1.2</td><td colspan=3>ROUGE-S*</td><td colspan=3>ROUGE-SU*</td><td rowspan=2 align=\"center\" valing=\"center\">Recuento</td></tr><tr style=\"background-color:#CCCCCC\" align=\"center\"><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td><td>R</td><td>P</td><td>F</td></tr>")
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    
    aux = fil.read().split("\n")[:216]
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
    original_tweets = load_obj("summary_raw_"+test_number+"/original_tweets")
    
    original_tweets = clean_tweets(original_tweets)
    
    clear_file("summary_results_"+test_number+"/summary_flagged.001")
    clear_file("summary_results_"+test_number+"/summary_flagged.002")
    clear_file("summary_rouge_results_"+test_number+"/results.txt")
    
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td>Sistema empleado</td><td>Total score</td><td>Number of suc. tweets</td><td>Avg. RT count</td></tr>")
    summary_tweets_data = ""
    for i in range(9):
        mrt=10
        summary = ts.summarize(tweets=original_tweets,use_retweets=True,flag=i,MAX_RES_TWEETS = mrt)
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.001")
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.002")
        
        #~ store_tweets(summary,"summary_results_"+test_number+"/summary_culete"+str(i))
        
        rouge_test(test_number)
        
        total_score=0
        tweets_in_summary=0
        avg_retweets=0
        for tweet in summary:
            total_score+=tweet["score"]
            avg_retweets+=tweet["retweet_count"]
            if tweet["score"]>6:
                tweets_in_summary+=1
        
        
        
        print("<tr align=\"center\"><td style=\"background-color:#AAAAAA\">",flag_key[i],"</td><td>",total_score,"</td><td>",tweets_in_summary,"</td><td>",avg_retweets/mrt,"</td></tr>")
        
        if verbose:
            summary_tweets_data+="<h4>"+flag_key[i]+"</h4> "
            for tweet in summary:
                summary_tweets_data+= "Score: "+str(tweet["score"])+"|| RT: "+str(tweet["retweet_count"])+"|| Id: "+tweet["id"]+"|| Text: "+tweet["text"][:50]+"<br />"
    print("</table><br />")
    
    process_rouge_output(test_number)
    if verbose:
        print("<br />"+summary_tweets_data)
    
if __name__ == "__main__":
    
    raw_mixed_tweets = load_obj("raw_mixed_tweets")
    #~ 
    #~ tweets = load_obj("modeled_mixed_scored_tweets")
    #~ tweets = gt.clear_retweets(raw_mixed_tweets)
    #~ save_obj(add_field("score",tweets,load_tweets_score(tweets,"plain_mixed_tweets")),"modeled_mixed_scored_tweets")
    
    
    tweets=load_obj("modeled_mixed_scored_tweets")
    sorted(tweets,lambda key k : "retweet_count")
    gg.draw_rt_vs_score([tweet["retweet_count"] for tweet in tweets],[tweet["favorite_count"] for tweet in tweets],[tweet["score"] for tweet in tweets])
    
    if False:
        test_number = "10"
        print("<meta http-equiv=\"Content-type\" content=\"text/html;charset=ISO-8859-1\">")
        print("<h1>Test #"+test_number+"</h1>")
        #TWEETS TAL CUAL #2 - #5
        #~ print("<br /> Esta primera prueba con el nuevo corpus entrenado consiste en un resumen realizado simplemente considerando los tweets con score >6 sin hashtags y habiendo eliminado manualmente los repetidos. El conjunto de tweets es el original, del que se han eliminado los que eran RT y se han añadido los originales de los mismos.")
        #~ print("<br /> La segunda prueba es igual que la anterior pero en este caso limpiamos los tweets antes de realizar el resumen.")
        #~ print("<br /> Es igual que el primero, pero utilizando en el model de resumen los tweets con hashtags")
        #~ print("<br /> Es igual que el segundo, pero utilizando en el modelo de resumen los tweets con hashtags y al limpiar, dejando los hashtags")
        
        #ELIMINANDO LOS QUE TENGAN RT DEBAJO DE LA MEDIA #6 - #9
        #~ print("<br /> En este caso, empleando el resumen sin hashtags como modelo, se ha intentado dar más relevancia a los retweets mediante la modificación de la matriz. Si el número de RT de un tweet concreto es inferior a la MEDIA de RT de todos los tweets, ese tweet no se cogerá.")
        #~ print("<br /> Igual que el anterior (descartando un tweet si sus RT son inferiores a la media) pero esta vez limpiando los tweets")
        #~ print("<br /> Igual que #6 pero trabajando con el modelo resumen con hashtags")
        #~ print("<br /> Igual que el anterior pero limpiando urls y menciones")
        
        #ELIMINANDO LOS QUE TENGAN RT DEBAJO DEL PERCENTIL
        print("<br /> Descarta los tweets que tengan RT por debajo del percentil (70). Resumen modelo sin hashtags y tweets limpiados.")
        launch_test(test_number,True)
