import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale
import numpy as np
import pandas as pd

def create_animation(df, variable):
    # plotly figure
    df.columns = [*df.columns[:-1], 'frame']
    fig = px.area(df, x = df.index, y = df.columns,
                  template="plotly_dark",
                  animation_frame='frame',
                  line_shape='spline',
                  width=1000, height=600)
    fig.update_traces(fill='none')
    
    if variable == 2:
        legend_title = ''
        yaxis_title = "Percent [%]"
    else:
        legend_title = ""
        yaxis_title = "Number of riders"

    # attribute adjusments
    fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True
    #fig.layout.updatemenus[0].buttons[0]['args'][1]['transition']['duration'] = 120
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 250
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
    fig.add_vline(x=pd.Timestamp('2020-03-11'), line_width=2, line_dash="dash", line_color="yellow")
    fig.add_annotation(x=pd.Timestamp('2020-03-11'), y=3000000,
            text="WHO declares global pandemic",
            showarrow=False,
            font=dict(
            size=12,
            color="yellow"
            ),
            textangle=-90,
            xshift=10)
    fig.update_xaxes(range = (pd.Timestamp('2019-12-01'), pd.Timestamp('2024-10-31')))
    fig.update_yaxes(range = (0, 5500000))
    fig.update_layout(width = 1000, height = 900,
                      font=dict(size=18), margin={"r":0,"t":0,"l":0,"b":0},
                      legend_title_text="",
                      legend=dict(
                                yanchor="top",
                                y=0.99,
                                xanchor="right",
                                x=0.99
                            ))
    return fig

def create_treemap_chart(df):
    fig = px.treemap(df, path=[px.Constant("MTA services"), 'Service'], values='Ridership',
                  color='Ridership',
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['Ridership']))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    return fig

def create_calendar_heatmap(df):
    data = df.reset_index()
    # Creating a pivot table for ridership data
    pivot_table = data.pivot_table(
        index=data['Date'].dt.month,  # Y-axis: months
        columns=data['Date'].dt.day,  # X-axis: days
        values='Subways: Total Estimated Ridership',  # Ridership values
        aggfunc='sum'
    )

    # Create heatmap
    fig = px.imshow(pivot_table,
                    labels=dict(x="Day", y="Month", color="Ridership"),
                    x=pivot_table.columns,
                    y=pivot_table.index,
                    color_continuous_scale='GnBu')

    fig.update_layout(
        xaxis=dict(
        title='',
        scaleanchor=None  # Ensures tiles can stretch independently
            ),
        yaxis = dict(
            title = "",
        tickvals = [1,2,3,4,5,6,7,8,9,10,11,12],
        ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        ), margin=dict(l=0, r=0, b=0, t=0),
        template = "plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar=dict(
                    thicknessmode="fraction", thickness=0.05,
                    lenmode="fraction", len=1.1))
    return fig

def create_bar_graph(df_precovid, df_postcovid):
    df_precovid = df_precovid.mean().sort_values(ascending=False)
    df_postcovid = df_postcovid.mean().sort_values(ascending=False)
    fig = go.Figure(data=[
    go.Bar(name='Pre-COVID', x=df_precovid.index, y=df_precovid, text=df_precovid, textposition="auto", marker=dict(color='#aee0b8')),
    go.Bar(name='Post-COVID', x=df_postcovid.index, y=df_postcovid, text=df_postcovid, textposition="auto", marker=dict(color='#096cae'))
    ])
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    # Change the bar mode
    # Customize x-axis tick labels
    # Add Annotations for X Labels Above Bars
    annotations = [
        dict(
            x=df_precovid.index[i], 
            y=df_precovid[i] + 1,  # Position above the bars (adjust as needed)
            text=df_precovid.index[i],
            showarrow=False,
            font=dict(size=16, color="white"),
            xanchor="center",
            yanchor="bottom",
            textangle=-90
        ) 
        for i in range(len(df_precovid.index))
    ]

    # Update Layout with Annotations
    fig.update_layout(
        annotations=annotations,
        xaxis=dict(showticklabels=False)# Optional Y-axis title
    )
    fig.update_layout(barmode='group', template = "plotly_dark", margin=dict(l=0, r=0, b=0, t=0),
                      legend = dict(orientation = "h",
                                    yanchor="top",
                                    y=1,
                                    xanchor="right",
                                    x=1))
    fig.update_yaxes(visible=False)
    return fig

def create_time_series_per_quarter(df_ridership, service_filter):
    df_ridership = df_ridership.reset_index()
    df = df_ridership.groupby(df_ridership['Date'].dt.to_period('Q'))[[service_filter]].sum()
    fig = px.line(x=df.index.to_series().astype(str), y=df[service_filter], template="plotly_dark", markers=True)
    fig.update_traces(
    marker=dict(symbol="circle", size=10, color="red"),  # Marker customization
    line=dict(color="yellow", width=2)  # Line customization
)
    fig.add_vline(x="2020Q1", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2020Q4", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2021Q1", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2021Q4", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2022Q1", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2022Q4", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2023Q1", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2023Q4", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2024Q1", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_vline(x="2024Q4", line_width=2, line_dash="dash", line_color="#aee0b8")
    fig.add_annotation(x="2020Q2", y=335000000,
            text="2020",
            showarrow=False,
            xanchor="left",
            yshift=0)
    fig.add_annotation(x="2021Q2", y=335000000,
            text="2021",
            showarrow=False,
            xanchor="left",
            yshift=0)
    fig.add_annotation(x="2022Q2", y=335000000,
            text="2022",
            showarrow=False,
            xanchor="left",
            yshift=0)
    fig.add_annotation(x="2023Q2", y=335000000,
            text="2023",
            showarrow=False,
            xanchor="left",
            yshift=0)
    fig.add_annotation(x="2024Q2", y=335000000,
            text="2024",
            showarrow=False,
            xanchor="left",
            yshift=0)
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),
                      xaxis = dict(
                        tickvals = df.index.to_series().astype(str),
                        ticktext = ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4']
                        ))
    fig.update_xaxes(title="")
    fig.update_yaxes(title="", visible=False, range = (0, 350000000))
    return fig

def create_donut_charts(df_ridership):
    labels = df_ridership.sum().index
    values = df_ridership.sum().values
    colors = sample_colorscale("GnBu", [v / max(values) for v in values])
    
    fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    row_heights=[0.5],
    specs=[[ {"type": "pie"}, {"type": "pie"}]],
    subplot_titles=["Service on weekdays", "Service on weekends"])

    fig.add_trace(go.Pie(
        labels=labels, 
        values=values,
        marker=dict(colors=colors),
        hole = 0.6,
        legendgroup="group",
        textinfo = "percent+label",
        textposition='inside'), 
        row=1, col=1)

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole = 0.6,
        legendgroup="group",
        textinfo = "percent+label",
        textposition='inside'), 
        row=1, col=2)

    fig.update_layout(margin = dict(t=30, l=0, r=0, b=0), template = "plotly_dark",
                      legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=0.5
                ), showlegend = False)
    return fig