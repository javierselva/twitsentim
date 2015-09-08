'''
@file:      tweetclass/code/generate_graph.py
@author:    Javier Selva Castello
@date:      2015
@desc:      This file contains all the necessary functions to generate the application graphics.
'''
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import matplotlib.dates as mdates
import datetime

import matplotlib.ticker as ticker

'''
@name:      draw_things
@desc:      Generic function to draw a graphic given a set of data
@params:    things  - a list of lists of integers containing the data to be plotted
                      All the lists inside "things" should have the same length.
            colors  - a list of strings representing the color that each thing in things
                      will have on the plot. The colors may be in hexadecimal (#AF33E2) or 
                      follow the matplotlib predefined colors (http://matplotlib.org/api/colors_api.html)
                      The length of this list should be greater or equal to the lenght of "things".
            labels  - a list of strings containing the label for each thing to be plotted.
                      The length of this list should be greater or equal to the lenght of "things".
            text    - a string containing the title of the plotting.
            name    - a string containing the name of the file where the plot will be stored.
                      If the default value is recieved, the file name will be the same as the "text"
@return:    nothing, a ".png" image with the resulting graphic will be saved to disk
'''
def draw_things(things,colors,labels,text,name=""):
    # If "name" is empty, it's setted to the text content without spaces
    if name=="":
        name = text.replace(" ","")
    
    # Create a figure and a canvas to draw in
    fig = Figure()
    fig.set_figwidth(15)
    fig.set_figheight(5)
    canvas = FigureCanvas(fig)
    
    # Set the figure configuration and parameters
    ax = fig.add_subplot(1,1,1, axisbg='white')
    ax.set_ylabel('Value')
    ax.set_xlabel('Tweets')
    ax.set_title(text)
    
    # Set the x axis indices for every plotting
    N = len(things[0])
    ind = np.arange(N) # creates an numpy.array from 0 to N-1
    
    # Formatter for the x axis
    def numeric_ment(x,pos):
        return "#0%d" % (x+1)
    
    formatter = ticker.FuncFormatter(numeric_ment)
    
    # Plot all the things
    for t in range(len(things)):
        ax.plot(ind,things[t],colors[t],label=labels[t],linewidth=1.5)
    
    # Plot the legend in the graphic
    ax.legend()
    # Format the x axis as defined avobe
    ax.xaxis.set_major_formatter(formatter)
    #Save the graphic as an image
    canvas.print_figure(name+'.png',facecolor='white',bbox_inches='tight')


'''
@name:      general_graph
@desc:      Draws the generic graph (a line for each polarity evolution) for a query
@params:    polarity    - a list of lists of integers (length = 6) representing the evolution
                          of each polarity through the different times the query was made
            name        - the name of the query being plotted
@return:    nothing, a ".png" image with the resulting graphic will be saved to disk
'''
def general_graph(polarity,name):
    
    # Create a figure and a canvas to draw in
    fig = Figure()
    fig.set_figwidth(12)
    canvas = FigureCanvas(fig)
    
    # Set the legend and the colors for the plot
    legend=["P+",     "P",      "NEU",    "N",      "N+",     "NONE"]
    colors=["#A7DB40","#D8E067","#FFB81F","#FF743D","#C4213D","#707070"]
    
    # Set the figure configuration and parameters
    ax = fig.add_subplot(1,1,1, axisbg='white')
    ax.set_ylabel('Polarity value')
    ax.set_xlabel('Date')
    ax.set_title('Polarity evolution for the query: '+ name)
    
    # Set the x axis indices for every plotting
    N = len(polarity[6])
    ind = np.arange(N)# creates an numpy.array from 0 to N-1
    
    # This is used in order to skip the dates where there is no information
    def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
        return polarity[6][thisind].strftime('%h,%d %Hh.')
    
    ax.autoscale(tight=True)
    ax.grid(True)
    
    i=0
    # Plot all the polarity evolution lines
    while i < 6: 
        ax.plot(ind,polarity[i],colors[i],label=legend[i],linewidth=3)
        i+=1
    # Plot the legend in the graphic
    ax.legend()
    
    # As indices are being used instead of dates, each index has to be
    # asociated with the correspondig date using the funcion defined
    # above
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    #Save the graphic as an image
    canvas.print_figure('tweetclass/static/tweetclass/histogram_generic_'+name+'.png',facecolor="#EBE8E9",bbox_inches='tight')

'''
@name:      radial_summary
@desc:      Draws a pie graph representing the percentage of each polarity in the total amount 
            of tweets in the generic summary 
@params:    polarity    - a list of integers representing the percentage of each polarity
            name        - the name of the query being plotted
@return:    nothing, a ".png" image with the resulting graphic will be saved to disk
'''
def radial_summary(values,name):
    # Set the colors for the plot
    colors=["#A7DB40","#D8E067","#FFB81F","#FF743D","#C4213D","#707070"]
    
    # Create a figure and a canvas to draw in
    fig = Figure()
    canvas = FigureCanvas(fig)
    fig.set_figwidth(1)
    fig.set_figheight(1)
    
    # Set the figure configuration and parameters
    ax = fig.add_subplot(1,1,1)

    # Plot the pie with the diferent values and colors
    ax.pie(values,colors=colors, shadow=True, startangle=90)
    
    #Save the graphic as an image
    canvas.print_figure('tweetclass/static/tweetclass/summary_pie_'+name+'.png',bbox_inches='tight')

'''
@name:      summary_graph
@desc:      Draws the summary graph (one line representing the summed up polarity) for a query
@params:    polarity    - a list of integers representing the evolution of the summed up polarity
                          of the query through the different times the query was made
            name        - the name of the query being plotted
@return:    nothing, a ".png" image with the resulting graphic will be saved to disk
'''
def summary_graph(polarity,name):
    # Create a figure and a canvas to draw in
    fig = Figure()
    fig.set_figwidth(12)
    canvas = FigureCanvas(fig)
    
    # Set the figure configuration and parameters
    ax = fig.add_subplot(1,1,1, axisbg='gray')
    ax.set_ylabel('Polarity value')
    ax.set_xlabel('Date')
    ax.set_title('Polarity evolution for the query: '+ name)
    
    # Set the x axis indices for every plotting
    N = len(polarity[1])
    ind = np.arange(N)
    
    # This is used in order to skip the dates where there is no information
    def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
        return polarity[1][thisind].strftime('%h,%d %Hh.')
    
    ax.autoscale(tight=True)
    ax.grid(True)
    
    # Plot the polarity evolution line
    ax.plot([min(ind),max(ind)],[50,50],'#000000',linewidth=4) # This draws a horizontal line in y=50
    ax.plot(ind,polarity[0],"#8888FF",linewidth=3.3)
    
    # As indices are being used instead of dates, each index has to be
    # asociated with the correspondig date using the funcion defined
    # above
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    #Save the graphic as an image
    canvas.print_figure('tweetclass/static/tweetclass/histogram_summary_'+name+'.png',facecolor="#EBE8E9",bbox_inches='tight')
