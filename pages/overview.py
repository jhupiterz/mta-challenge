import dash
import plots
import pandas as pd
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv("data/MTA_Daily_Ridership.csv")
df.Date = pd.to_datetime(df.Date)
df = df.set_index("Date")

df_ridership = df.iloc[:, [0, 2, 4, 6, 8, 10, 12]]
df_ridership.columns = [x.replace(": Total Estimated Ridership", "") for x in df_ridership.columns]
df_ridership.columns = [x.replace(": Total Scheduled Trips", "") for x in df_ridership.columns]
df_ridership.columns = [x.replace(": Total Traffic", "") for x in df_ridership.columns]
df_ridership_precovid = df_ridership[df_ridership.index < pd.Timestamp("2020-03-11")]
df_ridership_postcovid = df_ridership[df_ridership.index > pd.Timestamp("2020-03-11")]

melted_data = df.reset_index().melt(
    id_vars='Date',
    value_vars=[
        'Subways: Total Estimated Ridership',
        'Buses: Total Estimated Ridership',
        'LIRR: Total Estimated Ridership',
        'Metro-North: Total Estimated Ridership',
        'Access-A-Ride: Total Scheduled Trips',
        'Bridges and Tunnels: Total Traffic',
        'Staten Island Railway: Total Estimated Ridership'
    ],
    var_name='Service',
    value_name='Ridership'
)

melted_data.Service = [x.replace(": Total Scheduled Trips", "") for x in melted_data.Service]
melted_data.Service = [x.replace(": Total Estimated Ridership", "") for x in melted_data.Service]
melted_data.Service = [x.replace(": Total Traffic", "") for x in melted_data.Service]

dash.register_page(__name__, path='/')

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Total ridership", className="card-1", style = {"text-align": "center"}),
            html.P("7.93 B", style={"font-size": "4vh", "text-align": "center", "font-family": "arial"})
        ]
    ), style={"width": "17vw", "background-color": "#e9f7e3", "border-radius": "0px"}
)

second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Avg. Recovery Rate", className="card-2", style = {"text-align": "center"}),
            html.P("61.5 %", style={"font-size": "4vh", "text-align": "center", "font-family": "arial"})
        ]
    ), style={"width": "17vw", "background-color": "#e9f7e3", "border-radius": "0px"}
)

radio_items = dcc.RadioItems(['2020', '2021','2022', '2023', '2024'], '2020',
                             id = "year-selection",
                             inline=True, style = {"color": "white"}, labelStyle={"marginLeft": "10px"})

layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Year", style = {"color": "white"}),
            radio_items,
        ], style = {"display": "flex", "flex-direction": "row", "align-items": "center", "margin-left": "-4vw", "margin-top": "2vh"}),
        dcc.Graph(id = "heatmap",
                style={"padding": "0", "margin":"0", "margin-left": "4vw", "margin-top": "0vh", "height": "42vh", "width": "50vw", "z-index": "0"}, responsive=True),
        dcc.Graph(id = "bargraph",
                style = {"margin-left": "5.5vw", "margin-top": "2vh", "width": "45vw", "height": "35vh", "z-index": "100"})
    ], style = {"display": "flex", "flex-direction": "column", "align-items": "center"}),
    html.Div([
        html.Div([
            first_card,
            second_card
        ], style = {"display": "flex", "flex-direction": "row", "justify-content": "space-between"}),
        html.Div([
            dcc.Graph(id="quarter-timeseries", figure = plots.create_time_series_per_quarter(df_ridership, service_filter="Subways"),
                  style = {"margin-top": "3vh", "height":"25vh", "width": "112%", "margin-left": "-2vw"}, responsive=True)
        ], style = {"align-items": "center", "width": "37vw"}), 
        html.Div([
            dcc.Graph(id = "donuts", style = {"margin-top": "3vh", "height":"30vh"}, responsive=True),
        ], style = {"margin-top": "3vh"})  
    ],style = {"display": "flex", "flex-direction": "column", "margin-right": "5vw", "margin-top": "5vh", "margin-left": "5vw"})
], style = {"display": "flex", "flex-direction": "row"})

@callback(Output("heatmap", "figure"),
          Input("year-selection", "value"))
def generate_heatmap(year):
    figure = plots.create_calendar_heatmap(df, year)
    return figure

@callback(Output("bargraph", "figure"),
          Input("year-selection", "value"))
def generate_heatmap(year):
    figure = plots.create_bar_graph(df_ridership_precovid,
                                    df_ridership_postcovid, year)
    return figure

@callback(Output("donuts", "figure"),
          Input("year-selection", "value"))
def generate_heatmap(year):
    figure = plots.create_donut_charts(df_ridership, year)
    return figure
