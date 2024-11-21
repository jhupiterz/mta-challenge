import dash
import pandas as pd
import utils
import plots
from dash import html, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache

app = dash.get_app()

cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    })

dash.register_page(__name__, path='/animation')

radioitems_variable = html.Div(
    [
        dbc.Label("Ridership", style = {"color": "black", "fontSize": "2.5vh"}),
        dbc.RadioItems(
            options=[
                {"label": "Total", "value": 1},
                {"label": "Relative", "value": 2},
            ],
            value=1,
            id="variable",
            style = {"color": "black", "margin-right": "2vw", "fontSize": "2vh", "margin-top": "1.5vh"}
        ),
    ], style = {"background-color": "#e9f7e3", "padding": "0.5vw"}
)

radioitems_frequence = html.Div(
    [
        dbc.Label("Frequency", style = {"color": "black", "fontSize": "2.5vh"}),
        dbc.RadioItems(
            options=[
                {"label": "Monthly", "value": 1},
                {"label": "Weekly", "value": 2},
            ],
            value=2,
            id="frequency",
            style = {"color": "black", "fontSize": "2vh", "margin-top": "1.5vh"}
        ),
    ], style = {"background-color": "#e9f7e3", "padding": "0.5vw"}
)

layout = html.Div([
    html.Div([
        radioitems_variable, radioitems_frequence,
        html.Div(id='y-data-tracker', style={"background-color": "#e9f7e3", "margin-left": "3vw", "justify-content": "flex-start", "width": "67vw"}),
        dcc.Interval(id='interval-component', interval=250, n_intervals=0)
    ], style = {"display": "flex", "flex-direction": "row",
                "justify-content": "flex-start", "margin": "5vw",
                "margin-top": "4vh", "margin-bottom": "2vh"}),
    #openai_input
    dcc.Loading(id = "loading-icon", 
                children = 
                html.Div([
                        dcc.Graph(id = "animation", responsive=True,
                                  style = {"height": "65vh", "width": "85vw",  "margin": "5vw", "margin-top": "2vh", "margin-right": "2vh"}),
                    ], style = {"display": "flex", "flex-direction": "row"}))
    

], style = {"height": "100vh" ,"margin-bottom": "0px", "background-color": "#111111"})

# Cache the data loading function
@cache.memoize()
def load_large_dataset():
    data_dictionary = utils.get_data_dictionary()
    # Load and preprocess your large dataset
    return {
        "figure_weekly_ridership": plots.create_animation(data_dictionary["df_animation_weekly_ridership"], 1),
        "figure_monthly_ridership": plots.create_animation(data_dictionary["df_animation_monthly_ridership"], 1),
        "figure_weekly_percent": plots.create_animation(data_dictionary["df_animation_weekly_percent"], 2),
        "figure_monthly_percent": plots.create_animation(data_dictionary["df_animation_monthly_percent"], 2)
    }

figures = load_large_dataset()

@callback(Output('animation', 'figure'),
          Input('variable', 'value'),
          Input('frequency', 'value'))
def render_tab_content(variable, frequency):
    if variable == 1:
        if frequency == 1:
            return figures["figure_monthly_ridership"]
        else:
            return figures["figure_weekly_ridership"]
    else:
        if frequency == 1:
            return figures["figure_monthly_percent"]
        else:
            return figures["figure_weekly_percent"]

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
        
        dbc.Label(f"Date: {current_date}", style = {"color": "black", "fontSize": "3.5vh", "margin-left": "2vw"}),
        html.Div(
            net_changes_div
            , style = {"display": "flex", "flex-direction": "row"})
            
        ]