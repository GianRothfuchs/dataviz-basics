import matplotlib as mpl 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc, cm, colors
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import datetime 


rc('animation', html='html5')
mpl.rcParams['animation.ffmpeg_path'] = r'C:\\FFmpeg\\bin\\ffmpeg.exe'

def end_of_month(dt):
    todays_month = dt.month
    tomorrows_month = (dt + datetime.timedelta(days=1)).month
    return True if tomorrows_month != todays_month else False

# load data
my_data = pd.read_csv('EUR_IG_Curve.csv').sort_index()

date    = pd.to_datetime(my_data['Date']-719529,unit='d')
isMonthend = [end_of_month(x) for x in date]
df      = my_data.loc[isMonthend,'IGEEVC01':]
eoms  = date[isMonthend]
idx     = [x for x in range(1,16)]  
x_axis  = pd.DataFrame(idx)
x_subset = [1,2,3,5,7,8,10,14]
N       = df.shape[0]
df.index = [x for x in range(N)]

# create colour map
cmap = colors.LinearSegmentedColormap.from_list("", ["#348939","#FDBF02","#FE7E03","#9B1D1E"])

# fill up with nans
df2 = pd.DataFrame(np.nan, index=df.index, columns=["IGEEVC%02d" % x for x in range(1,16)])
df2.loc[:,df.columns] = df


# define plot
plt.style.use('seaborn-whitegrid')
#plt.style.use('dark_background')
fig = plt.figure()

plt.rcParams["figure.figsize"] = (8,6)

ax = plt.axes(xlim=(1,16), ylim=(-1,6))
plt.xlabel("Tenor")
plt.ylabel("%")
plt.title("Yield Curve: EUR Credit A+, A, A-")
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')


lines = [ax.text(0, 0, '', fontsize=9, horizontalalignment='center') for _ in range(len(x_subset))]
lines.extend([plt.plot([], [])[0] for _ in range(0,N+1)])

dtText = ax.text(0.05, 0.90, '',
        verticalalignment='bottom', horizontalalignment='left',
        transform=ax.transAxes,
        color="dimgray", fontsize=15)


def animate(i):

    offset = len(x_subset)   
    
    # get data
    ser = df2.iloc[i,:]
    ser.index = idx
    ser = ser.interpolate(method='cubic',order=2)
    dtText.set_text(eoms.iloc[i].strftime('%b %Y'))
    #print(i)
    if i+1 % 10 == 0:
        print("%4d/%4d" % (i,N))
        
    # update lines    
    lines[i+offset+1].set_data(x_axis, ser)
    lines[i+offset+1].set_color("dimgray")
    # marker add
    lines[i+offset+1].set_marker("o")
    lines[i+offset+1].set_markevery(x_subset)
    
    for num in range(len(x_subset)):
#         print(num)
#        print(lines[num])
        lines[num].set_text("%.2f" % ser[x_subset[num]+1])
        lines[num].set_position((x_subset[num]+1,ser[x_subset[num]+1]+0.25))

    if i > 0:
        lines[i+offset].set_color(cmap(ser.mean()/4.5))
        lines[i+offset].set_linewidth(0.5)
        lines[i+offset].set_marker("")
    
    return lines
#"#42ae48" , "#fdbf02","#fe7e03","#9b1d1e"

anim = animation.FuncAnimation(fig, animate, 
           frames=N, interval=170, repeat=False ,blit=True)

anim.save('euro_curve_corp_A_sm.gif',writer="pillow")