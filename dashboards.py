import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Year, Age, Death, Continent, Country, db_string, Birth, Population, Marriage

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

default_country = session.query(Country).filter_by(country='Brazil').first()

country_code_map = {
    "India": "IND",
    "China": "CHN",
    "United States of America": "USA",
    "Indonesia": "IDN",
    "Pakistan": "PAK",
    "Nigeria": "NGA",
    "Brazil": "BRA",
    "Bangladesh": "BGD",
    "Russian Federation": "RUS",
    "Mexico": "MEX",
    "Ethiopia": "ETH",
    "Japan": "JPN",
    "Philippines": "PHL",
    "Egypt": "EGY",
    "Dem. Rep. of the Congo": "COD",
    "Viet Nam": "VNM",
    "Iran (Islamic Republic of)": "IRN",
    "Turkey": "TUR",
    "Germany": "DEU",
    "Thailand": "THA"
}

years = session.query(Year).all()
year_df = pd.DataFrame([(y.id_year, y.year) for y in years], columns=['id_year', 'year'])
year_df = year_df.sort_values(by='year', ascending=True)

# Convert to DataFrame
country_df = pd.DataFrame([(c.id_country, c.country) for c in countries], columns=['id_country', 'country'])
age_df = pd.DataFrame([(a.id_age, a.age) for a in ages], columns=['id_age', 'age'])
age_df['age'] = pd.to_numeric(age_df['age'], errors='coerce')
# Define the top menu layout
menu_layout = html.Div([
    dcc.Link('Deaths by country', href='/deaths'),
    dcc.Link('Births by country', href='/births'),
    dcc.Link('Marriages by country', href='/marriages'),
    dcc.Link('Population by country', href='/population'),
    dcc.Link('Map dashboard', href='/maps'),
], style={'display': 'flex', 'gap': '20px', 'justify-content': 'center', 'padding': '20px', 'background': '#f0f0f0'})

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    menu_layout,
    html.Div(id='page-content')
])

# Define the content for Dashboard 1 
dashboard1_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='death-country-dropdown',
            options=[{'label': row['country'], 'value': row['id_country']} for index, row in country_df.iterrows()],
            multi=True,
            placeholder="Select Country/Countries",
            value=[default_country.id_country] if default_country else None
        ),
        dcc.Dropdown(
            id='death-sex-dropdown',
            options=[
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'}
            ],
            placeholder="Select Sex",
            value=None
        ),
        dcc.Input(
            id='death-age-min-input',
            type='number',
            placeholder='Min Age',
            min=age_df['id_age'].min(),
            max=age_df['id_age'].max(),
            step=1,
            value=None
        ),
        dcc.Input(
            id='death-age-max-input',
            type='number',
            placeholder='Max Age',
            min=age_df['id_age'].min(),
            max=age_df['id_age'].max(),
            step=1,
            value=None
        ),
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),
    dcc.Graph(id='death-graph')
])

dashboard2_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='birth-country-dropdown',
            options=[{'label': row['country'], 'value': row['id_country']} for index, row in country_df.iterrows()],
            multi=True,
            placeholder="Select Country/Countries",
            value=[default_country.id_country] if default_country else None
        ),
        dcc.Input(
            id='birth-age-min-input',
            type='number',
            placeholder='Min Mother Age',
            min=15,
            max=49,
            step=1,
            value=None
        ),
        dcc.Input(
            id='birth-age-max-input',
            type='number',
            placeholder='Max Mother Age',
            min=15,
            max=49,
            step=1,
            value=None
        ),
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),
    dcc.Graph(id='birth-graph')
])

dashboard3_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='marriage-country-dropdown',
            options=[{'label': row['country'], 'value': row['id_country']} for index, row in country_df.iterrows()],
            multi=True,
            placeholder="Select Country/Countries",
            value=[default_country.id_country] if default_country else None
        ),
        dcc.Input(
            id='marriage-age-min-input',
            type='number',
            placeholder='Min Wife Age',
            min=15,
            max=49,
            step=1,
            value=None
        ),
        dcc.Input(
            id='marriage-age-max-input',
            type='number',
            placeholder='Max Wife Age',
            min=15,
            max=49,
            step=1,
            value=None
        ),
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),
    dcc.Graph(id='marriage-graph')
])

dashboard4_layout = html.Div([
html.Div([
        dcc.Dropdown(
            id='population-country-dropdown',
            options=[{'label': row['country'], 'value': row['id_country']} for index, row in country_df.iterrows()],
            multi=True,
            placeholder="Select Country/Countries",
            value=[default_country.id_country] if default_country else None
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),
    dcc.Graph(id='population-graph')
])

dashboard5_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='datatype-dropdown',
            options=[
                {'label': 'Deaths', 'value': 'Deaths'},
                {'label': 'Births', 'value': 'Births'},
                {'label': 'Marriages', 'value': 'Marriages'}
            ],
            placeholder="Select type of data",
            value='Deaths'
        ),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': row['year'], 'value': row['id_year']} for index, row in year_df.iterrows()],
            placeholder="Select year",
            value=20
        ),
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '25%'}),

    dcc.Graph(id='map-graph', style={'height': '800px'}),
])

# Callback for updating the graph in Dashboard 1
@app.callback(
    Output('death-graph', 'figure'),
    [Input('death-country-dropdown', 'value'),
     Input('death-sex-dropdown', 'value'),
     Input('death-age-min-input', 'value'),
     Input('death-age-max-input', 'value')]
)
def update_graph(selected_countries, selected_sex, min_age, max_age):
    query = session.query(Death, Year, Country, Age).join(Year).join(Country).join(Age)

    if selected_countries:
        query = query.filter(Death.id_country.in_(selected_countries))

    if min_age is not None and max_age is not None:
        selected_age_ids = age_df.loc[(age_df['age'] >= min_age) & (age_df['age'] <= max_age), 'id_age'].tolist()

        if selected_age_ids:
            query = query.filter(Death.id_age.in_(selected_age_ids))

    if selected_sex:
        query = query.filter(Death.sex == selected_sex)
    else:
        query = query.filter(Death.sex == 'Both sexes')
      
    deaths = query.all()
    
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


# Callback for updating the graph in Dashboard 2
@app.callback(
    Output('birth-graph', 'figure'),
    [Input('birth-country-dropdown', 'value'),
     Input('birth-age-min-input', 'value'),
     Input('birth-age-max-input', 'value')]
)
def update_graph(selected_countries, min_age, max_age):
    query = session.query(Birth, Year, Country, Age).join(Year).join(Country).join(Age)

    if selected_countries:
        query = query.filter(Birth.id_country.in_(selected_countries))

    if min_age is not None and max_age is not None:
        selected_age_ids = age_df.loc[(age_df['age'] >= min_age) & (age_df['age'] <= max_age), 'id_age'].tolist()

        if selected_age_ids:
            query = query.filter(Birth.id_mother_age.in_(selected_age_ids))


    births = query.all()

    data = []
    for birth, year, country, age in births:
        data.append({
            'year': year.year,
            'country': country.country,
            'age': age.age,
            'measurement': birth.measurement
        })

    df = pd.DataFrame(data)
    if df.empty:
        return px.scatter(title='No data available for the selected filters')

    # Group data by year, country, and sex to avoid duplicate entries
    df_grouped = df.groupby(['year', 'country']).agg({'measurement': 'sum'}).reset_index()

    fig = px.line(df_grouped, x='year', y='measurement', color='country', markers=True,
                  line_group='country', hover_name='country', title='Births by Country')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        xaxis=dict(dtick=1, range=[1950, 2024])
    )

    return fig

# Callback for updating the graph in Dashboard 3
@app.callback(
    Output('marriage-graph', 'figure'),
    [Input('marriage-country-dropdown', 'value'),
     Input('marriage-age-min-input', 'value'),
     Input('marriage-age-max-input', 'value')]
)
def update_graph(selected_countries, min_age, max_age):
    query = session.query(Marriage, Year, Country, Age).join(Year).join(Country).join(Age)

    if selected_countries:
        query = query.filter(Marriage.id_country.in_(selected_countries))

    if min_age is not None and max_age is not None:
        selected_age_ids = age_df.loc[(age_df['age'] >= min_age) & (age_df['age'] <= max_age), 'id_age'].tolist()

        if selected_age_ids:
            query = query.filter(Marriage.id_age.in_(selected_age_ids))


    births = query.all()

    data = []
    for birth, year, country, age in births:
        data.append({
            'year': year.year,
            'country': country.country,
            'age': age.age,
            'measurement': birth.measurement
        })

    df = pd.DataFrame(data)
    if df.empty:
        return px.scatter(title='No data available for the selected filters')

    # Group data by year, country, and sex to avoid duplicate entries
    df_grouped = df.groupby(['year', 'country']).agg({'measurement': 'sum'}).reset_index()

    fig = px.bar(df_grouped, x='year', y='measurement', color='country', hover_name='country', title='Marriages by Country', barmode = 'group')
    fig.update_layout(
        xaxis=dict(dtick=1, range=[1970, 2024])
    )

    return fig

# Callback for updating the graph in Dashboard 4
@app.callback(
    Output('population-graph', 'figure'),
    Input('population-country-dropdown', 'value')
)
def update_graph(selected_countries):
    query = session.query(Population, Country).join(Country)

    if selected_countries:
        query = query.filter(Population.id_country.in_(selected_countries))


    populations = query.all()

    data = []
    for population, country in populations:
        data.append({
            'id_data': population.id_data,
            'country': country.country,
            'measurement': population.measurement
        })

    df = pd.DataFrame(data)
    if df.empty:
        return px.scatter(title='No data available for the selected filters')

    # Group data by year, country, and sex to avoid duplicate entries
    df_grouped = df.groupby(['country', 'id_data']).agg({'measurement': 'sum'}).reset_index()

    fig = px.line(df_grouped, x='id_data', y='measurement', color='country', markers=True,
                  line_group='country', hover_name='country', title='Population by Country')
    fig.update_traces(mode='lines+markers')
    return fig


# Callback for updating the graph in Dashboard 5
@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatype-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_map(selected_datatype, selected_year):
    if selected_datatype == 'Deaths':
        tab = Death
    elif selected_datatype == 'Births':
        tab = Birth
    elif selected_datatype == 'Marriages':
        tab = Marriage
    else:
        print("Something went wrong")
        tab = Death

    query = session.query(tab, Year, Country).join(Year).join(Country)

    if selected_year:
        query = query.filter(tab.id_year == selected_year)

    query_data = query.all()

    data = []
    for tab_data, year, country in query_data:
        data.append({
            'country': country.country,
            'year': year.year,
            'measurement': tab_data.measurement,
            'country_code': country_code_map.get(country.country, None)
        })

    df = pd.DataFrame(data)

    df_grouped = df.groupby(['year', 'country', 'country_code']).agg({'measurement': 'sum'}).reset_index()

    fig = go.Figure(data=go.Choropleth(
        locations=df_grouped['country_code'],
        z=df_grouped['measurement'],
        text=df_grouped['country'],
        colorscale='Blues',
        autocolorscale=True,
        reversescale=False,
        colorbar_title=selected_datatype,
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    return fig

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    menu_layout,
    html.Div(id='page-content')
])

# Callback for routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/' or pathname == '/deaths':
        return dashboard1_layout
    elif pathname == '/births':
        return dashboard2_layout
    elif pathname == '/marriages':
        return dashboard3_layout
    elif pathname == '/population':
        return dashboard4_layout
    elif pathname == '/maps':
        return dashboard5_layout
    else:
        return html.Div([
            html.H1('404 - Page Not Found'),
            html.P('The page you are looking for does not exist.')
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)