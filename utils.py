import pandas as pd
import numpy as np
from dash import html
import dash_bootstrap_components as dbc


def create_df_for_animation(dfi):
    start = 2
    obs = len(dfi)

    # new datastructure for animation
    df = pd.DataFrame() # container for df with new datastructure
    for i in np.arange(start,obs):
        dfa = dfi.head(i).copy()
        dfa['frame'] = i
        df = pd.concat([df, dfa])
    return df

def generate_net_change(figure, trace):
    name = figure['data'][trace]['legendgroup']
    current_y_data = figure['data'][trace]['y'][-1]
    previous_y_data = figure['data'][trace]['y'][-2]
    net_change = current_y_data - previous_y_data
    if net_change > 0:
        color = "green"
        sign = "+"
    else:
        color = "red"
        sign = ""
    return html.Div([
                    dbc.Label(name, style = {"color": "white", "fontSize": "2vh", "margin-left": "2vw"}),
                    html.P(f"{sign}{round(net_change,2)}",
                            style={'fontSize': '2.2hvh', "color": color, "margin-left": "2vw",
                            "font-family": "arial"})
                ], style = {"display": "flex", "flex-direction": "column"})
