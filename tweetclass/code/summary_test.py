#!encoding:utf8

import get_tweets as gt
import get_polarity as gp
import tweet_summary as ts
import generate_graph as gg
import pickle
from pyrouge import Rouge155
from numpy import *
import re
import math
import numpy as np
import sys



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

def try_regex(tweet,to_clean=["urls","hashtags","mentions"]):
    reg_exp={'urls':'\s*https?://[\w.-/]+\s*','mentions':'\s*@[a-zA-Z0-9_]+\s*','hashtags':'\s*#[\w-]+\s*'}
    
    rex = re.compile('|'.join([reg_exp[taca] for taca in to_clean]))
    return rex.findall(tweet)

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

def resume_tablas_rouge():
    
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    #PRINTA LAS TABLAS NORMALES (POR SISTEMAS)
    matrices_chachis=[]
    for c in ["","-C","-RT","-RT_2"]:
        for i in range(2,10):
            name = "0"+str(i)+c
            with open("summary_test_files/summary_rouge_results_"+name+"/resultados.html") as fil:
                print("<h2>"+name+"</h2>")
                todo = fil.read()
                trozos = todo.split("<table")
                tabla_rouge = trozos[2].replace("<b>","").replace("</b>","")
                filas = tabla_rouge.split("<tr>")
                    
                
                tabla_basica = trozos[1].split("<tr")
                chachi_matriz_1=[["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"]]
                for fila in tabla_basica[2:]:
                    elems = fila.split("<td>")[1:]
                    clean_elems = [elem.replace("</td>","") for elem in elems]
                    clean_elems[-1] = clean_elems[-1].split("</tr>")[0]
                    chachi_matriz_1.append(clean_elems)
                
                print("<table border=1> \
                            <tr style=\"background-color:#AAAAAA\" align=\"center\"> \
                                 <td align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td> \
                                 <td>ROUGE-4</td> \
                                 <td>ROUGE-L</td> \
                                 <td>ROUGE-W</td> \
                                 <td>ROUGE-SU*</td> \
                                 <td>Total score</td> \
                                 <td>Number of suc. tweets</td> \
                                 <td>Avg. RT count</td> \
                                 <td>Avg. Fav count</td> \
                                 <td>Avg. Followers</td> \
                            </tr>")
                            
                chachi_matriz_2 = [["00000000000000000000","00000000000000000000","00000000000000000000","00000000000000000000"]]
                for fila in filas[1:]:
                    columnas = fila.split("<td>")
                    chachi_matriz_2.append([columnas[col][:7] for col in [12, 15, 18, 24] ])
                
                chachi_matriz=np.concatenate((chachi_matriz_2,chachi_matriz_1),axis=1)
                chachi_matriz = chachi_matriz[1:]
                max_val_ind = argmax(chachi_matriz.astype(np.float),axis=0).tolist()
                
                for col in range(len(max_val_ind)):
                    row=max_val_ind[col]
                    chachi_matriz[row][col]="<b>"+chachi_matriz[row][col]+"</b>" 
                
                matrices_chachis.append(chachi_matriz)
                
                for fila in range(len(chachi_matriz)):
                    print("<tr><td style=\"background-color:#AAAAAA\">"+flag_key[fila]+"</td>")
                    for col in chachi_matriz[fila]:
                        print("<td align=center>"+col+"</td>")
                    print("</tr>")
                    
                print("</table>")
                print("<a href=\"./summary_rouge_results_"+name+"/resultados.html\" target=\"_blank\">Tabla original</a>")
                print("<br \><br \>")
    #PRINTA LAS TABLAS RESUMEN (POR CARACTERÍSTICAS)        
    measures = ["ROUGE-4","ROUGE-L","ROUGE-W","ROUGE-SU*","Total score","Number of suc. tweets","Avg. RT count","Avg. Fav count","Avg. Followers"]
    cont1=0
    todas_victorias = []
    for measure in measures:
        print("<h2>"+measure+"</h2>")
        print("<table border=1> \
                            <tr align=\"center\"> \
                                 <td style=\"background-color:#AAAAAA\" align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td> \
                                 <td style=\"background-color:#CCCCCC\">02</td> \
                                 <td style=\"background-color:#CCCCCC\">03</td> \
                                 <td style=\"background-color:#CCCCCC\">04</td> \
                                 <td style=\"background-color:#CCCCCC\">05</td> \
                                 <td style=\"background-color:#CCCCCC\">06</td> \
                                 <td style=\"background-color:#CCCCCC\">07</td> \
                                 <td style=\"background-color:#CCCCCC\">08</td> \
                                 <td style=\"background-color:#CCCCCC\">09</td> \
                                 <td style=\"background-color:#999999\">02-C</td> \
                                 <td style=\"background-color:#999999\">03-C</td> \
                                 <td style=\"background-color:#999999\">04-C</td> \
                                 <td style=\"background-color:#999999\">05-C</td> \
                                 <td style=\"background-color:#999999\">06-C</td> \
                                 <td style=\"background-color:#999999\">07-C</td> \
                                 <td style=\"background-color:#999999\">08-C</td> \
                                 <td style=\"background-color:#999999\">09-C</td> \
                                 <td style=\"background-color:#CCCCCC\">02-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">03-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">04-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">05-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">06-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">07-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">08-RT</td> \
                                 <td style=\"background-color:#CCCCCC\">09-RT</td> \
                                 <td style=\"background-color:#999999\">02-RT_2</td> \
                                 <td style=\"background-color:#999999\">03-RT_2</td> \
                                 <td style=\"background-color:#999999\">04-RT_2</td> \
                                 <td style=\"background-color:#999999\">05-RT_2</td> \
                                 <td style=\"background-color:#999999\">06-RT_2</td> \
                                 <td style=\"background-color:#999999\">07-RT_2</td> \
                                 <td style=\"background-color:#999999\">08-RT_2</td> \
                                 <td style=\"background-color:#999999\">09-RT_2</td> \
                                 <td style=\"background-color:#CCCCCC\">Victorias</td> \
                            </tr>")
        victorias = ["00000000000"]
        for cont3 in range(9):
            cont2=0
            print("<tr><td style=\"background-color:#AAAAAA\">"+flag_key[cont3]+"</td>")
            victoria = 0
            for c in ["","-C","-RT","-RT_2"]:
                for i in range(2,10):
                    name = "0"+str(i)+c
                    esta_celda = matrices_chachis[cont2][cont3][cont1]
                    if esta_celda.startswith("<b>"):
                        victoria+=1
                    print("<td>"+esta_celda+"</td>")
                    cont2+=1
            print("<td>"+str(victoria)+"</td>")
            victorias.append(str(victoria))
            print("</tr>")
        todas_victorias.append(victorias)
        print("</table>")
        print("Ganador: ",flag_key[argmax(victorias[1:])])
        cont1+=1
        
    todas_victorias = np.array(todas_victorias).transpose()
    
    max_val_ind = argmax(todas_victorias.astype(np.float),axis=0).tolist()
            
    for col in range(len(max_val_ind)):
        row=max_val_ind[col]
        todas_victorias[row][col]="<b>"+todas_victorias[row][col]+"</b>" 
    
    todas_victorias = todas_victorias[1:]
    print("<br /><br />")
    print("<h2>Recuento de victorias</h2><table border=1> \
                            <tr style=\"background-color:#AAAAAA\" align=\"center\"> \
                                 <td align=\"center\" valing=\"center\" width=\"200\">SISTEMA EMPLEADO</td> \
                                 <td>ROUGE-4</td> \
                                 <td>ROUGE-L</td> \
                                 <td>ROUGE-W</td> \
                                 <td>ROUGE-SU*</td> \
                                 <td>Total score</td> \
                                 <td>Number of suc. tweets</td> \
                                 <td>Avg. RT count</td> \
                                 <td>Avg. Fav count</td> \
                                 <td>Avg. Followers</td> \
                            </tr>")
    cont = 0
    for x in todas_victorias:
        print("<tr><td style=\"background-color:#AAAAAA\">"+flag_key[cont]+"</td>")
        for y in x:
            print("<td>"+y+"</td>")
        print("</tr>")
        cont+=1
    print("</table>")
    
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

def launch_test(test_number,clean_sys=0,rt=False,cr=False,stop=False,verbose=False):
    original_tweets = load_obj("summary_raw_"+test_number+"/original_tweets")
    
    if clean_sys==1:
        original_tweets = clean_tweets(original_tweets)
    elif clean_sys==2:
        original_tweets = clean_tweets(original_tweets,["urls","mentions"])
    
    #~ metric1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    #~ metric2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    #~ metric = [m1*m2 for m1,m2 in zip(metric1,metric2)]
    #~ max_met = max(metric)
    #~ add_field("metric",original_tweets,[1+(met/max_met) for met in metric])
    
    clear_file("summary_results_"+test_number+"/summary_flagged.001")
    clear_file("summary_results_"+test_number+"/summary_flagged.002")
    clear_file("summary_rouge_results_"+test_number+"/results.txt")
    
    flag_key={0:"Contadores",1:"Contadores binarios",2:"Contadores ngramas",3:"TF-IDF (Defecto)",4:"TF normalizado l1",5:"TF normalizado l2",6:"TF-IDF",7:"TF-IDF con idf suavizado",8:"TF-IDF: idf suav. y norm. l1"}
    
    print("<table border=1><tr style=\"background-color:#AAAAAA\" align=\"center\"><td>Sistema empleado</td><td>Total score</td><td>Number of suc. tweets</td><td>Avg. RT count</td><td>Avg. Fav count</td><td>Avg. Followers</td></tr>")
    summary_tweets_data = ""
    for i in range(9):
        mrt=10
        summary = ts.summarize(tweets=original_tweets,flag=i,remove_stop=stop,use_retweets=rt,use_cross=cr,MAX_RES_TWEETS = mrt)
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.001")
        store_tweets(summary,"summary_results_"+test_number+"/summary_flagged.002")
        
        #~ store_tweets(summary,"summary_results_"+test_number+"/summary_culete"+str(i))
        
        rouge_test(test_number)
        
        total_score=0
        tweets_in_summary=0
        avg_retweets=0
        avg_favorites=0
        avg_followers=0
        for tweet in summary:
            total_score+=tweet["score"]
            avg_retweets+=tweet["retweet_count"]
            avg_favorites+=tweet["favorite_count"]
            avg_followers+=tweet["followers"]
            if tweet["score"]>=5:
                tweets_in_summary+=1
        
        
        
        print("<tr align=\"center\"><td style=\"background-color:#AAAAAA\">",flag_key[i],"</td><td>",total_score,"</td><td>",tweets_in_summary,"</td><td>",avg_retweets/mrt,"</td><td>",avg_favorites/mrt,"</td><td>",avg_followers/mrt,"</td></tr>")
        
        if verbose:
            summary_tweets_data+="<h4>"+flag_key[i]+"</h4> "
            for tweet in summary:
                summary_tweets_data +=  "Score: "+str(tweet["score"])+ \
                                        "\t||\t RT: "+str(tweet["retweet_count"])+ \
                                        "\t||\t Fav: "+str(tweet["favorite_count"])+ \
                                        "\t||\t Fol: "+str(tweet["followers"])+ \
                                        "\t||\t Id: "+tweet["id"]+ \
                                        "\t||\t Text: "+tweet["text"][:50]+"<br />"
    print("</table><br />")
    
    process_rouge_output(test_number)
    if verbose:
        print("<br />"+summary_tweets_data)
        
def load_popular_raw():
    raw_popular = load_obj("raw_popular_tweets")
    
    modeled_popular=[]
    for tweet in raw_popular:
        modeled_popular.append(gt.extract_tweet_info(tweet))

    return modeled_popular
    
def load_modeled_mixed():
    modeled_mixed_tweets = load_obj("modeled_mixed_scored_tweets")

    return modeled_mixed_tweets

def test_metrics():
    original_tweets = load_modeled_mixed()
    
    metric_1_1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    metric_1_2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    metric_1 = [math.log(max(m1*m2,1)) for m1,m2 in zip(metric_1_1,metric_1_2)]
    max_met_1 = max(metric_1)
    add_field("metric1",original_tweets,[met for met in metric_1])
    
    metric_2_1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    metric_2_2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    metric_2 = [math.sqrt(m1*m2) for m1,m2 in zip(metric_2_1,metric_2_2)]
    max_met_2 = max(metric_2)
    add_field("metric2",original_tweets,[met for met in metric_2])
    
    metric_3_1 = [math.log(max((tweet["followers"]**2)/(tweet["friends"]+1),1)) for tweet in original_tweets]
    metric_3_2 = [math.log(max((tweet["retweet_count"]*1.5+tweet["favorite_count"])/(math.log(max(tweet["followers"],1))+1),1)) for tweet in original_tweets]
    metric_3 = [m1*m2 for m1,m2 in zip(metric_3_1,metric_3_2)]
    max_met_3 = max(metric_3)
    add_field("metric3",original_tweets,[met for met in metric_3])
    #~ 
    #~ print([1+(met/max_met) for met in metric])
    
    modeled_tweets = sorted(original_tweets, key=lambda k : k["metric1"])
     #~ #DRAWS A GRAPHIC COMPARING METRICS
    colors=["#00FF00","#FF0000","#33AAAA","#AAAA33","#AA33AA","#33AA33","#FF66FF"]
    labels=["Retuits","Favoritos","Seguidores","Amigos","Metrica_1","Metrica_2","Metrica_3"]
    retweets = [tweet["retweet_count"] for tweet in modeled_tweets]
    favorites = [tweet["favorite_count"] for tweet in modeled_tweets]
    followers = [tweet["followers"] for tweet in modeled_tweets]
    friends = [tweet["friends"] for tweet in modeled_tweets]
    metric_1 = [tweet["metric1"] for tweet in modeled_tweets]
    metric_2 = [tweet["metric2"] for tweet in modeled_tweets]
    metric_3 = [tweet["metric3"] for tweet in modeled_tweets]
    #~ for tweet in modeled_tweets:
        #~ print(tweet["retweet_count"]/(tweet["followers"]+1))
    max_rt = max(retweets)
    max_fav = max(favorites)
    max_fol = max(followers)
    max_fri = max(friends)
    #~ max_met_1 = max(metric_1)
    #~ max_met_2 = max(metric_2)
    #~ max_met_3 = max(metric_3)
    #~ print(max_met)
    gg.draw_things([[rt*30/max_rt for rt in retweets][800:],
                    [fav*30/max_fav for fav in favorites][800:],
                    [fol*30/max_fol for fol in followers][800:],
                    [fri*30/max_fri for fri in friends][800:],
                    [met*50/max_met_1 for met in metric_1][800:],
                    [met*50/max_met_2 for met in metric_2][800:],
                    [met*50/max_met_3 for met in metric_3][800:]],colors,labels,"Comparativa métricas de popularidad","A_metric_test")

def compare_metrics():
    # Con 07
    #~ mat1 = np.array([[32 , 3 , 563.7],[28 , 2 , 565.2],[31 , 1 , 535.2],[32 , 3 , 509.5],[33 , 3 , 440.4],[36 , 3 , 564.7],[33 , 2 , 539.0],[36 , 3 , 564.7],[35 , 4 , 348.1]]).transpose()
    #~ mat2 = np.array([[27 , 2 , 496.3],[30 , 2 , 525.2],[28 , 2 , 330.4],[29 , 3 , 381.4],[36 , 4 , 244.7],[35 , 4 , 365.1],[30 , 2 , 405.4],[30 , 2 , 437.0],[39 , 5 , 220.2]]).transpose()
    #~ mat5 = np.array([[34 , 2 , 587.5],[32 , 2 , 575.2],[31 , 1 , 560.2],[33 , 2 , 583.1],[32 , 2 , 575.2],[36 , 3 , 564.7],[33 , 2 , 684.5],[33 , 2 , 684.5],[38 , 3 , 543.3]]).transpose()
    mat6 = np.array([[32 , 3 , 563.7],[28 , 2 , 565.2],[31 , 1 , 535.2],[29 , 2 , 567.5],[33 , 3 , 440.4],[36 , 3 , 564.7],[32 , 2 , 544.4],[36 , 3 , 564.7],[35 , 4 , 341.0]]).transpose()
    mat3 = np.array([[32,3,563],[28,2,565],[30,1,511],[29,2,567],[35,3,535],[36,3,564],[36,3,564],[36,3,564],[35,4,351]]).transpose()
    #~ mat4 = np.array([[32,3,563],[26,1,552],[32,2,487],[32,3,487],[33,3,423],[35,3,535],[33,2,539],[31,2,555],[39,5,220]]).transpose()
    
    #Con 05
    #~ mat1 = np.array([[29,3,403.2],[28,2,489.2],[19,0,481.5],[36,3,564.7],[34,3,533.4],[30,3,459.7],[31,1,553.6],[27,1,554.4],[36,4,427.8]]).transpose()
    #~ mat2 = np.array([[33,4,373.6],[32,3,459.6],[22,0,446.1],[38,5,380.0],[35,4,425.6],[38,5,367.6],[28,1,494.0],[26,1,468.2],[36,5,271.2]]).transpose()
    #~ mat5 = np.array([[36,3,564.7],[32,2,575.2],[32,2,626.6],[33,2,583.1],[31,2,579.3],[32,2,575.2],[32,2,575.7],[33,2,612.9],[36,3,564.7]]).transpose()
    #~ mat6 = np.array([[28,2,565.2],[31,2,543.4],[19,0,481.5],[36,3,564.7],[34,3,533.4],[30,3,459.7],[32,2,575.7],[27,1,554.4],[36,4,427.8]]).transpose()
    #~ mat3 = np.array([[29,2,567.5],[36,3,564.7],[24,1,551.1],[36,3,564.7],[29,2,567.5],[29,2,567.5],[32,2,575.7],[32,2,575.7],[32,3,457.4]]).transpose()
    #~ mat4 = np.array([[29,3,403.2],[32,3,487.7],[21,0,448.5],[36,3,564.7],[34,3,533.4],[35,4,425.6],[31,1,553.6],[29,1,520.5],[37,4,421.9]]).transpose()
    
    #~ mat1**=2
    #~ mat2**=2
    #~ mat3**=2
    #~ mat4**=2
    #~ mat5**=2
    #~ mat6**=2
    #~ 
    #~ colors=["#00FF00","#FF0000","#33AA33","#AA33AA","#33AAAA","#AAAA33"]
    #~ labels=["A","B","C","D","E","F"]
    #~ gg.draw_things([mat1[0],mat2[0],mat3[0],mat4[0],mat5[0],mat6[0]],colors,labels,"Puntuación total","A_total_score_4")
    #~ gg.draw_things([mat1[1],mat2[1],mat3[1],mat4[1],mat5[1],mat6[1]],colors,labels,"Número de tuits >=5","A_suc_twe_4")
    #~ gg.draw_things([mat1[2],mat2[2],mat3[2],mat4[2],mat5[2],mat6[2]],colors,labels,"Media de Retweets","A_avg_ret_4")
    #~ 
    colors=["#33AA33","#AAAA33"]
    labels=["C","F"]
    gg.draw_things([mat3[0],mat6[0]],colors,labels,"Puntuación total","D_total_score")
    gg.draw_things([mat3[1],mat6[1]],colors,labels,"Número de tuits >=5","D_suc_twe")
    gg.draw_things([mat3[2],mat6[2]],colors,labels,"Media de Retweets","D_avg_ret")
    
    print("Mat.\tScore\tN_Tuits\tAvg. RT")
    print("------------------------------------")
    cosa=np.average(mat3,axis=1)
    print(" 3 \t",cosa[0],"\t",cosa[1],"\t",cosa[2])
    cosa=np.average(mat4,axis=1)
    print(" 3 \t",cosa[0],"\t",cosa[1],"\t",cosa[2])
    #~ 
    print("\multirow{2}{SIST. EMPLEADO} & \multicolumn{6}{|c|}{Puntuación} & \multicolumn{6}{|c|}{Nº tuits > 6} & \multicolumn{6}{|c|}{Media RT} \\\\ \hline" )
    print(" A & B & C & D & E & F & A & B & C & D & E & F & A & B & C & D & E & F & \\\\ \hline")
    mat1 = mat1.transpose()
    mat2 = mat2.transpose()
    mat3 = mat3.transpose()
    mat4 = mat4.transpose()
    mat5 = mat5.transpose()
    mat6 = mat6.transpose()
    flag=["Cont.","C. binarios","C. ngramas","TF-IDF: idf s. y 'l2'","TF norm. 'l1'","TF norm. 'l2'","TF-IDF","TF-IDF: idf suav.","TF-IDF: idf s. y 'l1'"]
    for fila in range(9):
        print(flag[fila])
        for col in range(3):
            print(" & "+str(mat1[fila][col])+" & "+str(mat2[fila][col])+" & "+str(mat3[fila][col])+" & "+str(mat4[fila][col])+" & "+str(mat5[fila][col])+" & "+str(mat6[fila][col]))
        print("\\\\ \hline\n")

def popular_features():
    original_tweets = load_popular_raw()
    modeled_tweets = sorted(original_tweets, key=lambda k : k["followers"])
    colors=["#00FF00","#FF0000","#33AAAA","#AAAA33"]
    labels=["Retuits","Favoritos","Seguidores","Amigos"]
    retweets = [tweet["retweet_count"] for tweet in modeled_tweets]
    favorites = [tweet["favorite_count"] for tweet in modeled_tweets]
    followers = [tweet["followers"] for tweet in modeled_tweets]
    friends = [tweet["friends"] for tweet in modeled_tweets]
    max_rt = max(retweets)
    max_fav = max(favorites)
    max_fol = max(followers)
    max_fri = max(friends)
    gg.draw_things([[rt*30/max_rt for rt in retweets],
                    [fav*30/max_fav for fav in favorites],
                    [fol*30/max_fol for fol in followers],
                    [fri*30/max_fri for fri in friends]],colors,labels,"Características Tweets populares","A_popular_features")
    
def compare_methods():
    all_mats=[np.array([[0.18227,0.37271,0.11675,0.11879,32,3,509.5,272.0,726940.2],[0.18227,0.37271,0.11675,0.11896,32,3,509.5,272.0,726940.2],[0.19295,0.37563,0.12008,0.12173,30,2,496.4,272.0,726829.5],[0.16185,0.37469,0.11315,0.12019,31,3,512.8,275.1,259697.7],[0.16262,0.36197,0.11152,0.11268,30,3,511.8,271.7,296224.9],[0.16262,0.36197,0.11152,0.11303,30,3,511.8,271.7,296224.9],[0.17957,0.38361,0.11881,0.12646,33,3,510.5,275.4,690413.0],[0.18227,0.37271,0.11675,0.11877,32,3,509.5,272.0,726940.2],[0.18651,0.37283,0.11681,0.11877,36,3,573.2,288.5,1074767.2]]).transpose(),np.array([[0.20356,0.39494,0.12743,0.13023,30,1,521.0,292.4,1056878.7],[0.19831,0.38280,0.12174,0.12298,36,3,564.7,288.5,1075519.8],[0.20270,0.40000,0.12591,0.13176,32,2,504.8,268.9,710369.9],[0.16582,0.36868,0.11277,0.11680,34,3,567.0,288.2,644804.5],[0.19780,0.38183,0.12136,0.12477,35,3,535.6,249.3,1103172.1],[0.16737,0.35854,0.11072,0.10909,29,2,567.5,293.6,675494.3],[0.16709,0.38119,0.11481,0.12147,29,1,562.8,290.5,658924.0],[0.19831,0.38280,0.12174,0.12328,36,3,564.7,288.5,1075519.8],[0.19780,0.38183,0.12136,0.12456,35,3,535.6,249.3,1103172.1]]).transpose(),np.array([[0.15331,0.31512,0.09622,0.07984,32,3,509.5,272.0,726940.2],[0.15331,0.31512,0.09622,0.07991,32,3,509.5,272.0,726940.2],[0.15797,0.31741,0.09807,0.08174,30,2,496.4,272.0,726829.5],[0.13639,0.31878,0.09376,0.08151,31,3,512.8,275.1,259697.7],[0.13672,0.30597,0.09169,0.07587,30,3,511.8,271.7,296224.9],[0.13672,0.30597,0.09169,0.07587,30,3,511.8,271.7,296224.9],[0.15139,0.32780,0.09827,0.08568,33,3,510.5,275.4,690413.0],[0.15331,0.31512,0.09622,0.07962,32,3,509.5,272.0,726940.2],[0.15277,0.31682,0.09668,0.07965,36,3,573.2,288.5,1074767.2]]).transpose(),np.array([[0.13838,0.30540,0.09161,0.07429,29,2,567.5,293.6,675494.3],[0.16442,0.32462,0.10021,0.08398,36,3,564.7,288.5,1075519.8],[0.14194,0.31520,0.09502,0.07945,24,1,551.1,298.8,267056.1],[0.16442,0.32462,0.10021,0.08361,36,3,564.7,288.5,1075519.8],[0.13838,0.30540,0.09161,0.07490,29,2,567.5,293.6,675494.3],[0.13838,0.30540,0.09161,0.07466,29,2,567.5,293.6,675494.3],[0.14164,0.31735,0.09468,0.08029,32,2,575.7,297.1,640269.8],[0.14164,0.31735,0.09468,0.08050,32,2,575.7,297.1,640269.8],[0.16595,0.31623,0.09884,0.07951,32,3,457.4,280.6,1112460.7]]).transpose(),np.array([[0.16388,0.36772,0.11292,0.11418,26,2,513.3,280.5,290387.5],[0.18227,0.37271,0.11675,0.11842,32,3,509.5,272.0,726940.2],[0.18451,0.38852,0.12564,0.12988,35,2,506.6,268.5,717466.1],[0.18755,0.37159,0.11677,0.11833,33,3,530.2,284.0,1100494.8],[0.18002,0.37963,0.11903,0.12567,37,4,509.0,266.6,696250.4],[0.18227,0.37271,0.11675,0.11917,32,3,509.5,272.0,726940.2],[0.17972,0.38393,0.12004,0.12296,35,2,620.8,322.3,819965.7],[0.18031,0.37696,0.11775,0.12122,36,3,626.5,328.8,800008.8],[0.16903,0.36137,0.11381,0.11357,30,1,559.1,291.6,663066.6]]).transpose(),np.array([[0.16766,0.36256,0.11122,0.11101,32,3,563.7,288.1,668851.1],[0.16723,0.36673,0.11259,0.11205,28,2,565.2,296.9,663013.7],[0.20050,0.39899,0.12819,0.13343,30,1,511.7,290.7,679114.1],[0.16737,0.35854,0.11072,0.10904,29,2,567.5,293.6,675494.3],[0.19780,0.38183,0.12136,0.12498,35,3,535.6,249.3,1103172.1],[0.19831,0.38280,0.12174,0.12372,36,3,564.7,288.5,1075519.8],[0.19831,0.38280,0.12174,0.12291,36,3,564.7,288.5,1075519.8],[0.19831,0.38280,0.12174,0.12311,36,3,564.7,288.5,1075519.8],[0.20855,0.38605,0.12460,0.12691,35,4,351.3,178.9,928399.1]]).transpose(),np.array([[0.13783,0.31092,0.09296,0.07687,26,2,513.3,280.5,290387.5],[0.15331,0.31512,0.09622,0.07966,32,3,509.5,272.0,726940.2],[0.15973,0.33057,0.10228,0.08890,35,2,506.6,268.5,717466.1],[0.15374,0.31454,0.09625,0.07933,33,3,530.2,284.0,1100494.8],[0.15171,0.32294,0.09822,0.08495,37,4,509.0,266.6,696250.4],[0.15331,0.31512,0.09622,0.07982,32,3,509.5,272.0,726940.2],[0.15342,0.31114,0.09605,0.07821,31,2,605.2,325.3,835122.6],[0.15192,0.31922,0.09728,0.08182,36,3,626.5,328.8,800008.8],[0.14216,0.30554,0.09322,0.07614,30,1,559.1,291.6,663066.6]]).transpose(),np.array([[0.13838,0.30540,0.09161,0.07458,29,2,567.5,293.6,675494.3],[0.16442,0.33027,0.10178,0.08632,32,2,544.4,288.4,1074106.4],[0.16315,0.33753,0.10249,0.08955,32,2,555.7,287.2,687149.2],[0.13750,0.31192,0.09277,0.07746,30,2,570.5,294.5,674589.6],[0.16442,0.32462,0.10021,0.08413,36,3,564.7,288.5,1075519.8],[0.16442,0.32462,0.10021,0.08426,36,3,564.7,288.5,1075519.8],[0.14164,0.31735,0.09468,0.08046,32,2,575.7,297.1,640269.8],[0.14204,0.31824,0.09553,0.08246,30,1,581.2,300.9,643721.5],[0.16396,0.32934,0.10048,0.08611,35,3,475.3,183.3,890908.3]]).transpose()]
    
    print("Mat.\tRouge-L\tScore\tN_Tuits\t\tAvg. RT\t\tAvg. Fav\tAvg. Folow")
    print("------------------------------------------------------------------------")
    cosas=[]
    for i in range(8):
        cosa=np.around(np.average(all_mats[i],axis=1),decimals=2)
        print(" "+str(i+2)+" \t",cosa[1],"\t",cosa[4],"\t",cosa[5],"\t\t",cosa[6],"\t",cosa[7]," \t",cosa[8])
        cosas.append(cosa[[1,4,5,6,7,8]].tolist())
    
    colors=["#FE2E2E","#FE9A2E","#F7FE2E","#64FE2E","#2EFEF7","#0000FF"]
    labels=["ROUGE-L","Puntuación","Nº Tuits>=5","Media RT","Media Fav","Media Fol"]
    cosas = np.array(cosas).transpose()
    max_cosas = np.max(cosas,axis=1)
    cosas*=50
    for i in range(6):
        cosas[i]/=max_cosas[i]
    gg.draw_things(cosas,colors,labels,"Medias","TOTAL_average")
    
    all_colors=["#FE2E2E","#FE9A2E","#F7FE2E","#64FE2E","#2EFEF7","#0000FF","#BF00FF","#F781F3"]
    all_labels=["02","03","04","05","06","07","08","09"]
    
    indices = range(8)
    #~ indices = [4,5,6,7]
    #~ indices = [0,1,2,3]
    #~ indices = [5,7]
    
    colors=[all_colors[ind] for ind in indices]
    labels=[all_labels[ind] for ind in indices]
    mats=[all_mats[ind] for ind in indices]
    
    gg.draw_things([mat[1] for mat in mats],colors,labels,"ROUGE-L","TOTAL_rougel")
    gg.draw_things([mat[4] for mat in mats],colors,labels,"Puntuación total","TOTAL_score")
    gg.draw_things([mat[5] for mat in mats],colors,labels,"Nº de tuits >=5","TOTAL_succesful")
    gg.draw_things([mat[6] for mat in mats],colors,labels,"Media de retuits","TOTAL_retweets")
    gg.draw_things([mat[7] for mat in mats],colors,labels,"Media de favoritos","TOTAL_favorite")
    gg.draw_things([mat[8] for mat in mats],colors,labels,"Media de seguidores","TOTAL_follower")
    
    

if __name__ == "__main__":
    
    print(gt.transform_links_regex("esto es @pedro un tuit con #hash @enrique y también #tags y alguna http://www.url.com"))
    
    if False:
        test_number = sys.argv[1]
        print("<meta http-equiv=\"Content-type\" content=\"text/html;charset=ISO-8859-1\">")
        print("<h1>Test #"+test_number+"</h1>")
        #TWEETS TAL CUAL #2 - #9 (Cross y sin)
        comment={   "02":"Esta primera prueba con el nuevo corpus puntuado consiste en un resumen realizado simplemente considerando los tweets con score >6 sin ninguna entidad (urls, menciones o hashtags) y habiendo eliminado manualmente los repetidos. El conjunto de tweets es el original, del que se han eliminado los que eran RT y se han anyadido los originales de los mismos.",
                    "03":"La segunda prueba es igual que la anterior pero en este caso limpiamos los tweets antes de realizar el resumen.",
                    "04":"Es igual que el primero, pero utilizando en el model de resumen los tweets con hashtags, y los tweets sin limpieza alguna",
                    "05":"Es igual que el segundo, pero utilizando en el modelo de resumen los tweets con hashtags y al limpiar, dejando los hashtags",
                    "06":"Es igual que el primero, pero eliminando stopwords",
                    "07":"Es igual que el segundo, pero eliminando stopwords",
                    "08":"Es igual que el tercero, pero eliminando stopwords",
                    "09":"Es igual que el cuarto, pero eliminando stopwords"}

        #~ print("<br /> sin el logaritmo, con normalización, con 1'  ")
        print("<br /> "+comment[test_number[:2]])
        
        limpieza={  "02":0,
                    "03":1,
                    "04":0,
                    "05":2,
                    "06":0,
                    "07":1,
                    "08":0,
                    "09":2}
        stopWords={ "02":False,
                    "03":False,
                    "04":False,
                    "05":False,
                    "06":True,
                    "07":True,
                    "08":True,
                    "09":True}          
        
        cross=False
        retweets=False
        if len(sys.argv[1])>3 and sys.argv[1][3]=="C":
            cross=True
        elif len(sys.argv[1])>4 and sys.argv[1][3:5]=="RT":
            retweets=True
            cross=True
        
        #~ print("limpieza: ",limpieza[test_number[:2]],"\nstop: ",stopWords[test_number[:2]],"\nrt: ",retweets,"\ncr: ",cross)
        
        launch_test(test_number,limpieza[test_number[:2]],retweets,cross,stopWords[test_number[:2]],True)
