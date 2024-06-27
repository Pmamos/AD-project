import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Year, Age, Death, Continent, Country, db_string  # assuming models.py contains your ORM classes

# Create a Dash application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Database connection
engine = create_engine(db_string)  # Update with your database path
Session = sessionmaker(bind=engine)
session = Session()

# Fetch initial data for dropdowns
countries = session.query(Country).all()
ages = session.query(Age).all()

# Fetch default values
default_country = session.query(Country).filter_by(country='Brazil').first()

# Convert to DataFrame
country_df = pd.DataFrame([(c.id_country, c.country) for c in countries], columns=['id_country', 'country'])
age_df = pd.DataFrame([(a.id_age, a.age) for a in ages], columns=['id_age', 'age'])

# Define the top menu layout
menu_layout = html.Div([
    dcc.Link('Dashboard 1', href='/dashboard1'),
    dcc.Link('Dashboard 2', href='/dashboard2'),
    dcc.Link('Dashboard 3', href='/dashboard3'),
    dcc.Link('Dashboard 4', href='/dashboard4'),
    dcc.Link('Dashboard 5', href='/dashboard5'),
], style={'display': 'flex', 'gap': '20px', 'justify-content': 'center', 'padding': '20px', 'background': '#f0f0f0'})

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    menu_layout,
    html.Div(id='page-content')
])

# Define the content for Dashboard 1 (the provided dashboard code)
dashboard1_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': row['country'], 'value': row['id_country']} for index, row in country_df.iterrows()],
            multi=True,
            placeholder="Select Country/Countries",
            value=[default_country.id_country] if default_country else None
        ),
        dcc.Dropdown(
            id='sex-dropdown',
            options=[
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'}
            ],
            placeholder="Select Sex",
            value=None
        ),
        dcc.Dropdown(
            id='age-dropdown',
            options=[{'label': row['age'], 'value': row['id_age']} for index, row in age_df.iterrows()],
            placeholder="Select Age Group",
            value=None
        ),
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),
    dcc.Graph(id='death-graph')
])

# Define other dashboard layouts (placeholders)
dashboard2_layout = html.Div([
    html.H1('Dashboard 2'),
    # Add other components and layout for Dashboard 2 here
])

dashboard3_layout = html.Div([
    html.H1('Dashboard 3'),
    # Add other components and layout for Dashboard 3 here
])

dashboard4_layout = html.Div([
    html.H1('Dashboard 4'),
    # Add other components and layout for Dashboard 4 here
])

dashboard5_layout = html.Div([
    html.H1('Dashboard 5'),
    # Add other components and layout for Dashboard 5 here
])

# Callback for updating the graph in Dashboard 1
@app.callback(
    Output('death-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('sex-dropdown', 'value'),
     Input('age-dropdown', 'value')]
)
def update_graph(selected_countries, selected_sex, selected_age):
    query = session.query(Death, Year, Country, Age).join(Year).join(Country).join(Age)
    
    if selected_countries:
        query = query.filter(Death.id_country.in_(selected_countries))
    
    if selected_age is not None:
        query = query.filter(Death.id_age == selected_age)
    
    if selected_sex:
        query = query.filter(Death.sex == selected_sex)
    else:
        query = query.filter(Death.sex == 'Both sexes')
    
    deaths = query.limit(50000).all()  # Limiting the number of records fetched
    
    data = []
    for death, year, country, age in deaths:
        data.append({
            'year': year.year,
            'country': country.country,
            'age': age.age,
            'sex': death.sex,
            'measurement': death.measurement
        })
    
    df = pd.DataFrame(data)
    if df.empty:
        return px.scatter(title='No data available for the selected filters')

    # Group data by year, country, and sex to avoid duplicate entries
    df_grouped = df.groupby(['year', 'country', 'sex']).agg({'measurement': 'sum'}).reset_index()
    
    fig = px.line(df_grouped, x='year', y='measurement', color='country', markers=True,
                  line_group='country', hover_name='country', title='Deaths by Country')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        xaxis=dict(dtick=1, range=[1950, 2024])  
    )
    
    return fig

# Callback for routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/' or pathname == '/dashboard1':
        return dashboard1_layout
    elif pathname == '/dashboard2':
        return dashboard2_layout
    elif pathname == '/dashboard3':
        return dashboard3_layout
    elif pathname == '/dashboard4':
        return dashboard4_layout
    elif pathname == '/dashboard5':
        return dashboard5_layout
    else:
        return html.Div([
            html.H1('404 - Page Not Found'),
            html.P('The page you are looking for does not exist.')
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
