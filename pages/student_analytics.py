import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Register the page, defining the URL path
dash.register_page(__name__, path='/students', name='Student Analytics')

# --- MOCK DATA FOR STUDENT ANALYTICS ---

# Generate mock data for a class of 20 students
np.random.seed(42) # for reproducibility
student_data = {
    'Student_ID': [f'L-{i:02d}' for i in range(1, 21)],
    'Vibe_Score': np.random.randint(40, 95, 20),
    'Sessions_Attended': np.random.randint(5, 15, 20),
    'Alert_Count': np.random.randint(0, 5, 20)
}
df_students = pd.DataFrame(student_data)

# Mock historical data for a selected student
def get_historical_data(student_id):
    days = 10
    return pd.DataFrame({
        'Date': pd.to_datetime(pd.date_range('2025-09-01', periods=days, freq='D')),
        'Vibe_Score': np.random.randint(55, 95, days)
    })

# --- STYLING COMPONENTS (Consistent with the Cyber Theme) ---

CYBER_CARD_STYLE = {
    'background-color': '#1f2937',
    'border': '2px solid #374151', 
    'border-radius': '0.75rem',
    'padding': '1.5rem',
    'box-shadow': '0 0 15px rgba(6, 182, 212, 0.4)',
    'height': '100%',
}
NEON_TEXT_STYLE = {'color': '#22d3ee', 'text-shadow': '0 0 5px #06b6d4, 0 0 10px #06b6d4'}

# --- TABLE STYLING FOR ALIGNMENT AND SEGREGATION ---

TABLE_STYLE_HEADER = {
    'backgroundColor': '#0b0f15',
    'color': '#22d3ee',
    'fontWeight': 'bold',
    'borderBottom': '3px solid #06b6d4',
    'fontFamily': 'monospace',
    'textAlign': 'center', # Center header text
    'padding': '12px 6px',
}

TABLE_STYLE_DATA = {
    'backgroundColor': '#1f2937',
    'color': '#e5e7eb',
    'borderBottom': '1px solid #374151',
    'fontFamily': 'monospace',
    'textAlign': 'center', # Center data text
    'padding': '12px 6px',
}

# Ensure all columns are centered and evenly spaced
TABLE_STYLE_CELL = {
    'textAlign': 'center', 
    'padding': '8px 4px', # Reduced padding to fit better
    'minWidth': '90px', 'width': 'auto', 'maxWidth': '150px',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
}


# --- PAGE LAYOUT ---

layout = html.Div([
    dbc.Row([
        # Main Title Header
        dbc.Col(
            html.H1('INDIVIDUAL LEARNER ANALYTICS // TARGETED INTERVENTION', 
                    className="text-4xl font-extrabold mb-8 pb-4 border-b-4 border-gray-700", 
                    style=NEON_TEXT_STYLE),
            width=12
        ),
    ]),

    # Main content row with a table and a graph
    dbc.Row([
        # COLUMN 1: Student List Table (Slightly narrower for better fit)
        dbc.Col([
            dbc.Card([
                html.H3('VIBE SCORES // CLASS RUNDOWN', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('Click a student ID to view their historical progress. Low scores are highlighted.', className='text-gray-400 mb-4'),
                dash_table.DataTable(
                    id='student-table',
                    columns=[{"name": i.replace('_', ' ').title(), "id": i} for i in df_students.columns],
                    data=df_students.to_dict('records'),
                    
                    # Apply improved styles
                    style_header=TABLE_STYLE_HEADER,
                    style_data=TABLE_STYLE_DATA,
                    style_cell=TABLE_STYLE_CELL,

                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Vibe_Score} <= 60'},
                            'backgroundColor': '#632b2b', 'color': '#f87171', 'fontWeight': 'bold'
                        },
                        {
                            'if': {'filter_query': '{Vibe_Score} > 60 && {Vibe_Score} <= 75'},
                            'backgroundColor': '#625b29', 'color': '#fde047'
                        }
                    ],
                    row_selectable='single',
                    selected_rows=[],
                    sort_action='native',
                    filter_action='native',
                    style_table={'overflowX': 'auto'} # Allows horizontal scroll if necessary, preventing overflow
                )
            ], style={**CYBER_CARD_STYLE}),
        ], md=5, className="mb-4"),
        
        # COLUMN 2: Historical Progress Graph
        dbc.Col([
            dbc.Card([
                html.H3(id='student-graph-title', children='HISTORICAL TRENDS // SELECT STUDENT', className='text-xl font-bold mb-3', style=NEON_TEXT_STYLE),
                html.P('View the Vibe Score trend for the selected learner.', className='text-gray-400 mb-4'),
                dcc.Graph(id='student-historical-graph', style={'height': '450px'}),
            ], style={**CYBER_CARD_STYLE}),
        ], md=7, className="mb-4"),
    ]),
])

# --- CALLBACKS ---

@dash.callback(
    Output('student-historical-graph', 'figure'),
    Output('student-graph-title', 'children'),
    Input('student-table', 'selected_rows')
)
def update_graph_on_click(selected_rows):
    if not selected_rows:
        # Default state with no student selected
        fig = go.Figure()
        fig.add_annotation(
            text="[AWAITING LEARNER SELECTION]",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False,
            font={'size': 18, 'color': '#ec4899', 'family': 'monospace'}
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#111827',
            plot_bgcolor='#111827',
            xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
            yaxis={'showgrid': False, 'zeroline': False, 'visible': False},
        )
        title = 'HISTORICAL TRENDS // SELECT STUDENT'
        return fig, title
    
    # Get the selected student's ID
    selected_id = df_students.iloc[selected_rows[0]]['Student_ID']
    
    # Generate historical data for the selected student
    historical_df = get_historical_data(selected_id)
    
    # Create the plot
    fig = go.Figure(
        data=go.Scatter(
            x=historical_df['Date'],
            y=historical_df['Vibe_Score'],
            mode='lines+markers',
            line={'color': '#22d3ee', 'width': 4},
            marker={'size': 10, 'color': '#22d3ee'}
        )
    )
    
    # Update layout to match the cyber theme
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        title={'text': f'VIBE SCORE HISTORY // {selected_id}', 'font': {'color': '#e5e7eb'}},
        xaxis={'title': 'Date', 'showgrid': False},
        yaxis={'title': 'Vibe Score', 'range': [0, 100]}
    )
    
    title = f'HISTORICAL TRENDS // {selected_id}'
    return fig, title
