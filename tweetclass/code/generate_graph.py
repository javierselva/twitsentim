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

def draw_rt_vs_score(rt,score):
    fig = Figure()
    fig.set_figwidth(20)
    canvas = FigureCanvas(fig)
    
    ax = fig.add_subplot(1,1,1, axisbg='white')
    ax.set_ylabel('Value')
    ax.set_xlabel('Tweets')
    ax.set_title('Score vs Retweet_count')
    
    N = len(rt)
    ind = np.arange(N)
    
    for s in range(len(rt)):
        rt[s]=(rt[s]*20)/1258
    
    ax.plot(ind,rt,"#00FF00",linewidth=1.3)
    ax.plot(ind,score,"#FF0000",linewidth=1.3)
    
    canvas.print_figure('comparision01.png',facecolor='white',bbox_inches='tight')

def general_graph(polarity,name):
    
    #~ fig = plt.figure()
    fig = Figure()
    #~ rect = fig.patch
    #~ rect.set_facecolor('white')
    fig.set_figwidth(12)
    
    
    colors=["#00FF00","#008800","#888888","#880000","#FF0000","#000000"]
    
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
        ax.plot(ind,polarity[i],colors[i],linewidth=1.3)
        i+=1
    #~ plt.grid(True)
    
    #~ plt.show()
    
    # As indices ar being used instead of dates, each index is to be
    # asociated with the correspondig date using the funcion defined
    # above
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    
    canvas.print_figure('tweetclass/static/tweetclass/histogram_generic_'+name+'.png',facecolor='white',bbox_inches='tight')
#~ graph([[1,2,3,4,5,6],[3,4,5,6,7,8],[5,6,7,8,9,10],[7,8,9,10,11,12],[9,10,11,12,13,14],[11,12,13,14,15,16],[13,14,15,16,17,18],[1,2,3,4,5,6]],"obama")

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
    
    canvas.print_figure('tweetclass/static/tweetclass/histogram_summary_'+name+'.png',facecolor='white',bbox_inches='tight')
