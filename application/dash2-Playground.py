#make sure this will update, even if no one is listening

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import time

import sys
sys.path.insert(1, '../')
from services.ADS1115Reader import *
from services.DataLogger import *
import datetime

#sensor stuff

GAIN = 16
DATA_RATE = 8
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
reader.open(differential=0, gain=GAIN, data_rate=DATA_RATE, sleep=CH0SLEEPTIME) #open channel 0 stream
reader.open(differential=3, gain=GAIN, data_rate=DATA_RATE, sleep=CH1SLEEPTIME) #open channel 1 stream

#instantiate the writer and write the header
dl= DataLogger()
dl.write("Plant bioelectric data log. Project: Setup")
dl.write(dl.filename)
dl.write("Channel0 is the control (a potato) sampled once every minute for a second.")
dl.write("Channel1 is the plant connected to tinned copper wire and sampled every minute for 59 seconds.")
dl.write("Gain: " + str(GAIN))
#dl.write("Volts per division: " + str(reader.voltsPerDivision))
dl.write("Data rate: " + str(DATA_RATE))
dl.write("Time                 Value in mV")

input_a = []
input_b = []
input_c = []
input_d = []
time_list_a = [0]   #probably should move time into ADSReader.read, so that time is logged when the value is read
time_list_b = [0]
time_list_c = []
time_list_d = []

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph-0', animate=True),
        dcc.Interval(
        id='graph-update-0',
        interval=1000,
        n_intervals = 0
        ),
        dcc.Graph(id='live-graph-1', animate=True),
        dcc.Interval(
            id='graph-update-1',
            interval=1000,
            n_intervals = 0
        ),

    ]
)

@app.callback(Output(component_id='live-graph-0', component_property='figure'),
        [Input(component_id='graph-update-0', component_property='n_intervals')])
def update_graph_0(input_value):
    #read inputs (reconfigure read to get time)
    #value_a = random.randint(-20, 20) #todo replace with a sensor reading
    #value_b = random.randint(-20, 20)
    value_a = reader.read(DIFFERENTIAL1, GAIN, DATA_RATE, 0)
    input_a.append(value_a)
    time_list_a.append(time_list_a[-1]+1)

    #Log data via DataLogger
    #now = datetime.datetime.now()
    #dl.write(((now.strftime("%H:%M:%S:%f")), (round((value_a), 4)), (round((value_b), 4))))

    data = go.Scatter(
            x=time_list_a,
            y=input_a,
            name='Channel 0',
            mode= 'lines+markers'
            )
    
    #fig_0 = go.Figure(data=[data], layout=go.Layout(xaxis=dict(range=[time_list_a[-1]-20, time_list_a[-1]]), yaxis=dict(range=[-30,30])))
    

    #periodically save the graph (currently set to every 10 data points for testing)
    if time_list_a[-1]%10 == 0:
        try:
            fig_0.write_html("../data/save_a.html")
        except:
            e = sys.exc_info()[0]
            print(e)

    #return fig_0
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[time_list_a[-1]-20, time_list_a[-1]]), yaxis=dict(range=[-30,30]))}


#@app.callback automatically wraps the following function. It automatically passes it the 
#inputs component property, in this case n_intervals (and also unused in this case)
#Whenever an input property changes, the wrapped function will get called automatically.
#the return value automatically updated the output return property
@app.callback(Output(component_id='live-graph-1', component_property='figure'),
        [Input(component_id='graph-update-0', component_property='n_intervals')])
def update_graph_1(input_value):
    time.sleep(.005)
    value_b = reader.read(DIFFERENTIAL2, GAIN, DATA_RATE, 0)
    input_b.append(value_b)
    time_list_b.append(time_list_b[-1]+1)
    #time_list_a.append(int(time.time()))
    #time_list_b.append(int(time.time()))

    data = go.Scatter(
            x=time_list_b,
            y=input_b,
            name='Channel 1',
            mode= 'lines+markers'
            )


    #fig_1 = go.Figure(data=[data], layout=go.Layout(xaxis=dict(range=[time_list_a[-1]-20, time_list_a[-1]]), yaxis=dict(range=[-30,30])))

    #periodically save the graph (currently set to every 10 data points for testing)
    if time_list_b[-1]%10 == 0:
        try:
            fig_1.write_html("../data/save_b.html")
        except:
            e = sys.exc_info()[0]
            print(e)

    #return fig_1
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[time_list_b[-1]-20, time_list_b[-1]]), yaxis=dict(range=[-30,30]))}

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host="0.0.0.0", debug=True) #expose to your local network