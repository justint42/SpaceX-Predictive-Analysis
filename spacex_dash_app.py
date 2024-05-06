# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objects as go
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
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder='Choose Site',
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={
        0: '0 kg',
        2500: '2500 kg',
        5000: '5000 kg',
        7500: '7500 kg',
        10000: '10000 kg'
    },
    value=[min_payload, max_payload]
),
html.Br(),


    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df[spacex_df['class'] == 1],
            names='Launch Site',
            title='Total Success Launches by Site')
    else:
        fig = px.pie(
            spacex_df[spacex_df['Launch Site'] == entered_site],
            names='class',
            title=f'Total Success Launches for site {entered_site}')
    return fig




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):

    # df_filtered is a DataFrame that filters the original spacex_df DataFrame.
    # It only includes rows where the 'Payload Mass (kg)' falls within the range specified by the payload slider.
    # This filtering makes sure that the scatter plot only displays data points relevant to the selected payload mass range.

    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if entered_site == 'ALL':
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload and Launch Success Correlation (All Sites)',
            labels={'class': 'Launch Success'})
    else:
        df_filtered = df_filtered[df_filtered['Launch Site'] == entered_site]
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload and Launch Success Correlation for {entered_site}',
            labels={'class': 'Launch Success'})

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)



"""
Which site has the largest successful launches?

KSC LC-39A

Which site has the highest launch success rate?

CCAFS SLC-40

Which payload range(s) has the highest launch success rate?

Payload range of 1900 to 5300

Which payload range(s) has the lowest launch success rate?

500 - 1000, 2200 - 2700, 4200 - 4700, 5200 - 6761

Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?

FT

FT in payloads between 2k and 4k

"""