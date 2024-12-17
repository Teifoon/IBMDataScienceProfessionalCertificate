# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}] + 
            [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(i): f"{int(i)} kg" for i in range(int(min_payload), int(max_payload) + 1, 5000)},
        value=[min_payload, max_payload]
    ),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        # Pie chart for all sites showing total successful launches
        fig = px.pie(
            spacex_df, 
            names='Launch Site', 
            values='class', 
            title='Total Success Launches by Site'
        )
    else:
        # Filter for the selected launch site and show success vs failure
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Total Success vs Failure for site {site_dropdown}"
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(site_dropdown, payload_range):
    # Filter data based on payload range
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if site_dropdown == 'ALL':
        # Scatter chart for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Success for All Sites'
        )
    else:
        # Scatter chart for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == site_dropdown]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation Between Payload and Success for site {site_dropdown}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)
    
