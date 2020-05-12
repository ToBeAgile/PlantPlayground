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
SLEEP = 1
NUMBEROFCHANNELS = 2
DIFFERENTIAL1 = 0
DIFFERENTIAL2 = 3

CHANNEL0 = 0
CHANNEL1 = 1
CH0SLEEPTIME = 0.5
CH1SLEEPTIME = 0.5

#create an instance of ADS1115 Reader
reader = ADS1115Reader()

# channel 0 is the control (a potato) gets read a second every minute
reader.open(differential=CHANNEL0, gain=GAIN, data_rate=DATA_RATE, sleep=CH0SLEEPTIME) #open channel 0 stream
reader.open(differential=CHANNEL1, gain=GAIN, data_rate=DATA_RATE, sleep=CH1SLEEPTIME) #open channel 1 stream

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
        html.Button('Save Note', id='save-note', n_clicks=0),
        dcc.Input(id="input-field", type="text", placeholder="", value="", debounce=True),
        html.Div(id='text-output', children='Enter your value'),
        dcc.Graph(id='live-graph0', animate=True),
        dcc.Interval(
            id='graph-update0',
            interval=1000,
            n_intervals = 0
        ),
        dcc.Graph(id='live-graph1', animate=True),
        dcc.Interval(
            id='graph-update1',
            interval=1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('text-output', 'children'),
    [Input('input-field', 'value'), Input('save-note', 'button_clicks')])
def save_note(text_value, button_clicks):
    #read from the text input
    #write that text output to a file
    now = datetime.datetime.now()
    with open('../data/notes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f"), text_value])
    return 'You entered: {}'.format(text_value)

@app.callback(Output('live-graph0', 'figure'),
        [Input('graph-update0', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update

#@app.callback(Output('live-graph1', 'figure'),
#        [Input('graph-update1', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update

def update_graph_a(n):

    X.append(X[-1]+1)
    time.sleep(0.01)
    c0_value = reader.read(DIFFERENTIAL1, GAIN, DATA_RATE, CH0SLEEPTIME)
    #c1_value = reader.read(DIFFERENTIAL2, GAIN, DATA_RATE, CH1SLEEPTIME)
    #print("C0: ", c0_value)
    #print("C1: ", c1_value)
    Y.append(c0_value) #modify these with your sensor values
    #Y2.append(c1_value)
    

    data0 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Channel 0',
            mode= 'lines+markers'
            )

    return {'data': [data0],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]), #modify this to only track the max(X) - 20 or something
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


@app.callback(Output('live-graph1', 'figure'),
        [Input('graph-update1', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update
def update_graph_b(n):

    X.append(X[-1]+1)
    time.sleep(0.01)
    c1_value = reader.read(DIFFERENTIAL2, GAIN, DATA_RATE, CH1SLEEPTIME)
    #print("C0: ", c0_value)
    #print("C1: ", c1_value)
    Y2.append(c1_value)

    data1 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y2),
            name='Channel 1',
            mode= 'lines+markers'
            )

    return {'data': [data1],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]), #modify this to only track the max(X) - 20 or something
                                                yaxis=dict(range=[min(Y),max(Y)]),)}
    #todo better autorange

#if __name__ == '__main__':
#app.run_server(debug=True)
app.run_server(host="0.0.0.0", debug=True)