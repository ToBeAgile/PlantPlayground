import socket
import sys
import pickle
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import threading
import datetime
import time
import csv

host = ''
port = 50000
backlog = 5
size = 5096

#dl = DataLogger()

s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    myIP = socket.gethostbyname(socket.gethostname())
    print("Created socket at " + myIP + " on port " + str(port))
    print("Listening for client connections...")
    s.listen(backlog)
    client, address = s.accept()  # blocks until the pi connects
    print("Accepted client connection from " + str(address[0]) + " on port " + str(address[1]))
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)


a_time_q = deque(maxlen=50)
a_time_q.append(1)
a_value_q = deque(maxlen=50)

b_time_q = deque(maxlen=50)
b_time_q.append(1)
b_value_q = deque(maxlen=50)

time_mark = datetime.datetime.now()
time_mark_set = False

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Button('Set Time Marker', id='set-marker', n_clicks=0),
        html.Button('Save Note', id='save-note', n_clicks=0),
        dcc.Input(id="input-field", type="text", placeholder="", value="", debounce=True),
        html.Div(id='text-output', children='Enter your value'),
        html.Div(id='time-mark-output', children=''),
        dcc.Graph(id='a-graph', animate=True),
        dcc.Graph(id='b-graph', animate=True),
        dcc.Interval(
            id='a-update',
            interval=1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='b-update',
            interval=1000,
            n_intervals=0
        ),
    ]
)


@app.callback(
    Output('time-mark-output', 'children'),
    [Input('set-marker', 'n_clicks')])
def set_marker(button_clicks):
    global time_mark
    global time_mark_set
    time_mark = datetime.datetime.now()
    time_mark_set = True
    return 'Time mark set: {}'.format(time_mark.strftime("%Y-%m-%d %H:%M:%S:%f"))




#read from the text input
#write that text output to a file
#n_submit correct behavior, but incorrect value
#value correct value, but incorrect behavior
@app.callback(
    Output('text-output', 'children'),
    [Input('input-field', 'n_submit'), Input('save-note', 'n_clicks')],
    [State('input-field', 'value')])
def save_note(text_submit, button_clicks, text_value):
    global time_mark
    global time_mark_set
    
    if not time_mark_set:
        time_mark = datetime.datetime.now()
    with open('notes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time_mark.strftime("%Y-%m-%d %H:%M:%S:%f"), text_value])
    time_mark_set = False
    return 'You entered: {}'.format(text_value)

@app.callback(Output('a-graph', 'figure'),
              [Input('a-update', 'n_intervals')])
def update_a_graph(n):
    data = plotly.graph_objs.Scatter(
            x=list(a_time_q),
            y=list(a_value_q),
            name='a-graph',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[(max(a_time_q)-50),max(a_time_q)]),
                                                yaxis=dict(range=[(min(a_value_q)-5),max(a_value_q)+5]),)}

@app.callback(Output('b-graph', 'figure'),
              [Input('b-update', 'n_intervals')])
def update_b_graph(n):
    data = plotly.graph_objs.Scatter(
            x=list(b_time_q),
            y=list(b_value_q),
            name='b-graph',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[(max(b_time_q)-50),max(b_time_q)]),
                                                yaxis=dict(range=[(min(b_value_q)-5),max(b_value_q)+5]),)}


def update_data():
    while True:
        serialized_data = client.recv(size)
        #value = pickle.loads(serialized_data)
        try: #deal with occasional broken network data
            data_dict = pickle.loads(serialized_data)
            sensor = data_dict["sensor"]
        except:
            data_dict = {"sensor": "junk", "value": 0, "time": 0}
            print("Bad Network Data")
        if sensor == "a_sensor":
            a_time = data_dict["time"]
            a_value = data_dict["value"]
            a_time_q.append(a_time_q[-1]+1)
            a_value_q.append(a_value)
        elif sensor == "b_sensor":
            b_time = data_dict["time"]
            b_value = data_dict["value"]
            b_time_q.append(b_time_q[-1]+1)
            b_value_q.append(b_value)
        else:
            print("Bad network data!")
        #value = data_dict["value"]
        #time = data_dict["time"]
        #print("Time: ", time, " Value: ", value)
        #dl.write(str(time), str(value))

if __name__ == '__main__':
    threading.Thread(target=update_data).start()
    #threading.Thread(target=app.run_server).start()
    threading.Thread(target=app.run_server, kwargs={'debug': True, 'use_reloader': False}).start()
    #app.run_server(debug=True, use_reloader=False) #to debug and block reload
    #see https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode for another option to block only certain things from being reinitialized
