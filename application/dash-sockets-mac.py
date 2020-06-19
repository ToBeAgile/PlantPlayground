import socket
import sys
import pickle
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import threading
#sys.path.insert(1, '/Users/davidscottbernstein/Dropbox/Dev/Python/Projects/PlantPlayground')
#from services.DataLogger import DataLogger
import time

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


a_time_q = deque(maxlen=300)
a_time_q.append(1)
a_value_q = deque(maxlen=300)
a_value_q.append(1)

b_time_q = deque(maxlen=300)
b_time_q.append(1)
b_value_q = deque(maxlen=300)
b_value_q.append(1)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(n):
    data = plotly.graph_objs.Scatter(
            x=list(a_time_q),
            y=list(a_value_q),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[(max(a_time_q)-50),max(a_time_q)]),
                                                yaxis=dict(range=[(min(a_value_q)-5),max(a_value_q)+5]),)}


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
        #value = data_dict["value"]
        #time = data_dict["time"]
        #print("Time: ", time, " Value: ", value)
        #dl.write(str(time), str(value))

if __name__ == '__main__':
    threading.Thread(target=update_data).start()
    threading.Thread(target=app.run_server).start()
    #app.run_server(debug=True, use_reloader=False) #to debug and block reload
    #see https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode for another option to block only certain things from being reinitialized
