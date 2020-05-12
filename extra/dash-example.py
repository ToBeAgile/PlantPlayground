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
            n_intervals = 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]) #make your input when sensor value changes (post filtering). This will trigger a graph update

def update_graph_scatter(n):

    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1)) #modify these with your sensor values

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]), #modify this to only track the max(X) - 20 or something
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

#if __name__ == '__main__':
app.run_server(debug=True)