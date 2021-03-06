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
sys.path.insert(1, '/Users/davidscottbernstein/Dropbox/Dev/Python/Projects/PlantPlayground')
from services.DataLogger import DataLogger

host = ''
port = 50000
backlog = 5
size = 1024

#instantiate the writer and write the header
dl = DataLogger()
dl.write("Plant bioelectric data log. Project: Setup")
dl.write(dl.filename)
dl.write("Channel0 is the control (a potato).")
dl.write("Channel1 is the plant connected to tinned copper wire.")
dl.write("Gain: " + str(GAIN))
dl.write("Volts per division: " + str(reader.voltsPerDivision))
dl.write("Data rate: " + str(DATA_RATE))
dl.write("Time                 Value in mV")

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


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)


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
    serialized_data = client.recv(size)
    data_dict = pickle.loads(serialized_data)
    time = data_dict["time"]
    topic = data_dict["topic"]
    sensor = data_dict["sensor"]
    value = data_dict["value"]

    if topic == "SEC":
        dl.write(str(time), str(sensor), str(value))

    X.append(X[-1]+1)
    Y.append(value)
    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    #isDashInitialized = True
    #app.run_server() #debug enables reload by default. This means that every line is run again, resulting in reinitialization. This breaks sockets.
    app.run_server(debug=True, use_reloader=False) #to debug and block reload
    #see https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode for another option to block only certain things from being reinitialized