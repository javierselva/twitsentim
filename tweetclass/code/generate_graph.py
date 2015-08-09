#~ from matplotlib import pylab
#~ from pylab import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import matplotlib.dates as mdates
import datetime

import matplotlib.ticker as ticker

#~ from ..models import Query

#~ try:
    #~ from StringIO import StringIO
#~ except ImportError:
    #~ from io import StringIO

def draw_things(things,colors,labels,text):
    fig = Figure()
    fig.set_figwidth(30)
    canvas = FigureCanvas(fig)
    
    ax = fig.add_subplot(1,1,1, axisbg='white')
    ax.set_ylabel('Value')
    ax.set_xlabel('Tweets')
    ax.set_title(text)
    
    N = len(things[0])
    ind = np.arange(N)
    
    cont=0
    
    for t in range(len(things)):
        ax.plot(ind,things[t],colors[cont],label=labels[t],linewidth=1.3)
        cont+=1
    ax.legend()
    
    canvas.print_figure(text+'.png',facecolor='white',bbox_inches='tight')

def general_graph(polarity,name):
    
    #~ fig = plt.figure()
    fig = Figure()
    #~ rect = fig.patch
    #~ rect.set_facecolor('white')
    fig.set_figwidth(12)
    
    legend=["P+",     "P",      "NEU",    "N",      "N+",     "NONE"]
    colors=["#A7DB40","#D8E067","#FFB81F","#FF743D","#C4213D","#707070"]
    
    canvas = FigureCanvas(fig)
    
    ax = fig.add_subplot(1,1,1, axisbg='white')
    ax.set_ylabel('Polarity value')
    ax.set_xlabel('Date')
    ax.set_title('Polarity evolution for the query: '+ name)
    
    N = len(polarity[6])
    ind = np.arange(N)
    
    # This is used in order to skip the dates where there is no information
    def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
        return polarity[6][thisind].strftime('%h,%d %Hh.')
    
    #~ years = mdates.YearLocator()
    #~ months = mdates.MonthLocator()
    #~ days = mdates.DayLocator()
    #~ hours = mdates.HourLocator()
    #~ minutes = mdates.MinuteLocator()
    #~ 
    #~ ax.xaxis.set_major_locator(days)
    #~ ax.xaxis.set_minor_locator(hours)
    #~ 
    #~ datemin = datetime.date(min(polarity[6]).year, min(polarity[6]).month, min(polarity[6]).day)
    #~ datemax = datetime.date(max(polarity[6]).year, max(polarity[6]).month, max(polarity[6]).day)
    #~ ax.set_xlim(datemin, datemax)
    
    #~ print(min(polarity[6]).day)
    
    #~ ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    #~ if len(polarity[0])>20:
        #~ ax.set_aspect(len(polarity[0])/20)
    
    ax.autoscale(tight=True)
    ax.grid(True)
    
    i=0
    while i < 6: 
        ax.plot(ind,polarity[i],colors[i],label=legend[i],linewidth=3)
        i+=1
    ax.legend()
    #~ plt.grid(True)
    
    #~ plt.show()
    
    # As indices ar being used instead of dates, each index is to be
    # asociated with the correspondig date using the funcion defined
    # above
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    canvas.print_figure('tweetclass/static/tweetclass/histogram_generic_'+name+'.png',facecolor="#EBE8E9",bbox_inches='tight')
#~ graph([[1,2,3,4,5,6],[3,4,5,6,7,8],[5,6,7,8,9,10],[7,8,9,10,11,12],[9,10,11,12,13,14],[11,12,13,14,15,16],[13,14,15,16,17,18],[1,2,3,4,5,6]],"obama")

def radial_summary(values,name):
    legend=["P+",     "P",      "NEU",    "N",      "N+",     "NONE"]
    colors=["#A7DB40","#D8E067","#FFB81F","#FF743D","#C4213D","#707070"]
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    fig.set_figwidth(1)
    fig.set_figheight(1)
    
    ax = fig.add_subplot(1,1,1)

    ax.pie(values,colors=colors, shadow=True, startangle=90)

    canvas.print_figure('tweetclass/static/tweetclass/summary_pie_'+name+'.png',bbox_inches='tight')

def summary_graph(polarity,name):
    
    fig = Figure()
    fig.set_figwidth(12)
    
    canvas = FigureCanvas(fig)
    
    ax = fig.add_subplot(1,1,1, axisbg='gray')
    ax.set_ylabel('Polarity value')
    ax.set_xlabel('Date')
    ax.set_title('Polarity evolution for the query: '+ name)
    
    N = len(polarity[1])
    ind = np.arange(N)
    
    def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
        return polarity[1][thisind].strftime('%h,%d %Hh.')
    
    ax.autoscale(tight=True)
    ax.grid(True)
    
    ax.plot([min(ind),max(ind)],[50,50],'#000000',linewidth=4)
    ax.plot(ind,polarity[0],"#8888FF",linewidth=3.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    canvas.print_figure('tweetclass/static/tweetclass/histogram_summary_'+name+'.png',facecolor="#EBE8E9",bbox_inches='tight')
