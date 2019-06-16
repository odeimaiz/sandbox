import pandas as pd

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

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

client = leaderboard.create_client()

timeframe='this_year'
gender='M'
club_id=316340 #Veloton
# club_id=None
nResults = 20
VCH_ITT_19_1 = 20600593
VCH_ITT_19_2 = 20601219
segments = [VCH_ITT_19_1, VCH_ITT_19_2]
for segment_id in segments:
	leaderboard.learboard_to_csv(client, segment_id, timeframe, gender, club_id, nResults)

df_overall = pd.read_csv(str(VCH_ITT_19_1)+'_leaderboard.csv')
df_up = pd.read_csv(str(VCH_ITT_19_1)+'_leaderboard.csv')
df_down = pd.read_csv(str(VCH_ITT_19_2)+'_leaderboard.csv')

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

        html.Div([
            html.H2(
                children='Overall',
                style=centered_text
            ),
            dash_table.DataTable(
                id='table_overall',
                columns=[{"name": i, "id": i} for i in df_overall.columns],
                data=df_overall.to_dict('records'),
            )
        ], style=flex_column),

        html.Div([
            html.H2(
                children='Up',
                style=centered_text
            ),
            dash_table.DataTable(
                id='table_up',
                columns=[{"name": i, "id": i} for i in df_up.columns],
                data=df_up.to_dict('records'),
            )
        ], style=flex_column),

        html.Div([
            html.H2(
                children='Down',
                style=centered_text
            ),
            dash_table.DataTable(
                id='table_down',
                columns=[{"name": i, "id": i} for i in df_down.columns],
                data=df_down.to_dict('records'),
            )
        ], style=flex_column)
    ], style=flex_columns)
], style=veloton_style)

if __name__ == '__main__':
    app.run_server(debug=True)