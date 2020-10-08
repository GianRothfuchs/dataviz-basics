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
3. Scripting Layer: pyplot, serves as a quick access to the Artist layer through the matplotlib.pyplot interface

Here are two ways to generate a histogram, first by going through the Artist layer, and second by using the scripting layer.

The code to go directly to the Artist Layer is syntactically heavy, but very flexible in return:
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
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(10000)
plt.hist(x, 100)
plt.title('Normal distribution with $\mu=0, \sigma=1$')
plt.show()
~~~
 
Both results in:

![Histogram Example](assets/matplotlib_ArtistLayerExample.png "Histogram")

Furter literature on the architecture of matplotlib can be found [here](http://aosabook.org/en/matplotlib.html).
