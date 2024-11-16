import plotly.express as px

def create_animation(df, variable):
    # plotly figure
    df.columns = [*df.columns[:-1], 'frame']
    fig = px.area(df, x = df.index, y = df.columns,
                  template="plotly_dark",
                  animation_frame='frame',
                  line_shape='spline',
                  width=1000, height=600)
    
    if variable == 2:
        legend_title = ''
        yaxis_title = "Percent [%]"
    else:
        legend_title = ""
        yaxis_title = "Number of riders"

    # attribute adjusments
    fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True
    #fig.layout.updatemenus[0].buttons[0]['args'][1]['transition']['duration'] = 120
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    fig.update_yaxes(title= yaxis_title)
    fig.update_xaxes(title = "", range = [df.index.min(), df.index.max()])
    fig.update_layout(width = 1000, height = 900, legend = dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99, font = dict(size = 16, color = "white")),
                      legend_title_text= legend_title,
                      font=dict(size=18), margin={"r":0,"t":0,"l":0,"b":0},
                      legend_title = dict(font = dict(size = 18, color = "white")))
    return fig

def create_daily_timeseries(df):
    fig = px.line(data_frame=df,
                  x="Date", y="Ridership", color = "Service", template="plotly_dark")
    fig.update_layout(width = 1000, height = 900,
                      font=dict(size=18), margin={"r":0,"t":0,"l":0,"b":0},
                      legend_title_text="",
                      legend=dict(
                                yanchor="top",
                                y=0.99,
                                xanchor="left",
                                x=0.01
                            ))
    return fig