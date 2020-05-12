import datetime as dt
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
    pullData = open("data_file.csv","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y,z = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
            zar.append(int(z))
    ax1.clear()
    ax1.plot(xar,yar, zar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

    
    #vget data y1 and y2
    # plt.cla()
    # plt.plot(x, y1, label='Channel 0')
    # plt.plot(x, y2, label='Channel 1')
    # ani = animation.FuncAnimation(fig=fig, func=animate, interval=1000)
    # plt.show()
    
    # plt.legend(loc='upper left')
    # plt.tight_layout()
    
    
def my_plot(value):
    ys.append(value)
    xs.append(x_increment)
    x_increment += 1
    

""" EXAMPLE OF LIVE GRAPH
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tmp102

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
tmp102.init()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = round(tmp102.read_temp(), 2)
    ch0_value = round(

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(ch0_value)
    ys.append(ch1_value)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Voltage over Time')
    plt.ylabel('Current (millivolts)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()


"""