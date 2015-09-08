'''
@file:      tweetclass/graph_data_generator.py
@desc:      The main idea for this file is transforming the raw Query_datas into a list of polarities
            so the plotter (generate_graph) only has to draw it.
@date:      2015
@author:    Javier Selva Castello
'''

from .models import Query, Query_data
from .code import generate_graph

'''
@name:      generate_data
@desc:      This function creates a list of lists of polarity values (floats), and then
            calls the draw function in code/generate_graph.py to plot the graphics
@params:    name        - string containing the query text
            query_list  - a list of Query_datas with all the polarity results for every time the 
                          query "name" was made
@return:    nothing, it will create the graphics calling the plotter
'''
# This method recieves the name of the query and a list of query_data
def generate_data(name,query_list):
    polarity=[[] for i in range(0,7)]
    pol_summary=[]
    
    # polarity[6] will contain the information of the dates
    # polarity[i] for i in [0,5], will contain the information about the polarity at the corresponding date
    # pol_summary will contain a summarized info about the polarity
    for query in query_list:
        polarity[0].append(int(query.p_pos_p))  # P+
        polarity[1].append(int(query.p_pos))    # P
        polarity[2].append(int(query.p_neu))    # NEU
        polarity[3].append(int(query.p_neg))    # N
        polarity[4].append(int(query.p_neg_p))  # N+
        polarity[5].append(int(query.p_none))   # NONE
        
        polarity[6].append(query.query_date)    # Date
        
        # Here, a metric is used in order to measure the polarity in an only mixed up value
        pol_summary.append(50 # Base value
                            + polarity[0][-1]*1.5   # Very positive
                            + polarity[1][-1]       # Positive
                            - polarity[3][-1]       # Negative
                            - polarity[4][-1]*1.5 ) # Very negative
    
    # Call the drawing fucntions
    generate_graph.general_graph(polarity,name)
    generate_graph.summary_graph([pol_summary,polarity[6]],name)
