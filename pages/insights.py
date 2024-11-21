import dash
import plots
import pandas as pd
import re
import os
import openai
from dash import html, callback, Input, Output, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/insights')

# Import data
df = pd.read_csv("data/MTA_Daily_Ridership.csv")
df.Date = pd.to_datetime(df.Date)
df = df.set_index("Date")

df.columns = [x.replace(": Total Estimated Ridership", "") for x in df.columns]
df.columns = [x.replace(": Total Scheduled Trips", "") for x in df.columns]
df.columns = [x.replace(": Total Traffic", "") for x in df.columns]

melted_data = df.reset_index().melt(
    id_vars='Date',
    value_vars=[
        'Subways',
        'Buses',
        'LIRR',
        'Metro-North',
        'Access-A-Ride',
        'Bridges and Tunnels',
        'Staten Island Railway'
    ],
    var_name='Service',
    value_name='Ridership'
)

melted_data_weekdays = melted_data[melted_data.Date.dt.dayofweek < 5]
melted_data_weekends = melted_data[melted_data.Date.dt.dayofweek >= 5]

# Load environment variables from the .env file
openai.api_key = os.environ.get('OPENAI')

openai_switch = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Make me laugh", "value": 1},
            ],
            value=[],
            id="openai-funny",
            switch=True,
            style= {"color": "black"}
        ),
    ], style= {"margin-right": "3vw"}
)

openai_input = html.Div([
    html.Div([
        html.H4("MTA Ridership Analysis Assistant", style = {"color": "black", "margin-bottom": "2vh"}),
        openai_switch
    ], style = {"background-color": "#e9f7e3", "width": "35vw", "height": "12vh", "padding-left": "1.5vw"}),
    html.Div([
        html.Pre(id='response_output', style = {"color": "white", 'whiteSpace': 'pre-wrap', 'wordWrap': 'break-word'})
    ], style = {"height": "70vh", "align-items": "center"})  
], style = {"width": "35vw", "margin-right": "5vw"})

filter_switches = html.Div(
    [
        dbc.Label("Filters", style= {"color": "black", "fontSize": "3vh"}),
        dbc.Checklist(
            options=[
                {"label": "Business days only (recommended)", "value": 1},
                {"label": "Weekends only", "value": 2},
            ],
            value=[1],
            id="switches-input",
            switch=True,
            style= {"color": "black"},
            className= "switches-input"
        ),
    ], style= {"margin-right": "3vw", "margin-left": "2vw"}
)

options = []
for service in melted_data_weekdays.Service.unique():
    options.append({"label": service, "value": service})
dropdown_services = html.Div([
    dbc.Label("Services to plot", style= {"color": "white", "fontSize": "3vh", "color": "black"}),
    dbc.DropdownMenu(
        children=[
            dbc.Checklist(
            options= options,
            value=["Subways", "Buses"],
            id="checklist-input",
        )],
        style= {"width": "25vw", "color": "black"},
        label="Service(s) to plot",
    )]
)

layout = html.Div([
    html.Div([
    ], style = {"display": "flex", "flex-direction": "row",
                "justify-content": "flex-start", "margin": "5vw",
                "margin-top": "4vh", "margin-bottom": "2vh"}),
    #openai_input
    html.Div([
        html.Div([
            html.Div([
                filter_switches,
                dropdown_services,
            ], style = {"display": "flex", "flex-direction": "row", "margin-left": "5vw", "align-items": "flex-start", "background-color": "#e9f7e3"}),
            dcc.Loading(id = "loading-icon-insights",
                        children = dcc.Graph(id = "time-series" ,responsive=True, style = {"height": "70vh", "width": "50vw",  "margin": "5vw", "margin-top": "2vh", "margin-right": "2vh"})),
        ], style = {"display": "flex", "flex-direction": "column"}),

        html.Div([
            openai_input,
        ], style = {"display": "flex", "flex-direction": "column", "width": "20vw", "margin-left": "3vw"})
    ], style = {"display": "flex", "flex-direction": "row"}),

], style = {"height": "100vh" ,"margin-bottom": "0px", "background-color": "#111111"})

@callback(
        Output("time-series", "figure"),
        [Input('switches-input', 'value'),
        Input('checklist-input', 'value')]
)
def generate_timeseries(days_of_week, services):
    if days_of_week == [1]:
        df = melted_data_weekdays[melted_data_weekdays.Service.isin(services)]
    elif days_of_week == [2]:
        df = melted_data_weekends[melted_data_weekends.Service.isin(services)]
    else:
        df = melted_data[melted_data.Service.isin(services)]
    return plots.create_daily_timeseries(df)

@callback(
    Output('response_output', 'children'),
    [Input('time-series', 'hoverData'),
     Input('openai-funny', 'value')]
)
def update_output(data, make_me_laugh):
    if data:
        date = data["points"][0]["x"]
        # Make a request to OpenAI's API
        if make_me_laugh == [1]:
            query = f"Invent a hilariously sarcastic story telling why the MTA ridership might have been disrupted on {date}. Add as many funny details while keeping it concise."
            pass
        else:
            query = f"Concisely and in a numbered bullet-point list of max 4 items, identify the most probable causes for the MTA ridership to be abnormal on {date}. Indicate if on that specific date there were any major cultural/sports event, severe weather reports, COVID restrictions, public holidays, or scheduled maintenance of MTA services. Be specific."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" or any available model
            messages=[{"role": "user", "content": query}]
        )
        answer = response['choices'][0]['message']['content']
        items = re.split(r'(\d+\.\s)', answer)

        formatted_text = "".join([item if i % 2 == 0 else "\n" + item for i, item in enumerate(items) if item.strip()])
        text = f"Possible causes of ridership disruptions on {date} include:\n\n" + formatted_text
        return text
    return "Hover on a data point to get some insights from ChatGPT"
