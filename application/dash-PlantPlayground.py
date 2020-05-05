#this likely won't be able to track all data points. It may be a good idea to choose a set number of
#data points, and then write out the graph. Or, write out the graph once per hour (just make sure it can handle this)
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

import sys
sys.path.insert(1, '/home/pi/Documents/Code/PlantPlayground')
from services.ADS1115Reader import *
from services.DataLogger import *
import datetime

#sensor stuff
GAIN = 16
DATA_RATE = 8
SLEEP = 2
NUMBEROFCHANNELS = 2
DIFFERENTIAL1 = 0
DIFFERENTIAL2 = 3

CHANNEL0 = 0
CHANNEL1 = 1
CH0SLEEPTIME = 30
CH1SLEEPTIME = 30

#create an instance of ADS1115 Reader
reader = ADS1115Reader()

# channel 0 is the control (a potato) gets read a second every minute
reader.open(channel=CHANNEL0, gain=GAIN, data_rate=DATA_RATE, sleep=CH0SLEEPTIME) #open channel 0 stream
reader.open(channel=CHANNEL1, gain=GAIN, data_rate=DATA_RATE, sleep=CH1SLEEPTIME) #open channel 1 stream

#graph stuff
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
Y2 = deque(maxlen=20)
Y2.append(1)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update

def update_graph_scatter(n):

    X.append(X[-1]+1)
    c0_value = reader.read(DIFFERENTIAL1, GAIN, DATA_RATE, 0)
    time.sleep(0.01)
    c1_value = reader.read(DIFFERENTIAL2, GAIN, DATA_RATE, 0)
    print("C0: ", c0_value)
    print("C1: ", c1_value)
    Y.append(c1_value) #modify these with your sensor values
    Y2.append(c0_value)
    

    data1 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )
    data2 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y2),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data1, data2],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]), #modify this to only track the max(X) - 20 or something
                                                yaxis=dict(range=[8,15]),)}
    #todo better autorange

#if __name__ == '__main__':
app.run_server(debug=True)