import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os # Needed to import pages

# --- CONFIGURATION ---
# Use a dark, bold theme for Dash Bootstrap
EXTERNAL_STYLESHEETS = [dbc.themes.SLATE] 

# Initialize the Dash App
# use_pages=True enables the multi-page functionality
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, use_pages=True, suppress_callback_exceptions=True)

# Define custom styles for the aggressive cyber theme
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#1f2937", 
    "border-right": "4px solid #06b6d4",
    "box-shadow": "5px 0 15px rgba(6, 182, 212, 0.2)",
}

CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#0b0f15", # Match body background
}

NEON_TEXT_STYLE = {'color': '#22d3ee', 'text-shadow': '0 0 5px #06b6d4, 0 0 10px #06b6d4'}

# --- LAYOUT COMPONENTS ---

sidebar = html.Div(
    [
        # Header/Logo
        html.Hr(style={"border-color": "#d946ef"}), # Fuchsia separator

        
        # Navigation Links
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(["LIVE SESSION DASHBOARD"], className="ms-2 font-mono text-lg"), 
                    href="/", active="exact", className="neon-text"
                ),
                dbc.NavLink(
                    html.Div(["HISTORICAL ANALYTICS"], className="ms-2 font-mono text-lg"), 
                    href="/analytics", active="exact", className="neon-text"
                ),
            ],
            vertical=True,
            pills=True,
            className="mt-5",
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    id="page-content", 
    style=CONTENT_STYLE,
    children=dash.page_container # This is where the page content will be injected
)

# --- APP LAYOUT ---
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# --- RUN THE APP ---
if __name__ == '__main__':
    # Fix for obsolete run_server
    app.run(debug=True)
