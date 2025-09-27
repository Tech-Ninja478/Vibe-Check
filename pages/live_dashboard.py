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

# --- PLOTLY GRAPHIC FUNCTIONS ---

# Initial Mock Data: 
# We use dcc.Store to hold the *current* state of the graph data for persistent updates.
initial_time_labels = pd.date_range('10:00', periods=10, freq='5min').strftime('%H:%M')
initial_engagement = list(np.random.randint(85, 95, 10))

# This data store holds the graph's history
GRAPH_DATA_STORE_ID = 'predictive-graph-data'


def create_predictive_graph(x_data, y_actual, y_predicted):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data, y=y_actual, mode='lines+markers', name='ACTUAL VIBE LEVEL',
        line=dict(color='#22d3ee', width=4), marker=dict(size=8, color='#22d3ee', line=dict(width=2, color='#1f2937'))
    ))
    
    # Only plot prediction if it's not all None
    if any(y_predicted):
        fig.add_trace(go.Scatter(
            x=x_data, y=y_predicted, mode='lines', name='CRITICAL FORECAST',
            line=dict(color='#ec4899', width=3, dash='dashdot'),
        ))
        
    fig.update_layout(
        template='plotly_dark',
        title={'text': 'ENGAGEMENT TIMELINE: ACTUAL VS. CRITICAL FORECAST (USP)', 'x': 0.5, 'font': {'size': 20, 'color': '#e5e7eb', 'family': 'monospace'}},
        height=400, plot_bgcolor='#111827', paper_bgcolor='#1f2937', font=dict(color='#e5e7eb', family='Inter'),
        xaxis_title="Time Code", yaxis_title="VIBE LEVEL (%)", margin=dict(l=40, r=20, t=60, b=40),
        yaxis_range=[50, 100] # Set fixed range for better visualization
    )
    return fig

# Initial Activity Data and Graph Creator (for Donut Chart)
initial_activity_data = {
    'Activity': ['Productive Group Work', 'Facilitator Lecture', 'Structured Practical', 'Distractive Chaos', 'Individual Quiet Work'],
    'Duration': [22, 15, 8, 3, 5]
}
df_activity = pd.DataFrame(initial_activity_data)

def create_activity_graph(hole_size=0.5, colors=None, pull_index=None):
    
    # Define custom cyber colors
    cyber_colors = colors if colors else ['#10b981', '#6366f1', '#22d3ee', '#ef4444', '#9ca3af']
    
    # Calculate pull list for exploded view effect
    pull_list = [0.0] * len(df_activity)
    if pull_index is not None:
        pull_list[pull_index] = 0.1 # Pull the selected slice out

    fig = go.Figure(data=[go.Pie(
        labels=df_activity['Activity'], 
        values=df_activity['Duration'], 
        hole=hole_size, # Dynamic hole size
        marker=dict(colors=cyber_colors, line=dict(color='#111827', width=2)),
        textinfo='percent+label',
        hoverinfo='label+percent',
        pull=pull_list # Dynamic pull effect
    )])
    
    fig.update_layout(
        template='plotly_dark',
        height=350,
        plot_bgcolor='#111827', paper_bgcolor='#1f2937',
        showlegend=True,
        margin=dict(t=0, b=0, l=0, r=0),
        uniformtext_minsize=12, 
        uniformtext_mode='hide'
    )
    
    return fig

# --- PAGE LAYOUT ---

layout = html.Div([
    # Store to hold the degrading Vibe Score for text updates
    dcc.Store(id='vibe-score-storage', data={'current_score': MOCK_VIBE_SCORE}),
    # Store to hold the graph's historical data
    dcc.Store(id=GRAPH_DATA_STORE_ID, data={
        'time': list(initial_time_labels), 
        'actual': initial_engagement, 
        'predicted': [None] * len(initial_engagement)
    }),
    # Hidden interval to trigger the mock degradation every 3 seconds (3000 ms)
    dcc.Interval(id='vibe-interval', interval=3000, n_intervals=0),
    
    # Store to hold the state of the donut chart (clicked slice)
    dcc.Store(id='activity-chart-state', data={'pull_index': -1}),


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
            ], style={**CYBER_CARD_STYLE, 'height': '100%'}, className='mb-4 border-t-4 border-emerald-500 shadow-lg shadow-emerald-900/50'),

            # Predictive Trend Analysis (USP Card)
            dbc.Card([
                # ID added here: This is the element that will have its color updated dynamically
                html.H2('CRITICAL THRESHOLD BREACH', id='critical-breach-heading', className='text-2xl font-extrabold mb-3', style=FUCHSIA_TEXT_STYLE),
                html.P('PREDICTED VIBE DROP: -25% in 15 minutes. HIGH DISENGAGEMENT PROTOCOL ACTIVE.', 
                       className='text-lg font-mono text-fuchsia-200 border-b border-fuchsia-700 pb-3 mb-4', id='prediction-text-output'),
                html.Div([
                    html.P('PROACTIVE INTERVENTION [IMPERATIVE]:', className='uppercase text-xs tracking-widest opacity-80 mb-2'),
                    html.P('EXECUTE GROUP HACK V2.0 NOW (5 MIN). OVERRIDE FATIGUE/RE-ENGAGE.', 
                           className='text-xl font-mono', id='recommendation-text-output')
                ], className='bg-fuchsia-700 text-white p-4 rounded-lg font-extrabold shadow-2xl border border-fuchsia-400 pulse-urgent')

            ], style={**CYBER_CARD_STYLE, 'height': '100%'}, className='border-t-4 border-fuchsia-400 shadow-xl shadow-fuchsia-900/70'),

        ], lg=4, className='d-flex flex-column justify-content-between'), # Use d-flex to ensure column items fill space

        # COLUMN 2: Predictive Engagement Trend Chart
        dbc.Col([
            dbc.Card([
                dcc.Graph(
                    id='predictive-graph',
                    figure=create_predictive_graph(initial_time_labels, initial_engagement, [None] * len(initial_engagement)),
                    config={'displayModeBar': False}
                ),
            ], style={**CYBER_CARD_STYLE, 'height': '100%'}),
        ], lg=8),

    ], className='mb-6 mt-4'), 

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
                html.P('22 MIN', className='text-3xl font-mono text-emerald-300', style=NEON_TEXT_STYLE, id='productive-time'),
                html.P('GROUP ALIGNMENT: 95% CONFIDENCE', className='text-xs text-gray-400')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #10b981'}, className='mb-3'),
            
            # Distractive
            dbc.Card([
                html.P('DISTRACTIVE NON-ALIGNMENT', className='text-sm font-bold text-red-400 mb-1'),
                html.P('3 MIN', className='text-3xl font-mono text-red-300', style=FUCHSIA_TEXT_STYLE, id='distractive-time'),
                html.P('EXCESSIVE MOTION/HEAD-DOWN DETECTED', className='text-xs text-gray-400')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #ef4444'}, className='mb-3'),
            
            # Key Insight
            dbc.Card([
                html.P('SYSTEM KEY INSIGHT', className='text-sm font-bold text-cyan-400 mb-1'),
                html.P('PEER COLLABORATION IS HIGH-YIELD. MAXIMIZE DURATION.', className='text-md font-mono text-cyan-300', id='key-insight-text')
            ], style={**CYBER_CARD_STYLE, 'border-left': '4px solid #22d3ee'}),
            
        ], md=4, className='space-y-4')
    ], className='mb-6 mt-4'), 

])


# --- CALLBACKS FOR DYNAMIC COLOR, SCORE, AND GRAPH UPDATE ---

@dash.callback(
    [
        Output('vibe-score-storage', 'data'),
        Output(GRAPH_DATA_STORE_ID, 'data'),
        Output('current-engagement-text', 'children'),
        Output('vibe-status', 'children'),
        Output('vibe-status', 'className'),
        Output('critical-breach-heading', 'style'),
        Output('predictive-graph', 'figure'),
        Output('focus-level', 'children'),
        Output('prediction-text-output', 'children'),
        Output('recommendation-text-output', 'children'),
    ],
    [
        Input('vibe-interval', 'n_intervals')
    ],
    [
        State('vibe-score-storage', 'data'),
        State(GRAPH_DATA_STORE_ID, 'data')
    ]
)
def update_vibe_score_and_color(n_intervals, vibe_data, graph_data):
    
    # 1. SCORE DEGRADATION LOGIC
    current_score = vibe_data.get('current_score', MOCK_VIBE_SCORE)
    
    # --- MODIFIED LOGIC: RANDOMIZED SCORE CHANGE ---
    
    # Generate a random change (increase or decrease)
    # Range: -3 to +3 points. This keeps it dynamic.
    score_change = np.random.randint(-3, 4) 
    
    # Apply a slight bias towards decrease if score is high (simulating natural fatigue)
    if current_score > 85 and score_change > 0:
        score_change = np.random.randint(-2, 2) # Reduce likelihood of large gains at peak
        
    # Apply a strong bias towards increase if score is very low (simulating intervention effect)
    if current_score < 60 and score_change < 0:
        score_change = np.random.randint(-1, 4) # Increase likelihood of recovery
    
    new_score = current_score + score_change
    
    # Clamp score between 30 and 99 (for a realistic range)
    new_score = max(30, min(99, new_score))
        
    vibe_data['current_score'] = new_score
    
    # 2. GRAPH DATA UPDATE LOGIC
    
    # Determine the next time label
    if graph_data['time']:
        last_time_str = graph_data['time'][-1]
        last_time = pd.to_datetime(last_time_str, format='%H:%M')
        new_time = (last_time + pd.Timedelta(minutes=5)).strftime('%H:%M')
    else:
        new_time = '10:00'
    
    # Append new data point
    graph_data['time'].append(new_time)
    graph_data['actual'].append(new_score)
    
    # Trim the data to show only the last 20 points for a moving window
    max_points = 20
    graph_data['time'] = graph_data['time'][-max_points:]
    graph_data['actual'] = graph_data['actual'][-max_points:]
    
    # Create mock prediction for the next few points if the score drops low
    y_predicted = [None] * len(graph_data['actual'])
    
    prediction_text = 'PREDICTED VIBE DROP: -25% in 15 minutes. HIGH DISENGAGEMENT PROTOCOL ACTIVE.'
    recommendation_text = 'EXECUTE GROUP HACK V2.0 NOW (5 MIN). OVERRIDE FATIGUE/RE-ENGAGE.'
    
    if new_score <= 70: # Start prediction when score hits a critical level
        
        # Start prediction 5 points before the end
        prediction_start_index = max(0, len(graph_data['actual']) - 5)
        
        # Simulate a drop forecast: 1 point lower than current for the next 3 points
        mock_forecast = [score - 5 - i*2 for i, score in enumerate(graph_data['actual'][prediction_start_index:])]
        
        # Merge actual and prediction list
        for i in range(len(mock_forecast)):
            index = prediction_start_index + i
            if index < len(y_predicted):
                y_predicted[index] = mock_forecast[i]
                
    else:
        prediction_text = 'FORECAST: STABLE. CONTINUE CURRENT PEDAGOGICAL PROTOCOL.'
        recommendation_text = 'PROTOCOL GREEN: MONITOR VIBE SCORE.'

    # 3. COLOR AND STATUS LOGIC
    
    # Calculate Dynamic Color
    dynamic_color = get_color_from_score(new_score)
    dynamic_shadow = f'0 0 5px {dynamic_color}, 0 0 10px {dynamic_color}'
    
    # Update Heading Style
    new_heading_style = {
        'color': dynamic_color, 
        'text-shadow': dynamic_shadow, 
        'transition': 'color 0.5s ease, text-shadow 0.5s ease'
    }
    
    # Determine Vibe Status Label and Class
    status_data = VIBE_STATUS_MAP[80] 
    for threshold, status in sorted(VIBE_STATUS_MAP.items(), reverse=True):
        if new_score >= threshold:
            status_data = status
            break
            
    # Format Vibe Status ClassName (Tailwind requires explicit class strings)
    status_class = f'px-3 py-1 font-bold rounded-full {status_data["bg"]} text-{status_data["color"]} border border-{status_data["color"]}'
    
    # Recreate the figure with the new data
    new_figure = create_predictive_graph(graph_data['time'], graph_data['actual'], y_predicted)
    
    # 4. RETURN ALL UPDATED VALUES
    return (
        vibe_data, # 1. Vibe Score Storage
        graph_data, # 2. Graph Data Store
        f'{new_score}%', # 3. Current Engagement Text
        status_data['label'], # 4a. Vibe Status Label
        status_class, # 4b. Vibe Status ClassName
        new_heading_style, # 5. Critical Breach Heading Style
        new_figure, # 6. Predictive Graph Figure
        f'{new_score + np.random.randint(2, 5)}%', # 7. Mock Focus Level
        prediction_text, # 8. Prediction Text
        recommendation_text # 9. Recommendation Text
    )

# --- NEW CALLBACK FOR INTERACTIVE PIE CHART (ZOOM EFFECT) ---
@dash.callback(
    Output('activity-chart', 'figure'),
    [Input('activity-chart', 'clickData')],
    [State('activity-chart-state', 'data')]
)
def update_activity_graph(clickData, state):
    
    # Default to the initial graph if no click data or click data is reset
    if not clickData or (state.get('pull_index', -1) != -1 and not clickData):
        # Reset graph state and figure (no pull, default hole size)
        new_pull_index = -1
        state['pull_index'] = new_pull_index
        return create_activity_graph(hole_size=0.5, pull_index=new_pull_index)
        
    # Determine the index of the clicked slice
    clicked_index = clickData['points'][0]['pointIndex']
    
    # Check if the same slice was clicked twice (to trigger zoom-out/reset)
    if clicked_index == state.get('pull_index', -1):
        # Zoom out / Reset
        new_pull_index = -1
        new_hole_size = 0.5
    else:
        # Zoom in / Select new slice
        new_pull_index = clicked_index
        new_hole_size = 0.65 # Make the hole larger for a dramatic zoom effect
    
    # Update the stored state for the next call
    state['pull_index'] = new_pull_index
    
    # Return the new figure
    return create_activity_graph(hole_size=new_hole_size, pull_index=new_pull_index)
