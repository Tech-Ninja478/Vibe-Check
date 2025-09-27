import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Register the page, defining the URL path
dash.register_page(__name__, path='/analytics', name='Historical Analytics')

# --- MOCK DATA FOR INTERACTIVITY ---
# Mock data for Curriculum Map Dropdown
MODULES = ['Module 1: Foundations', 'Module 2: Advanced Wiring', 'Module 3: Project Integration', 'Module 4: Safety & Protocol']
# Mock data for Attendance Table
attendance_data = {
    'Session_ID': ['S-001', 'S-002', 'S-003', 'S-004'],
    'Date': ['2025-09-20', '2025-09-21', '2025-09-22', '2025-09-23'],
    'Total_Present': [19, 20, 18, 19],
    'Learner_ID_Missing': ['L-07', 'None', 'L-01, L-09', 'L-03']
}
df_attendance = pd.DataFrame(attendance_data)
df_attendance.index.name = 'Index'

# --- STYLING (Enhanced for extreme cyber look) ---
CYBER_CARD_STYLE = {
    'background-color': '#1f2937', # Dark Card Base
    'border': '2px solid #374151', 
    'border-radius': '0.75rem',
    'padding': '1.5rem',
    'box-shadow': '0 0 15px rgba(6, 182, 212, 0.4)', # Stronger Cyan Glow
    'height': '100%',
    'position': 'relative',
}
NEON_TEXT_STYLE = {'color': '#22d3ee', 'text-shadow': '0 0 5px #06b6d4, 0 0 10px #06b6d4'}
FUCHSIA_TEXT_STYLE = {'color': '#ec4899', 'text-shadow': '0 0 5px #d946ef, 0 0 10px #d946ef'}

# Custom style for embedded components to match dark theme
CYBER_EMBEDDED_STYLE = {
    'background-color': '#111827', 
    'border': '1px solid #1f2937', 
    'padding': '1rem', 
    'border-radius': '0.5rem'
}

# --- COMPONENTS ---

def create_attendance_table(df):
    """Creates a Dash DataTable for attendance logs with cyber theme styling."""
    return dash_table.DataTable(
        id='attendance-log-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_header={
            'backgroundColor': '#0b0f15', # Very dark header
            'color': '#22d3ee',
            'fontWeight': 'bold',
            'borderBottom': '3px solid #06b6d4',
            'fontFamily': 'monospace'
        },
        style_data={
            'backgroundColor': '#1f2937', # Match card background
            'color': '#e5e7eb',
            'borderBottom': '1px solid #374151',
            'fontFamily': 'monospace'
        },
        style_table={'overflowX': 'auto', 'border': 'none'},
        page_action='none',
        sort_action='native',
        filter_action='native'
    )

def create_strategy_graph_placeholder():
    """Placeholder graph for Pedagogical Strategy Comparison."""
    fig = go.Figure()
    fig.add_annotation(
        text="[SIMULATION GRID ACTIVE: LOAD STRATEGY DATA]",
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False,
        font={'size': 18, 'color': '#ec4899', 'family': 'monospace'}
    )
    fig.update_layout(
        template='plotly_dark',
        height=300,
        plot_bgcolor='#111827',
        paper_bgcolor='#1f2937',
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
        yaxis={'showgrid': False, 'zeroline': False, 'visible': False}
    )
    return fig

# --- PAGE LAYOUT ---

layout = html.Div([
    dbc.Row([
        # Main Title Header
        dbc.Col(
            html.H1('HISTORICAL ANALYTICS // STRATEGIC REPORTS', 
                    className="text-4xl font-extrabold mb-8 pb-4 border-b-4 border-gray-700", 
                    style=NEON_TEXT_STYLE),
            width=12
        ),
    ]),

    # Row 1: Curriculum Effectiveness Map & Strategy Comparison
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('CURRICULUM EFFECTIVENESS MAP', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('Select Module to view average Vibe Score and retention rate.', className='text-gray-400 mb-4'),
                html.Div([
                    dcc.Dropdown(
                        id='module-dropdown',
                        options=[{'label': i, 'value': i} for i in MODULES],
                        value=MODULES[0],
                        clearable=False,
                        style={'backgroundColor': '#111827', 'color': '#22d3ee', 'borderColor': '#06b6d4'},
                        className='mb-4'
                    ),
                    # Placeholder for the main Curriculum Bar Chart
                    html.Div(dcc.Graph(
                        figure=create_strategy_graph_placeholder(),
                        config={'displayModeBar': False}
                    ), style=CYBER_EMBEDDED_STYLE)
                ]),
            ], style=CYBER_CARD_STYLE),
        ], md=6, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                html.H3('PEDAGOGICAL STRATEGY COMPARISON', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('Compare engagement outcomes for different instructional methods.', className='text-gray-400 mb-4'),
                html.Div(dcc.Graph(
                    figure=create_strategy_graph_placeholder(), # Reusing the placeholder function
                    config={'displayModeBar': False}
                ), style=CYBER_EMBEDDED_STYLE)
            ], style=CYBER_CARD_STYLE),
        ], md=6, className="mb-4"),
    ]),

    # Row 2: Individual Learner Trends & Attendance Logs
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('INDIVIDUAL LEARNER TRENDS (Intervention Targets)', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('Identify learners with consistently low focus across sessions. Priority targets flagged in **FUCHSIA**.', className='text-gray-400 mb-4'),
                html.Div([
                    # Placeholder for Learner ID List (Simulated Scrollable Log)
                    html.Div([
                        html.Div("L-01 | Focus: 45% (LOW) | Intervention: REQUIRED", style={'color': '#ec4899', 'fontFamily': 'monospace', 'borderBottom': '1px dashed #d946ef30'}),
                        html.Div("L-07 | Focus: 58% (MARGINAL) | Intervention: SOFT ALERT", style={'color': '#fde047', 'fontFamily': 'monospace', 'borderBottom': '1px dashed #d946ef30'}),
                        html.Div("L-12 | Focus: 89% (HIGH) | Intervention: NONE", style={'color': '#4ade80', 'fontFamily': 'monospace', 'borderBottom': '1px dashed #d946ef30'}),
                        html.Div("L-09 | Focus: 51% (LOW) | Intervention: REQUIRED", style={'color': '#ec4899', 'fontFamily': 'monospace', 'borderBottom': '1px dashed #d946ef30'}),
                        html.Div("L-04 | Focus: 72% (OPTIMAL) | Intervention: NONE", style={'color': '#4ade80', 'fontFamily': 'monospace', 'borderBottom': '1px dashed #d946ef30'}),
                    ], className='space-y-3 p-4', style={'height': '220px', 'overflowY': 'auto', **CYBER_EMBEDDED_STYLE})
                ]),
            ], style=CYBER_CARD_STYLE),
        ], md=8, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                html.H3('AUTOMATED ATTENDANCE LOGS', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('Fulfilling the core requirement with objective face-recognition data.', className='text-gray-400 mb-4'),
                html.Div(create_attendance_table(df_attendance), style=CYBER_EMBEDDED_STYLE)
            ], style={**CYBER_CARD_STYLE, 'boxShadow': '0 0 15px rgba(236, 72, 153, 0.4)'}), # Fuchsia specific glow
        ], md=4, className="mb-4"),
    ])
])
