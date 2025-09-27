import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Register the page in the multi-page framework
dash.register_page(__name__, path='/', name='Live Session Dashboard') 

# --- STYLING AND MOCK DATA ---

# Global variable to simulate a degrading Vibe Score for demonstration
# This will be replaced by your actual ML prediction output later.
MOCK_VIBE_SCORE = 95
VIBE_STATUS_MAP = {
    80: {'label': 'OPTIMAL VIBE', 'color': 'emerald-500', 'bg': 'bg-emerald-900/50'},
    65: {'label': 'WATCH LEVEL', 'color': 'yellow-500', 'bg': 'bg-yellow-900/50'},
    50: {'label': 'HIGH ALERT', 'color': 'orange-500', 'bg': 'bg-orange-900/50'},
    0: {'label': 'CRITICAL BREACH', 'color': 'red-500', 'bg': 'bg-red-900/50'},
}

# Custom Styles
CYBER_CARD_STYLE = {
    'background-color': '#1f2937',
    'border': '2px solid #374151', 
    'border-radius': '1rem',
    'padding': '1.5rem',
    'box-shadow': '0 0 15px rgba(6, 182, 212, 0.2)',
}

NEON_TEXT_STYLE = {'color': '#22d3ee', 'text-shadow': '0 0 5px #06b6d4, 0 0 10px #06b6d4'}
FUCHSIA_TEXT_STYLE = {'color': '#ec4899', 'text-shadow': '0 0 5px #d946ef, 0 0 10px #d946ef'}


# --- UTILITY: COLOR MAPPING FUNCTION ---
# This function maps a score (0-100) to a dynamic hex color.
def get_color_from_score(score):
    """Maps score (0-100) to a hex color: Green(100) -> Yellow(50) -> Red(0)"""
    score = max(0, min(100, score)) # Clamp score between 0 and 100
    
    # Invert score so 0 is red and 100 is green
    r, g, b = 0, 0, 0
    if score >= 50:
        # Green to Yellow (Score 50 to 100)
        ratio = (score - 50) / 50.0  # 0 to 1
        r = int(255 * (1 - ratio))
        g = 255
    else:
        # Yellow to Red (Score 0 to 50)
        ratio = score / 50.0  # 0 to 1
        r = 255
        g = int(255 * ratio)

    # Simple scaling for extreme cyber look (full 255 range looks better with dark background)
    return f'#{r:02x}{g:02x}00' 

# --- PLOTLY GRAPHIC FUNCTIONS (Unchanged from last version) ---

# Mock Data for Graphs
data_points = 20
time_labels = pd.date_range('10:00', periods=data_points, freq='5min').strftime('%H:%M')
df = pd.DataFrame({
    'Time': time_labels,
    'Actual_Engagement': np.random.randint(70, 95, data_points),
    'Predicted_Engagement': [None] * (data_points - 5) + list(np.random.randint(55, 80, 5))
})

def create_predictive_graph(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Time'], y=df['Actual_Engagement'], mode='lines+markers', name='ACTUAL VIBE LEVEL',
        line=dict(color='#22d3ee', width=4), marker=dict(size=8, color='#22d3ee', line=dict(width=2, color='#1f2937'))
    ))
    fig.add_trace(go.Scatter(
        x=df['Time'], y=df['Predicted_Engagement'], mode='lines', name='CRITICAL FORECAST',
        line=dict(color='#ec4899', width=3, dash='dashdot'),
    ))
    fig.update_layout(
        template='plotly_dark',
        title={'text': 'ENGAGEMENT TIMELINE: ACTUAL VS. CRITICAL FORECAST (USP)', 'x': 0.5, 'font': {'size': 20, 'color': '#e5e7eb', 'family': 'monospace'}},
        height=400, plot_bgcolor='#111827', paper_bgcolor='#1f2937', font=dict(color='#e5e7eb', family='Inter'),
        xaxis_title="Time Code", yaxis_title="VIBE LEVEL (%)", margin=dict(l=40, r=20, t=60, b=40)
    )
    return fig

def create_activity_graph():
    activity_data = {
        'Activity': ['Productive Group Work', 'Facilitator Lecture', 'Structured Practical', 'Distractive Chaos', 'Individual Quiet Work'],
        'Duration': [22, 15, 8, 3, 5]
    }
    df_activity = pd.DataFrame(activity_data)
    
    fig = go.Figure(data=[go.Pie(
        labels=df_activity['Activity'], 
        values=df_activity['Duration'], 
        hole=.5, 
        marker_colors=['#10b981', '#6366f1', '#22d3ee', '#ef4444', '#9ca3af']
    )])
    
    fig.update_layout(
        template='plotly_dark',
        height=350,
        plot_bgcolor='#111827', paper_bgcolor='#1f2937',
        showlegend=True,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    return fig

# --- PAGE LAYOUT ---

layout = html.Div([
    # Hidden component to store and drive the mock score value
    dcc.Store(id='vibe-score-storage', data={'current_score': MOCK_VIBE_SCORE}),
    # Hidden interval to trigger the mock degradation every 3 seconds (3000 ms)
    dcc.Interval(id='vibe-interval', interval=3000, n_intervals=0),

    dbc.Row([
        # Main Title Header (Inside the content area)
        dbc.Col(
            html.H1('LIVE SESSION DASHBOARD // REAL-TIME VIBE CHECK', 
                    className="text-4xl font-extrabold mb-8 pb-4 border-b-4 border-gray-700", 
                    style=NEON_TEXT_STYLE),
            width=12
        ),
    ]),
    
    # MAIN CONTENT GRID
    dbc.Row([
        # COLUMN 1: VIBE SCORE & RECOMMENDATION
        dbc.Col([
            # Vibe Score Card
            dbc.Card([
                html.H2('CURRENT VIBE SCORE [LIVE FEED]', className='text-xl font-bold mb-4', style={'color': '#e5e7eb'}),
                html.Div([
                    # ID added to make the text dynamically updatable
                    html.P(f'{MOCK_VIBE_SCORE}%', id='current-engagement-text', style={**NEON_TEXT_STYLE, 'font-size': '4rem'}),
                    # ID added to make the status dynamically updatable
                    html.Span('OPTIMAL VIBE', id='vibe-status', className='px-3 py-1 font-bold rounded-full bg-emerald-900/50 text-emerald-300 border border-emerald-500')
                ], className='flex justify-between items-center border-b border-gray-700 pb-4 mb-4'),
                
                # Metrics Grid
                dbc.Row([
                    dbc.Col([
                        html.P('18 / 20', className='text-3xl font-mono', id='attendance-count', style=NEON_TEXT_STYLE),
                        html.P('ATTENDANCE COUNT', className='text-sm text-gray-400 mt-1')
                    ], className='bg-gray-900 p-3 rounded-lg border border-gray-700 text-center'),
                    dbc.Col([
                        html.P('92%', className='text-3xl font-mono', id='focus-level', style=NEON_TEXT_STYLE),
                        html.P('VISUAL FOCUS INDEX', className='text-sm text-gray-400 mt-1')
                    ], className='bg-gray-900 p-3 rounded-lg border border-gray-700 text-center'),
                ], className='g-3')
            ], style=CYBER_CARD_STYLE, className='mb-4 border-t-4 border-emerald-500 shadow-lg shadow-emerald-900/50'),

            # Predictive Trend Analysis (USP Card)
            dbc.Card([
                # ID added here: This is the element that will have its color updated dynamically
                html.H2('CRITICAL THRESHOLD BREACH', id='critical-breach-heading', className='text-2xl font-extrabold mb-3', style=FUCHSIA_TEXT_STYLE),
                html.P('PREDICTED VIBE DROP: -25% in 15 minutes. HIGH DISENGAGEMENT PROTOCOL ACTIVE.', 
                       className='text-lg font-mono text-fuchsia-200 border-b border-fuchsia-700 pb-3 mb-4'),
                html.Div([
                    html.P('PROACTIVE INTERVENTION [IMPERATIVE]:', className='uppercase text-xs tracking-widest opacity-80 mb-2'),
                    html.P('EXECUTE GROUP HACK V2.0 NOW (5 MIN). OVERRIDE FATIGUE/RE-ENGAGE.', 
                           className='text-xl font-mono')
                ], className='bg-fuchsia-700 text-white p-4 rounded-lg font-extrabold shadow-2xl border border-fuchsia-400 pulse-urgent', id='recommendation-card-content')
            ], style=CYBER_CARD_STYLE, className='border-t-4 border-fuchsia-400 shadow-xl shadow-fuchsia-900/70'),

        ], lg=4),

        # COLUMN 2: Predictive Engagement Trend Chart
        dbc.Col([
            dbc.Card([
                dcc.Graph(
                    id='predictive-graph',
                    figure=create_predictive_graph(df),
                    config={'displayModeBar': False}
                ),
            ], style=CYBER_CARD_STYLE),
        ], lg=8),
    ], className='mb-6 mt-4'), # MODIFIED: Added mt-4 for top margin and kept mb-6 for bottom margin.

    # ACTIVITY BREAKDOWN ROW
    dbc.Row([
        # Activity Breakdown Chart
        dbc.Col([
            dbc.Card([
                html.H2('ACTIVITY HASHMAP [LAST 30 CYCLES]', className='text-xl font-mono font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2'),
                dcc.Graph(
                    id='activity-chart',
                    figure=create_activity_graph(),
                    config={'displayModeBar': False},
                    style={'height': '350px'}
                ),
            ], style={**CYBER_CARD_STYLE, 'height': '100%'}),
        ], md=8),
        
        # Summary Panel
        dbc.Col([
            # Productive
            dbc.Card([
                html.P('PRODUCTIVE CLUSTER TIME', className='text-sm font-bold text-emerald-400 mb-1'),
                html.P('22 MIN', className='text-3xl font-mono text-emerald-300', style=NEON_TEXT_STYLE),
                html.P('GROUP ALIGNMENT: 95% CONFIDENCE', className='text-xs text-gray-400')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #10b981'}, className='mb-3'),
            
            # Distractive
            dbc.Card([
                html.P('DISTRACTIVE NON-ALIGNMENT', className='text-sm font-bold text-red-400 mb-1'),
                html.P('3 MIN', className='text-3xl font-mono text-red-300', style=FUCHSIA_TEXT_STYLE),
                html.P('EXCESSIVE MOTION/HEAD-DOWN DETECTED', className='text-xs text-gray-400')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #ef4444'}, className='mb-3'),
            
            # Key Insight
            dbc.Card([
                html.P('SYSTEM KEY INSIGHT', className='text-sm font-bold text-cyan-400 mb-1'),
                html.P('PEER COLLABORATION IS HIGH-YIELD. MAXIMIZE DURATION.', className='text-md font-mono text-cyan-300')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #22d3ee'}),
            
        ], md=4, className='space-y-4')
    ], className='mb-6 mt-4'), # End of Row
])


# --- CALLBACKS FOR DYNAMIC COLOR AND SCORE ---
@dash.callback(
    [
        Output('vibe-score-storage', 'data'),
        Output('current-engagement-text', 'children'),
        Output('vibe-status', 'children'),
        Output('vibe-status', 'className'),
        Output('critical-breach-heading', 'style'),
        Output('focus-level', 'children')
    ],
    [
        Input('vibe-interval', 'n_intervals')
    ],
    [
        State('vibe-score-storage', 'data')
    ]
)
def update_vibe_score_and_color(n_intervals, data):
    # Simulate score degradation (Mock logic for hackathon demo)
    current_score = data.get('current_score', MOCK_VIBE_SCORE)
    
    # Degradation: Decrease score every interval, stop at 30
    if current_score > 30:
        new_score = current_score - 2
    else:
        new_score = 30 # Maintain a floor
        
    data['current_score'] = new_score
    
    # 1. Calculate Dynamic Color
    dynamic_color = get_color_from_score(new_score)
    dynamic_shadow = f'0 0 5px {dynamic_color}, 0 0 10px {dynamic_color}'
    
    # 2. Update Heading Style
    new_heading_style = {
        'color': dynamic_color, 
        'text-shadow': dynamic_shadow, 
        'transition': 'color 0.5s ease, text-shadow 0.5s ease'
    }
    
    # 3. Determine Vibe Status Label and Class
    status_data = VIBE_STATUS_MAP[80] 
    for threshold, status in sorted(VIBE_STATUS_MAP.items(), reverse=True):
        if new_score >= threshold:
            status_data = status
            break
            
    # Format Vibe Status ClassName (Tailwind requires explicit class strings)
    status_class = f'px-3 py-1 font-bold rounded-full {status_data["bg"]} text-{status_data["color"]} border border-{status_data["color"]}'
    
    # 4. Return all updated values
    return (
        data, # 1. Vibe Score Storage
        f'{new_score}%', # 2. Current Engagement Text
        status_data['label'], # 3a. Vibe Status Label
        status_class, # 3b. Vibe Status ClassName
        new_heading_style, # 4. Critical Breach Heading Style
        f'{new_score + np.random.randint(2, 5)}%' # 5. Mock Focus Level
    )
