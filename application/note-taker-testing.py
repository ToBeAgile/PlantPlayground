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
        
        html.Button('Save Note', id='save-note', n_clicks=0),
        dcc.Input(id="input-field", type="text", placeholder="", value="Hello", debounce=True),
        html.Div(id='text-output', children='Enter your value'),
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


"""
@app.callback(
    Output('button-output', 'children'),
    [Input('save-note', 'n_clicks')])
def save_note(n_clicks):
    #read from the text input
    #write that text output to a file
    now = datetime.datetime.now()
    with open('../data/notes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S:%f")])
    return 'The button was clicked "{}" times'.format(n_clicks)
"""

if __name__ == '__main__':
    app.run_server(debug=True)