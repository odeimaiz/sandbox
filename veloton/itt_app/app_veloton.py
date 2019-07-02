import pandas as pd
import datetime

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

# ITT_1 = 20600593
# ITT_2 = 20601219
# Susten 5145893
# Grimsel -
# Nufenen 658845
# Gottard 10050259
# Forststrasse 4164918
# Double Whopper 762274
SEGMENT_ID_1 = 5145893
SEGMENT_ID_2 = 658845
SEGMENT_ID_3 = 10050259
SEGMENT_LABEL_1 = 'Susten'
SEGMENT_LABEL_2 = 'Nufenen'
SEGMENT_LABEL_3 = 'Gottard'

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
                children='Zurich Veloton',
                style=centered_text
            ),
            html.H3(
                children='Wednesday Ride long climbs',
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
                        value=SEGMENT_ID_1,
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
                        value=SEGMENT_ID_2,
                        style=dcc_input_number
                    )
                ], style=dcc_input_pair),
                html.Div([
                    html.Div([
                        html.Label('Segment 3:')
                    ], style=dcc_input_label),
                    dcc.Input(
                        id='segment_3',
                        type='number',
                        value=SEGMENT_ID_3,
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
                children=SEGMENT_LABEL_1,
                style=centered_text
            ),
            html.Div(id='segment1-table')
        ], style=flex_column),

        html.Div([
            html.H2(
                children=SEGMENT_LABEL_2,
                style=centered_text
            ),
            html.Div(id='segment2-table')
        ], style=flex_column),

        html.Div([
            html.H2(
                children=SEGMENT_LABEL_3,
                style=centered_text
            ),
            html.Div(id='segment3-table')
        ], style=flex_column)
    ], style=flex_columns)
], style=veloton_style)


@app.callback(
    Output('input-data', 'children'),
    [Input('update-button', 'n_clicks')],
    state=[
        State(component_id='segment_1', component_property='value'),
        State(component_id='segment_2', component_property='value'),
        State(component_id='segment_3', component_property='value'),
        State(component_id='timeframe', component_property='value'),
        State(component_id='gender', component_property='value'),
        State(component_id='club_id', component_property='value')
    ]
)
def dump_to_csv(_n_clicks, segment_1_id, segment_2_id, segment_3_id, timeframe, gender, club_id):
    print(segment_1_id, segment_2_id, segment_3_id, timeframe, gender, club_id)
    if timeframe is 0:
        timeframe = None
    if gender is 0:
        gender = None
    if club_id is 0:
        club_id = None
    nResults = 100
    segments = []
    if segment_1_id != 0:
        segments.append(segment_1_id)
    if segment_2_id != 0:
        segments.append(segment_2_id)
    if segment_3_id != 0:
        segments.append(segment_3_id)
    for segment_id in segments:
        leaderboard.learboard_to_csv(client, segment_id, timeframe, gender, club_id, nResults)
    leaderboard.sum_learboards(segments)
    segments.insert(0, 'overall')
    return segments

def create_table(data, index, table_id):
    if index == 'overall' or len(data) > index:
        if index == 'overall':
            segment_id = 'overall'
        else:
            segment_id = data[index]
        df = pd.read_csv('leaderboards/'+str(segment_id)+'.csv')
        for index, row in df.iterrows():
            formatted = str(datetime.timedelta(seconds=row['Time']))
            # formatted = formatted[2:]
            df.loc[index, 'Time'] = formatted
        table = dash_table.DataTable(
            id=table_id,
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
        return table
    return

@app.callback(
    Output('segment1-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_1(data):
    id = 1
    return create_table(data, 1, 'table_'+str(id))

@app.callback(
    Output('segment2-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_2(data):
    id = 2
    return create_table(data, 2, 'table_'+str(id))

@app.callback(
    Output('segment3-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_3(data):
    id = 3
    return create_table(data, id, 'table_'+str(id))

@app.callback(
    Output('segment-overall-table', 'children'),
    [Input('input-data', 'children')]
)
def create_table_overall(data):
    id = 'overall'
    return create_table(data, 'overall', 'table_'+str(id))


if __name__ == '__main__':
    app.run_server(debug=True)