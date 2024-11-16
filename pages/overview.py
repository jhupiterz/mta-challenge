import dash
from dash import html

dash.register_page(__name__, path='/overview')

layout = html.Div([
    "Overview page"
])
