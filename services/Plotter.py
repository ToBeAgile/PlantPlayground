import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#class Plotter:
    #style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []
x_increment = 0

def animate(i):
    ax1.clear()
    ax1.plot(xs, ys)
    
def my_plot(value):
    ys.append(value)
    xs.append(x_increment)
    x_increment += 1
    
ani = animation.FuncAnimation(fig=fig, func=animate, interval=1000)
plt.show()
