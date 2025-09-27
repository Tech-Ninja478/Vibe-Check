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
    "background-color": "#111827", # Deeper dark background for contrast
    "border-right": "4px solid #06b6d4",
    "box-shadow": "5px 0 15px rgba(6, 182, 212, 0.4)", # Cyan Shadow
    "overflowY": "auto",
}

CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#0b0f15", # Match body background
}

NEON_TEXT_STYLE = {'color': '#22d3ee', 'text-shadow': '0 0 5px #06b6d4, 0 0 10px #06b6d4'}
FUCHSIA_TEXT_STYLE = {'color': '#ec4899', 'text-shadow': '0 0 5px #d946ef, 0 0 10px #d946ef'}

# --- LAYOUT COMPONENTS ---

sidebar = html.Div(
    [
        # HEADER
        html.H2('VIBE CHECK OS', className='text-3xl font-extrabold mb-8 pt-4 pb-4 text-center border-b-4 border-[#06b6d4]', style=NEON_TEXT_STYLE),
        html.Hr(style={"border-color": "#d946ef"}), # Fuchsia separator
        
        # NAVIGATION LINKS (Dynamically generated for all pages)
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div([page['name']], className="ms-2 font-mono text-lg"), 
                    href=page['path'], 
                    active="exact", 
                    # Apply custom link styling to override default dbc styles
                    style={
                        'color': '#22d3ee', 
                        'text-shadow': '0 0 5px #06b6d4',
                        'margin-bottom': '1rem',
                        'border': '1px solid #06b6d4',
                        'border-radius': '0.5rem',
                        'transition': 'all 0.3s ease',
                        'background-color': 'rgba(6, 182, 212, 0.05)',
                    },
                    className="hover:bg-cyan-900/40"
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="mt-5 mb-5",
        ),

        html.Hr(style={"border-color": "#374151"}), # Darker separator

        # STATUS INDICATORS
        html.H3('SYSTEM STATUS', className='text-md font-bold mb-4 mt-4', style=FUCHSIA_TEXT_STYLE),

        # Status Grid (Using dbc.Row and dbc.Col for a responsive grid)
        html.Div([
            # 1. GPU TEMP
            html.Div([
                html.P('GPU TEMP', className='text-xs text-gray-400 mb-1'),
                html.P('72°C', className='text-xl font-mono text-fuchsia-300', style={'text-shadow': '0 0 4px #c026d3'}),
                html.Span('WARNING', className='text-[10px] bg-fuchsia-900/50 text-fuchsia-300 px-1 rounded')
            ], className='p-3 rounded-lg border border-fuchsia-700 shadow-lg shadow-fuchsia-900/50 mb-3 bg-gray-900'),

            # 2. DATA STREAM
            html.Div([
                html.P('DATA STREAM', className='text-xs text-gray-400 mb-1'),
                html.P('ACTIVE', className='text-xl font-mono text-emerald-300', style={'text-shadow': '0 0 4px #047857'}),
                html.Span('LIVE', className='text-[10px] bg-emerald-900/50 text-emerald-300 px-1 rounded')
            ], className='p-3 rounded-lg border border-emerald-700 shadow-lg shadow-emerald-900/50 mb-3 bg-gray-900'),
            
            # 3. ML MODULE
            html.Div([
                html.P('ML MODULE', className='text-xs text-gray-400 mb-1'),
                html.P('LOADED', className='text-xl font-mono text-cyan-300', style={'text-shadow': '0 0 4px #06b6d4'}),
                html.Span('OK', className='text-[10px] bg-cyan-900/50 text-cyan-300 px-1 rounded')
            ], className='p-3 rounded-lg border border-cyan-700 shadow-lg shadow-cyan-900/50 mb-5 bg-gray-900'),

        ], className='d-grid gap-3'),

        # ADMIN BUTTON
        dbc.Button(
            "ADMIN OVERRIDE", 
            id="admin-button", 
            color="primary", 
            className="w-100 text-lg font-mono", # Use w-100 for full width in Bootstrap
            style={
                'background-color': '#0f172a', 
                'color': '#ec4899', 
                'border': '1px solid #d946ef', 
                'box-shadow': '0 0 8px #d946ef, 0 0 15px #d946ef', # Double shadow for maximum glow
                'font-weight': 'bold', 
                'padding': '8px', 
                'border-radius': '0.5rem', 
                'transition': 'all 0.3s ease'
            }
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
