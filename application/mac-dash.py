import datetime
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# graph stuff
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
Y2 = deque(maxlen=20)
Y2.append(1)

isMarkTimeSet = False
now = datetime.datetime.now()

ip = ""
port = 50000

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Button('Set Time Marker', id='set-marker', n_clicks=0),
        dcc.Input(id="input-field", type="text", placeholder="", value="", debounce=True),
        html.Button('Save Note', id='save-note', n_clicks=0),
        html.Div(id='time-output', children='Time: '),
        html.Div(id='text-output', children='Entry: '),
        dcc.Graph(id='live-graph0', animate=True),
        dcc.Interval(
            id='graph-update0',
            interval=1000,
            n_intervals=0
        ),
        dcc.Graph(id='live-graph1', animate=True),
        dcc.Interval(
            id='graph-update1',
            interval=1000,
            n_intervals=0
        ),
    ]
)


@app.callback(
    Output('time-output', 'children'),
    [Input('set-marker', 'n_clicks')])
def set_marker(button_clicks):
    global isMarkTimeSet
    global now
    isMarkTimeSet = True
    now = datetime.datetime.now()
    return ['Now is ', now.strftime("%Y-%m-%d %H:%M:%S:%f")]


@app.callback(
    Output('text-output', 'children'),
    [Input('input-field', 'value'), Input('save-note', 'n_clicks')])
def save_note(text_value, button_clicks):

    # read from the text input
    # write that text output to a file
    global isMarkTimeSet
    global now
    if not isMarkTimeSet:
        now = datetime.datetime.now()
    with open('../data/notes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f"), text_value])
    isMarkTimeSet = False
    return ["Placeholder"]
    #except:
        #e = sys.exc_info()[0]
        #print(e)
    #return 'You entered: {}'.format(text_value)


@app.callback(Output('live-graph0', 'figure'),
              [Input('graph-update0',
                     'n_intervals')])  # make your input when sensor value changes (post filtering). This will trigger a graph update
# @app.callback(Output('live-graph1', 'figure'),
#        [Input('graph-update1', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update
def update_graph_a(n):
    X.append(X[-1] + 1)
    c0_value = 12
    Y.append(c0_value)  # modify these with your sensor values
    # Y2.append(c1_value)

    data0 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Channel 0',
        mode='lines+markers'
    )

    return {'data': [data0], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                 # modify this to only track the max(X) - 20 or something
                                                 yaxis=dict(range=[min(Y), max(Y)]), )}


@app.callback(Output('live-graph1', 'figure'),
              [Input('graph-update1',
                     'n_intervals')])  # make your input when sensor value changes (post filtering). This will trigger a graph update
def update_graph_b(n):
    X.append(X[-1] + 1)
    c1_value = 54
    Y2.append(c1_value)

    data1 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y2),
        name='Channel 1',
        mode='lines+markers'
    )

    return {'data': [data1], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                 # modify this to only track the max(X) - 20 or something
                                                 yaxis=dict(range=[min(Y), max(Y)]), )}

def raw_handler(address, *args):
    print(f"{address}: {args}")

if __name__ == '__main__':
    dispatcher = Dispatcher()
    dispatcher.map("/PP01/ADC0/RAW/", raw_handler)
    dispatcher.map("/PP01/ADC1/RAW/", raw_handler)
    #server = BlockingOSCUDPServer((ip, port), dispatcher)
    #server.serve_forever()  # Blocks forever
    app.run_server(host="0.0.0.0", debug=True)
