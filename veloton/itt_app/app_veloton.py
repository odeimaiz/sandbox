import pandas as pd

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import strava_client
import leaderboard

veloton_style = {
    'color': '#5e7e95',
    'backgroundColor': '#bad9ed',
    'gridColor': '#444'
}
flex_columns = {
    'display': 'flex'
}
flex_column = {
    'flex': 1,
    'min-width': 0
}
unflex_column = {
    'flex': 0,
    'min-width': '400px',
    'margin': '10px',
    'color': veloton_style['color'],
    'backgroundColor': veloton_style['backgroundColor']
}
centered_text = {
    'text-align': 'center',
    'color': veloton_style['color'],
    'backgroundColor': veloton_style['backgroundColor']
}
hidden = {
    'display': 'none'
}
dcc_input = {
    'color': veloton_style['color'],
    # 'backgroundColor': veloton_style['gridColor']
}
dcc_input_button = {
    'height': '40px',
    'width': '100%',
    'color': dcc_input['color'],
    # 'backgroundColor': dcc_input['backgroundColor']
}
dcc_input_label = {
    'width': '200px',
    'float': 'left'
}
dcc_input_number = {
    'height': '30px',
    'width': '200px',
    'color': dcc_input['color'],
    # 'backgroundColor': dcc_input['backgroundColor']
}
dcc_input_pair = {
    'overflow': 'hidden',
    'margin-top': '2px',
    'margin-bottom': '2px',
    'color': veloton_style['color'],
    'backgroundColor': veloton_style['backgroundColor']
}

client = strava_client.create_client()


app = dash.Dash(__name__)
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(children=[
    html.Div([
        # Controls on the left side
        html.Div([
            html.Div(
                id='logo',
                style=centered_text
            ),
            html.H1(
                children='Zurich Veloton ITT',
                style=centered_text
            ),
            html.Div(
                children='Sihlstrasse Up&Down. August 28th',
                style=centered_text
            ),

            html.Div([
                html.Div(
                    children='Options'
                ),
                dcc.Dropdown(
                    id='timeframe',
                    options=[
                        {'label': 'All time', 'value': 0},
                        {'label': 'This year', 'value': 'this_year'},
                        {'label': 'This month', 'value': 'this_month'},
                        {'label': 'Today', 'value': 'today'}
                    ],
                    value=0
                ),
                dcc.Dropdown(
                    id='gender',
                    options=[
                        {'label': 'All', 'value': 0},
                        {'label': 'Men', 'value': 'M'},
                        {'label': 'Women', 'value': 'F'}
                    ],
                    value=0
                ),
                dcc.Dropdown(
                    id='club_id',
                    options=[
                        {'label': '', 'value': 0},
                        {'label': 'Veloton', 'value': 316340}
                    ],
                    value=316340
                ),
            ]),

            html.Div([
                html.Div(
                    children='Segments'
                ),
                html.Div([
                    html.Div([
                        html.Label('Segment 1:')
                    ], style=dcc_input_label),
                    dcc.Input(
                        id='segment_1',
                        type='number',
                        value=20600593,
                        style=dcc_input_number
                    )
                ], style=dcc_input_pair),
                html.Div([
                    html.Div([
                        html.Label('Segment 2:')
                    ], style=dcc_input_label),
                    dcc.Input(
                        id='segment_2',
                        type='number',
                        value=20601219,
                        style=dcc_input_number
                    )
                ], style=dcc_input_pair)
            ]),
            
            html.Div([
                html.Button('Update', id='update-button')
            ])
        ], style=unflex_column),
        
        html.Div(id='input-data', style=hidden),

        html.Div([
            html.H2(
                children='Overall',
                style=centered_text
            ),
            html.Div(id='segment-overall-table')
        ], style=flex_column),

        html.Div([
            html.H2(
                children='Up',
                style=centered_text
            ),
            html.Div(id='segment1-table')
        ], style=flex_column),

        html.Div([
            html.H2(
                children='Down',
                style=centered_text
            ),
            html.Div(id='segment2-table')
        ], style=flex_column)
    ], style=flex_columns)
], style=veloton_style)


@app.callback(
    Output('input-data', 'children'),
    [Input('update-button', 'n_clicks')],
    state=[
        State(component_id='segment_1', component_property='value'),
        State(component_id='segment_2', component_property='value'),
        State(component_id='timeframe', component_property='value'),
        State(component_id='gender', component_property='value'),
        State(component_id='club_id', component_property='value')
    ]
)
def dump_to_csv(_n_clicks, segment_1_id, segment_2_id, timeframe, gender, club_id):
    print(segment_1_id, segment_2_id, timeframe, gender, club_id)
    if timeframe is 0:
        timeframe = None
    if gender is 0:
        gender = None
    if club_id is 0:
        club_id = None
    nResults = 20
    segments = [segment_1_id, segment_2_id]
    for segment_id in segments:
        leaderboard.learboard_to_csv(client, segment_id, timeframe, gender, club_id, nResults)
    leaderboard.sum_learboards(segment_1_id, segment_2_id)
    segments.append('overall')
    return segments

def create_table(segment_id, table_id):
    df = pd.read_csv(str(segment_id)+'_leaderboard.csv')
    table = dash_table.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
    return table

@app.callback(
    Output('segment1-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_1(data):
    segment_id = data[0]
    return create_table(segment_id, 'table_1')

@app.callback(
    Output('segment2-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_2(data):
    segment_id = data[1]
    return create_table(segment_id, 'table_2')

@app.callback(
    Output('segment-overall-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_overall(data):
    segment_id = data[2]
    return create_table(segment_id, 'table_3')


if __name__ == '__main__':
    app.run_server(debug=True)