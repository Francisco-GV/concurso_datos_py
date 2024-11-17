import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

dash.register_page(__name__, title="Inicio", path="/", name="Inicio", h1_title="General", icon="house")

layout = html.Div([
])
