import dash
import pandas as pd
import plots
import utils
from dash import html, callback, Input, Output, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# Import data
df = pd.read_csv("data/MTA_Daily_Ridership.csv")
df.Date = pd.to_datetime(df.Date)
df = df.set_index("Date")

df_ridership = df.iloc[:, [0, 2, 4, 6, 8, 10, 12]]
df_percent = df.iloc[:, [1, 3, 5, 7, 9, 11, 13]]

df_monthly_ridership = df_ridership.groupby(pd.Grouper(freq='M')).sum()
df_monthly_percent = df_percent.groupby(pd.Grouper(freq='M')).mean()

df_weekly_ridership = df_ridership.groupby(pd.Grouper(freq='W-MON')).sum()
df_weekly_percent = df_percent.groupby(pd.Grouper(freq='W-MON')).mean()

# Build df for animation plot
df_animation_monthly_ridership = utils.create_df_for_animation(df_monthly_ridership)
df_animation_weekly_ridership = utils.create_df_for_animation(df_weekly_ridership)

df_animation_monthly_percent = utils.create_df_for_animation(df_monthly_percent)
df_animation_weekly_percent = utils.create_df_for_animation(df_weekly_percent)

radioitems_variable = html.Div(
    [
        dbc.Label("Variable", style = {"color": "white", "fontSize": "3vh"}),
        dbc.RadioItems(
            options=[
                {"label": "Total ridership", "value": 1},
                {"label": "Relative ridership", "value": 2},
            ],
            value=1,
            id="variable",
            style = {"color": "white", "margin-right": "2vw"}
        ),
    ]
)

radioitems_frequence = html.Div(
    [
        dbc.Label("Frequency", style = {"color": "white", "fontSize": "3vh"}),
        dbc.RadioItems(
            options=[
                {"label": "Monthly", "value": 1},
                {"label": "Weekly", "value": 2},
            ],
            value=2,
            id="frequency",
            style = {"color": "white"}
        ),
    ]
)

layout = html.Div([
    html.Div([
        radioitems_variable, radioitems_frequence,
        html.Div(id='y-data-tracker'),
        dcc.Interval(id='interval-component', interval=500, n_intervals=0)
    ], style = {"display": "flex", "flex-direction": "row",
                "justify-content": "flex-start", "margin": "5vw",
                "margin-top": "4vh", "margin-bottom": "2vh"}),
    #openai_input
    html.Div([
        dcc.Graph(id = "animation", responsive=True, style = {"height": "70vh", "width": "90vw",  "margin": "5vw", "margin-top": "2vh", "margin-right": "2vh"}),
    ], style = {"display": "flex", "flex-direction": "row"}),

], style = {"height": "100vh" ,"margin-bottom": "0px", "background-color": "#111111"})

@callback(Output('animation', 'figure'),
          Input('variable', 'value'),
          Input('frequency', 'value'))
def render_tab_content(variable, frequency):
    if variable == 1:
        if frequency == "Monthly":
            df = df_animation_monthly_ridership
        else:
            df = df_animation_weekly_ridership
        df.columns = [x.split(": Total Estimated Ridership")[0] for x in df.columns]
        df.columns = [x.split(": Total Scheduled Trips")[0] for x in df.columns]
        df.columns = [x.split(": Total Traffic")[0] for x in df.columns]
    else:
        if frequency == "Monthly":
            df = df_animation_monthly_percent
        else:
            df = df_animation_weekly_percent
        df.columns = [x[0:-34] for x in df.columns]
    return plots.create_animation(df, variable)

@callback(
    Output('y-data-tracker', 'children'),
    Input('animation', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_y_data(figure, n_intervals):
    # Retrieve the y data from the last trace
    current_date = pd.Timestamp(figure['data'][0]['x'][-1]).date()
    net_changes_div = [utils.generate_net_change(figure, x) for x in range(len(figure['data']))]   
    return [
        
        dbc.Label(f"Date: {current_date}", style = {"color": "white", "fontSize": "3vh", "margin-left": "5vw"}),
        html.Div(
            net_changes_div
            , style = {"display": "flex", "flex-direction": "row", "margin-left": "3vw"})
            
        ]