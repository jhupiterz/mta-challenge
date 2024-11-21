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

def format_number(num):
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"  # Format in millions
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.1f}k"  # Format in thousands
    else:
        return str(num)

def generate_net_change(figure, trace):
    name = figure['data'][trace]['legendgroup']
    current_y_data = figure['data'][trace]['y'][-1]
    previous_y_data = figure['data'][trace]['y'][-2]
    net_change = current_y_data - previous_y_data
    if net_change > 0:
        color = "#2d4964"
        sign = "+"
    else:
        color = "red"
        sign = ""
    return html.Div([
                    dbc.Label(name, style = {"color": "black", "fontSize": "2vh", "margin-left": "2vw"}),
                    html.P(f"{sign}{format_number(net_change)}",
                            style={'fontSize': '2.2hvh', "color": color, "margin-left": "2vw",
                            "font-family": "arial"})
                ], style = {"display": "flex", "flex-direction": "column"})

def get_data_dictionary():
    #print("GENERATING DATA DICTIONARY")
    df = pd.read_csv("data/MTA_Daily_Ridership.csv")
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index("Date")

    df_ridership = df.iloc[:, [0, 2, 4, 6, 8, 10, 12]]
    df_ridership.columns = [x.replace(": Total Estimated Ridership", "") for x in df_ridership.columns]
    df_ridership.columns = [x.replace(": Total Scheduled Trips", "") for x in df_ridership.columns]
    df_ridership.columns = [x.replace(": Total Traffic", "") for x in df_ridership.columns]

    df_percent = df.iloc[:, [1, 3, 5, 7, 9, 11, 13]]
    df_percent.columns = [x.replace(": % of Comparable Pre-Pandemic Day", "") for x in df_percent.columns]
    

    df_monthly_ridership = df_ridership.groupby(pd.Grouper(freq='ME')).sum()
    df_monthly_percent = df_percent.groupby(pd.Grouper(freq='ME')).mean()

    df_weekly_ridership = df_ridership.groupby(pd.Grouper(freq='W-MON')).sum()
    df_weekly_percent = df_percent.groupby(pd.Grouper(freq='W-MON')).mean()

    # Build df for animation plot
    df_animation_monthly_ridership = create_df_for_animation(df_monthly_ridership)
    df_animation_weekly_ridership = create_df_for_animation(df_weekly_ridership)

    df_animation_monthly_percent = create_df_for_animation(df_monthly_percent)
    df_animation_weekly_percent = create_df_for_animation(df_weekly_percent)
    #print("DONE GENERATING DATA DICT")
    return {"df": df,
            "df_ridership": df_ridership,
            "df_percent": df_percent,
            "df_monthly_ridership": df_monthly_ridership,
            "df_monthly_percent": df_monthly_percent,
            "df_weekly_ridership": df_weekly_ridership,
            "df_weekly_percent": df_weekly_percent,
            "df_animation_monthly_ridership": df_animation_monthly_ridership,
            "df_animation_weekly_ridership": df_animation_weekly_ridership,
            "df_animation_monthly_percent": df_animation_monthly_percent,
            "df_animation_weekly_percent": df_animation_weekly_percent}
