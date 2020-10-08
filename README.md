# dataviz-basics
My notes on data visualizations
## Data Visualization with Python (IBM Skills Network)
[Darkhorse Analytics](http://www.darkhorseanalytics.com/) is a quantitative consultancy specialized on data analytics and visualizations. The company is known for a rigorously minimalist approach when it comes to data visualizations
### Matplotlib Architecture
Matplotlib Architecture entails three layers:
1. Backend Layer: FigureCanvas, Renderer, Events
 1.1 FigureCanvas: matplotlib.backend_bases.FigureCanvas, encompasses the are onto which the figure is drawn.
 1.2 Renderer: matplotlib.backend_bases.Renderer, draws the figure
 1.3 Events: matplotlib.backend_bases.Event, handles events like keyboard strokes and mouse klicks
2. Artist Layer: Artist, connects abstract elements with the renderer drawing on the canvas:
 Everything that is visible on the graphic is essentially an instance of an Artist object. There are two types of Artist objects:
 2.1 Primitives: Lines, Rectangles, Circles, and Text
 2.2 Composite: Axis, Tick, Axes, and Figure
 The Figure Artist is the toplevel object that contains and manages all elements in a graphic. Each composite Artist may contain other composite artists as wella s primitive artists.
3. Scripting Layer: pyplot, server as a quick access to the Artist layer

Here are two ways to generate a histogram, first by going through the Artist layer, and second by using the scripting layer.

The code to go directly to the Artist Layer is much longer.
~~~
from matplotlib.backends.backend_agg import FigureCanvas as FigureCanvas 
from matplotlib.figure import Figure

# creating instances
fig = Figure()
canvas = FigureCanvas(fig)

import numpy as np
x = np.random.randn(10000) # generate data


ax = fig.add_subplot(111) # creating an axis artist (111 = 1 row,1 col,subplot goes to cell 1)
    # (automatically added to fig.axes conatiner, since it is an Axis Artist)
    
ax.hist(x,100) # call axis method to gen histogram
    # (automatically added to fig.axes conatiner,  since it is an Axis Artist method)

ax.set_title('Normal distribution with $\mu=0, \sigma=1$')
~~~
While the code using the Scripting Layer is more neat, but also more restricted.
~~~

~~~

Both results in:

![Histogram Example](matplotlib_ArtistLayerExample.png "Histogram")


