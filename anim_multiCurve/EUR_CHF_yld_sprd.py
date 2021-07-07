# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 15:36:18 2021

@author: giro
"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc, cm, colors
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import datetime 

# load data
my_data = pd.read_csv('EUR_IG_Curve_Comb.csv').sort_index()

# auxiliary function
def end_of_month(dt):
    todays_month = dt.month
    tomorrows_month = (dt + datetime.timedelta(days=1)).month
    return True if tomorrows_month != todays_month else False

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

date    = pd.to_datetime(my_data['Date']-719529,unit='d')
isMonthend = [end_of_month(x) for x in date]
df      = my_data.loc[isMonthend,'BVCSBC01':'BVCSBC15']
df_gov      = my_data.loc[isMonthend,'BVCSEB01':'BVCSEB15']
eoms  = date[isMonthend]
idx     = [x for x in range(1,16)]  
x_axis  = pd.DataFrame(idx)
x_subset = [1,2,3,5,7,8,10,14]
N       = df.shape[0]
df.index = [x for x in range(N)]

# create colour map
#cmap = colors.LinearSegmentedColormap.from_list("", ["#348939","#FDBF02","#FE7E03","#9B1D1E"])
cmap = colors.LinearSegmentedColormap.from_list("", ["#e8e8e8","#033500"])
                                                     
                                                     
# fill up with nans
df2 = pd.DataFrame(np.nan, index=df.index, columns=["BVCSBC%02d" % x for x in range(1,16)])
df2.loc[:,df.columns] = df

df2_gov = pd.DataFrame(np.nan, index=df_gov.index, columns=["BVCSEB%02d" % x for x in range(1,16)])
df2_gov.loc[:,df_gov.columns] = df_gov

# define plot
plt.style.use('seaborn-whitegrid')

#plt.style.use('dark_background')
fig, axs = plt.subplots(3, 1,figsize=(12, 6),gridspec_kw={'height_ratios': [1,1, 0.2]})


axs[0].set_xlim((1,15))
axs[1].set_xlim((1,15))
axs[2].set_xlim((1,15))
axs[0].set_ylim((-1,6))
axs[1].set_ylim((0,2.5))
axs[2].set_ylim((-0.5,0.5))

axs[2].grid(False)
axs[2].axis('off')
axs[2].get_xaxis().set_visible(False)
axs[2].get_yaxis().set_visible(False)
axs[1].set_xlabel("Yr",multialignment="right")

axs[0].set_ylabel("% Rendite")
axs[1].set_ylabel("% Spread")
axs[0].set_title("EURO Credit Spread: BBB vs Gov")
# predfine elements 
linesUp = [axs[0].plot([], [],color="dimgray")[0] for _ in range(0,2)]
linesDn = [axs[1].plot([], [],color="dimgray")[0] for _ in range(0,N)]

linesT = [axs[2].plot([], [],color="dimgray")[0] for _ in range(2)]

dtText = axs[2].text(0.5, -0.25, 'A',
        verticalalignment='bottom', horizontalalignment='center',
        transform=axs[2].transAxes,
        color="dimgray", fontsize=15)

tmp = axs[2].text(0.99, -0.25, '2021',
        verticalalignment='bottom', horizontalalignment='right',
        transform=axs[2].transAxes,
        color="dimgray", fontsize=15)

tmp2 = axs[2].text(0.01, -0.25, '2012',
        verticalalignment='bottom', horizontalalignment='left',
        transform=axs[2].transAxes,
        color="dimgray", fontsize=15)

#tmp = axs[2].text(0.0, -0.05, 'A',
#        verticalalignment='bottom', horizontalalignment='left',
#        transform=axs[0].transAxes,
#        color="dimgray", fontsize=15)

#linesDn[0].set_height(np.random.random_sample(15).tolist()+5)
linesT[0].set_data(x_axis, np.zeros(15))
linesT[1].set_data([1], [0])

linesT[1].set_marker("o")
lst = []

def animate(i):
    
    if not i >= N:
        # get data
        ser = df2.iloc[i,:]
        ser.index = idx
        ser = ser.interpolate(method='cubic',order=2)
        
        ser_gov = df2_gov.iloc[i,:]
        ser_gov.index = idx
        ser_gov = ser_gov.interpolate(method='cubic',order=2)
        
        dtText.set_text(eoms.iloc[i].strftime('%b %Y'))
        
        linesT[1].set_data([(i+1)/(N)*15], [0])
        
        creditSpread =  ser - ser_gov
        lst.append(creditSpread.mean())
        ## --- update top graph ---
        # add data
        linesUp[0].set_data(x_axis, ser)
        linesUp[1].set_data(x_axis, ser + creditSpread)
        # marker add
        linesUp[0].set_marker("o")
        linesUp[0].set_markevery(x_subset)
        linesUp[1].set_marker("o")
        linesUp[1].set_markevery(x_subset)
        
        ## --- update bottom graph ---
        # add data
        linesDn[i].set_data(x_axis, creditSpread)
        linesDn[i].set_color("dimgray")
        # make history
        if i > 0:
            #linesDn[i-1].set_color(cmap((creditSpread.mean()-0.69)/1.37))
            linesDn[i-1].set_color(cmap((i+1)/N))
            linesDn[i-1].set_linewidth(0.5)
            linesDn[i-1].set_marker("")
    
#    
#    for num in range(len(x_subset)):
#        linesUp[0].set_text("%.2f" % ser[x_subset[num]+1])
#        linesUp[0].set_position((x_subset[num]+1,ser[x_subset[num]+1]+0.25))
#        linesUp[1].set_text("%.2f" % ser[x_subset[num]+1])
#        linesUp[1].set_position((x_subset[num]+1,ser[x_subset[num]+1]+0.25))
    # https://stackoverflow.com/questions/20624408/matplotlib-animating-multiple-lines-and-text
    #for num,aaa in enumerate(linesDn[0].get_children()):
        #print(aaa.get_height())
    
    return tuple(linesUp) + tuple(linesDn)  + tuple(linesT)

anim = animation.FuncAnimation(fig, animate, 
           frames=N+30, interval=170, repeat=False ,blit=True)
#anim.show()
#
anim.save('multicurve.gif',writer="pillow")
