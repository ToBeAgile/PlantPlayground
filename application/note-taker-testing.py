import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import datetime
import csv

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(id='button-output', children='Enter your value'),
        html.Button('Save Note', id='save-note', n_clicks=0)
    ]
)

@app.callback(
    Output('button-output', 'children'),
    [Input('save-note', 'n_clicks')])
def save_note(n_clicks):
    now = datetime.datetime.now()
    with open('../data/notes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f")])
    return 'The button was clicked "{}" times'.format(n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)