import dash
from dash import html
import dash_bootstrap_components as dbc

# Create app ---------------------------------------------------------------
app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    use_pages= True,
    external_stylesheets=[dbc.themes.LITERA, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

server = app.server
app.title = "MTA Data App"

app.layout = html.Div([
        html.Header([
        html.H1("MTA Pre- vs. Post-pandemic Data", style = {"color": "white", "text-align": "center"}),
        html.Div([
            html.A("Overview", href = "/overview", style = {"color": "white", "margin-right": "2vw"}),
            html.A("Animation", href = "/", style = {"color": "white", "margin-right": "2vw"}),
            html.A("ChatGPT Insights", href = "/insights", style = {"color": "white"})
        ], style = {"display": "flex", "flex-direction": "row", "align-items": "center", "justify-content": "flex-end"}),
    ], style = {"display": "flex", "flex-direction": "row", "align-items": "center", "justify-content": "space-between",
                "margin-left": "5vw", "margin-right": "5vw"}),
    dash.page_container
], style = {"height": "100vh", "background-color": "#111111"})

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)