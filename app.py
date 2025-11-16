import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt

# Load data
df = pd.read_csv('data/data1985.csv',parse_dates=['dt'])

# Data preprocessing
# df = df.dropna(subset=['AverageTemperature'])
df['Year'] = df['dt'].dt.year
df['Month'] = df['dt'].dt.month

# Convert geographical coordinates
def convert_lat_lon(coord):
    try:
        if 'N' in coord:
            return float(coord.replace('N', ''))
        elif 'S' in coord:
            return -float(coord.replace('S', ''))
        elif 'E' in coord:
            return float(coord.replace('E', ''))
        elif 'W' in coord:
            return -float(coord.replace('W', ''))
    except:
        return np.nan

df['Latitude_num'] = df['Latitude'].apply(convert_lat_lon)
df['Longitude_num'] = df['Longitude'].apply(convert_lat_lon)

# Use Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

# Navigation
navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.Img(src="/assets/logo.svg", height="30px")),
                dbc.Col(dbc.NavbarBrand("Climate Analytics", className="ms-2")),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"},
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/", id="home-link")),
                dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard", id="dashboard-link")),
                dbc.NavItem(dbc.NavLink("About", href="#")),
            ], className="ms-auto", navbar=True),
            id="navbar-collapse",
            navbar=True,
        ),
    ]),
    color="primary",
    dark=True,
    sticky="top"
)

# Function to create table from dataframe
def create_data_table(df):
    """Create a Dash table from pandas dataframe"""
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ], className="table table-striped table-bordered table-hover")

# Landing Page
landing_page = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H1("🌍 Global Climate Change Analytics", 
                               className="display-4 mb-4",
                               style={'color': '#2c3e50'}),
                        html.P("Discover temperature trends from over 200 years of data collected worldwide. "
                              "Use this platform to visually and interactively explore climate change patterns.",
                              className="lead mb-4"),
                        dbc.Button("Get Started", 
                                  id="get-started-btn",
                                  color="primary", 
                                  size="lg",
                                  className="me-2"),
                        dbc.Button("About Data", 
                                  id="about-data-btn",
                                  color="outline-primary", 
                                  size="lg"),
                    ], className="text-center")
                ])
            ], className="border-0 bg-transparent")
        ], width=12)
    ], className="my-5"),
    
    # Features Section
    dbc.Row([
        dbc.Col([
            html.H2("Key Features", className="text-center mb-5")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H1("📊", style={'fontSize': '3rem'}),
                        html.H4("Historical Data"),
                        html.P("Temperature data from 1743 to 2013 from cities around the world")
                    ], className="text-center")
                ])
            ], className="h-100")
        ], md=4, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H1("🗺️", style={'fontSize': '3rem'}),
                        html.H4("Interactive Map"),
                        html.P("Visualize data on global maps with zoom and filter capabilities")
                    ], className="text-center")
                ])
            ], className="h-100")
        ], md=4, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H1("📈", style={'fontSize': '3rem'}),
                        html.H4("Trend Analysis"),
                        html.P("Examine temperature change trends over time for different countries")
                    ], className="text-center")
                ])
            ], className="h-100")
        ], md=4, className="mb-4")
    ]),
    
    # Statistics Section
    dbc.Row([
        dbc.Col([
            html.H2("Dataset Overview", className="text-center my-5")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H3(f"{len(df['City'].unique()):,}", className="text-primary"),
                        html.P("Unique Cities")
                    ], className="text-center")
                ])
            ])
        ], md=3, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H3(f"{len(df['Country'].unique()):,}", className="text-success"),
                        html.P("Different Countries")
                    ], className="text-center")
                ])
            ])
        ], md=3, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H3(f"{df['Year'].max() - df['Year'].min():,}", className="text-warning"),
                        html.P("Years of Historical Data")
                    ], className="text-center")
                ])
            ])
        ], md=3, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H3(f"{len(df):,}", className="text-info"),
                        html.P("Data Records")
                    ], className="text-center")
                ])
            ])
        ], md=3, className="mb-4")
    ], className="mb-5"),
    
    # Data Sample Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Data Sample"),
                dbc.CardBody([
                    html.Div(id="data-sample")
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Store to track current page
current_page_store = dcc.Store(id='current-page', data='/')

# Main Dashboard
def create_dashboard():
    # Sidebar
    sidebar = dbc.Card([
        dbc.CardBody([
            html.H4("Controls", className="card-title", style={'textAlign': 'center'}),
            html.Hr(),
            html.H6("Select Time Range", className="mt-3"),
            dcc.RangeSlider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=[1950, 2013],
                marks={str(year): str(year) for year in range(1850, 2014, 50)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.H6("Select Month", className="mt-4"),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': f'Month {i}', 'value': i} for i in range(1, 13)],
                value=7,
                clearable=False
            ),
            html.H6("Select Countries", className="mt-4"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} 
                        for country in sorted(df['Country'].unique())],
                value=['United States', 'China', 'India', 'Brazil', 'Germany'],
                multi=True
            ),
            html.H6("Map Type", className="mt-4"),
            dbc.RadioItems(
                id='map-type',
                options=[
                    {'label': 'Heat Map', 'value': 'density'},
                    {'label': 'Scatter Map', 'value': 'scatter'}
                ],
                value='scatter',
                inline=True
            ),
            html.Hr(),
            dbc.Button("Back to Home", id="back-to-home", color="secondary", className="w-100")
        ])
    ], style={"height": "100vh", "position": "sticky", "top": 0})
    
    # Stats Cards
    stats_cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🌡️ Average Temp", className="card-title"),
                html.H4(id="avg-temp", className="card-text")
            ])
        ], color="primary", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🔥 Max Temp", className="card-title"),
                html.H4(id="max-temp", className="card-text")
            ])
        ], color="danger", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("❄️ Min Temp", className="card-title"),
                html.H4(id="min-temp", className="card-text")
            ])
        ], color="info", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🏙️ Cities Count", className="card-title"),
                html.H4(id="cities-count", className="card-text")
            ])
        ], color="success", inverse=True), width=3)
    ])
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🌍 Global Temperature Change Map", 
                       className="text-center my-4",
                       style={'color': '#2c3e50'})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(stats_cards, width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(sidebar, width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='world-map', style={'height': '500px'})
                            ])
                        ])
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='temperature-trend', style={'height': '300px'})
                            ])
                        ])
                    ], width=12)
                ], className="mt-4")
            ], width=9)
        ])
    ], fluid=True)

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    current_page_store,
    navbar,
    html.Div(id='page-content')
])

# Callback for page navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dashboard':
        return create_dashboard()
    else:
        return landing_page

# Navigation callbacks
@app.callback(
    Output('url', 'pathname'),
    [Input('dashboard-link', 'n_clicks'),
     Input('back-to-home', 'n_clicks'),
     Input('home-link', 'n_clicks')],
    [State('url', 'pathname')],
    prevent_initial_call=True
)
def handle_navigation(dashboard_clicks, back_home_clicks, home_clicks, current_path):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return current_path
    
    # Get the ID of the component that triggered the callback
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle navigation based on which button was clicked
    if trigger_id == 'dashboard-link':
        return '/dashboard'
    elif trigger_id in ['back-to-home', 'home-link']:
        return '/'
    
    return current_path

# Landing page button callbacks
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('get-started-btn', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_dashboard(n_clicks):
    if n_clicks:
        return '/dashboard'
    return '/'

# Callback for data sample
@app.callback(
    Output('data-sample', 'children'),
    [Input('url', 'pathname')]
)
def show_data_sample(pathname):
    sample_df = df[['dt', 'City', 'Country', 'AverageTemperature']].head(10)
    
    # Create table header
    header = [html.Tr([html.Th(col) for col in sample_df.columns])]
    
    # Create table rows
    rows = []
    for i in range(len(sample_df)):
        row = html.Tr([
            html.Td(str(sample_df.iloc[i][col])) for col in sample_df.columns
        ])
        rows.append(row)
    
    # Return the table with Bootstrap classes
    return html.Table(
        # Header
        [html.Thead(header)] +
        # Body
        [html.Tbody(rows)],
        className="table table-striped table-bordered table-hover w-100"
    )

# Dashboard callbacks
@app.callback(
    Output('world-map', 'figure'),
    [Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('map-type', 'value')]
)
def update_map(selected_years, selected_month, selected_countries, map_type):
    filtered_df = df[
        (df['Year'] >= selected_years[0]) & 
        (df['Year'] <= selected_years[1]) &
        (df['Month'] == selected_month) &
        (df['Country'].isin(selected_countries))
    ]
    
    city_avg = filtered_df.groupby(['City', 'Country', 'Latitude_num', 'Longitude_num']).agg({
        'AverageTemperature': 'mean',
        'AverageTemperatureUncertainty': 'mean'
    }).reset_index()
    
    if map_type == 'scatter':
        fig = px.scatter_mapbox(
            city_avg,
            lat="Latitude_num",
            lon="Longitude_num",
            size="AverageTemperature",
            color="AverageTemperature",
            hover_name="City",
            hover_data={
                "Country": True,
                "AverageTemperature": ":.2f",
                "AverageTemperatureUncertainty": ":.2f"
            },
            color_continuous_scale=px.colors.sequential.Plasma,
            zoom=1,
            title=f"Average City Temperatures ({selected_years[0]}-{selected_years[1]})"
        )
    else:
        fig = px.density_mapbox(
            city_avg,
            lat="Latitude_num",
            lon="Longitude_num",
            z="AverageTemperature",
            radius=10,
            hover_name="City",
            color_continuous_scale=px.colors.sequential.Plasma,
            zoom=1,
            title=f"Temperature Density Map ({selected_years[0]}-{selected_years[1]})"
        )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

@app.callback(
    [Output('avg-temp', 'children'),
     Output('max-temp', 'children'),
     Output('min-temp', 'children'),
     Output('cities-count', 'children')],
    [Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_stats_cards(selected_years, selected_month, selected_countries):
    filtered_df = df[
        (df['Year'] >= selected_years[0]) & 
        (df['Year'] <= selected_years[1]) &
        (df['Month'] == selected_month) &
        (df['Country'].isin(selected_countries))
    ]
    
    avg_temp = filtered_df['AverageTemperature'].mean()
    max_temp = filtered_df['AverageTemperature'].max()
    min_temp = filtered_df['AverageTemperature'].min()
    num_cities = filtered_df['City'].nunique()
    
    return (
        f"{avg_temp:.1f}°C" if not pd.isna(avg_temp) else "N/A",
        f"{max_temp:.1f}°C" if not pd.isna(max_temp) else "N/A",
        f"{min_temp:.1f}°C" if not pd.isna(min_temp) else "N/A",
        f"{num_cities}"
    )

@app.callback(
    Output('temperature-trend', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_trend(selected_countries, selected_years):
    trend_df = df[
        (df['Country'].isin(selected_countries)) &
        (df['Year'] >= selected_years[0]) & 
        (df['Year'] <= selected_years[1])
    ]
    
    yearly_avg = trend_df.groupby(['Year', 'Country'])['AverageTemperature'].mean().reset_index()
    
    fig = px.line(
        yearly_avg,
        x='Year',
        y='AverageTemperature',
        color='Country',
        title='Annual Temperature Trends',
        labels={'AverageTemperature': 'Average Temperature (°C)', 'Year': 'Year'}
    )
    
    fig.update_layout(
        xaxis_range=[selected_years[0], selected_years[1]]
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)