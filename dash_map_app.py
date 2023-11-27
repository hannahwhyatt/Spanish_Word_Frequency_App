import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input, Patch
from dash.exceptions import PreventUpdate

map_app = Dash(__name__)
server = map_app.server 

DB_USER = os.getenv('db_username')
DB_PASSW = os.getenv('db_password')
HOST = os.getenv('db_host')

conn_string = "postgresql://{}:{}@{}/escorpus".format(DB_USER, DB_PASSW, HOST)

engine = create_engine(conn_string)
query = f'SELECT * FROM frequency;'
frequency_table = pd.read_sql(query, con=engine)

full_names = ['Argentina', 
           'Bolivia', 
           'Chile', 
           'Costa Rica', 
           'Colombia',
           'Cuba', 
           'Dominican Republic', 
           'Ecuador', 
           'Spain', 
           'Guatemala', 
           'Honduras', 
           'Mexico', 
           'Nicaragua', 
           'Panama', 
           'Peru', 
           'Puerto Rico',
           'Paraguay', 
           'El Salvador', 
           'United States', 
           'Uruguay', 
           'Venezuela']

frequency_table_T = frequency_table.T
frequency_table_T = frequency_table_T.rename(columns=frequency_table_T.iloc[0]).drop(frequency_table_T.index[0])
lemma = frequency_table_T.columns[:].to_list()

df = frequency_table_T[lemma].astype(np.float64)
df.insert(0, 'country_name', full_names)


map_app.layout = html.Div([
    dcc.Dropdown(
        lemma,
        id='dynamic-dropdown',
        placeholder='Enter a word',
        value='carro',
               style={'width':'50%', 'font-family': 'Arimo'}
    ),
    dcc.Graph(id='graph-content', 
             style={'height': '80vh', 'width': '100%'}),
    html.Div(id='sidebar', children=[], )
], style={'padding': '20px'})

@callback(
    Output("dynamic-dropdown", "options"),
    Input("dynamic-dropdown", "search_value")
)

def update_options(search_value):
    if search_value is None:
        raise PreventUpdate
    options = [{'label': word, 'value': word} for word in lemma if word is not None and word.startswith(search_value)]
    return options

@callback(
    [Output('graph-content', 'figure'),
    Output('sidebar', 'children')],
    Input('dynamic-dropdown', 'value')
)

def update_graph(value):
    fig = px.choropleth(df, 
                    projection='natural earth',
                    locationmode='country names', 
                    locations=df['country_name'], 
                    color=df[value], color_continuous_scale='Sunsetdark')
    fig.update_layout(coloraxis_colorbar_x=1,
                     coloraxis=dict(colorbar_title=f''))
    fig.update_traces(hovertemplate="%{location}<br>%{z}", selector=dict(type='choropleth'))
    sidebar_info = "" # max(df[value])
    return fig, sidebar_info

if __name__ == '__main__' or os.environ.get('GUNICORN_CMD_ARGS', '') == '':
    map_app.run(debug=True)
