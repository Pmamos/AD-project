import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Base, Year, Age, Death, Continent, Country, Birth, Marriage, db_string

# def fix_country_name(name):
#     if name == 'Dem. Rep. of the Congo': name = 'Congo, the Democratic Republic of the'
#     elif name == 'Iran (Islamic Republic of)': name = 'Iran, Islamic Republic of'
#     #elif name == 'Viet Nam': name = 'Vietnam'
#
#     return name

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

# Create a Dash application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Database connection
engine = create_engine(db_string)  # Update with your database path
Session = sessionmaker(bind=engine)
session = Session()

years = session.query(Year).all()
year_df = pd.DataFrame([(y.id_year, y.year) for y in years], columns=['id_year', 'year'])

# Define the top menu layout
menu_layout = html.Div([
    html.H1('Map dashboard'),
], style={'display': 'flex', 'gap': '20px', 'justify-content': 'center', 'padding': '20px', 'background': '#f0f0f0'})

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    menu_layout,

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

    dcc.Graph(id='map-graph'),
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatype-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_map(selected_datatype, selected_year):
    if selected_datatype == 'Deaths': tab = Death
    elif selected_datatype == 'Births': tab = Birth
    elif selected_datatype == 'Marriages': tab = Marriage
    else:
        print("Something went wrong")
        tab = Death

    query = session.query(tab, Year, Country).join(Year).join(Country)

    if selected_year:
        query = query.filter(tab.id_year == selected_year)

    query_data = query.all()

    #country_to_code = pd.read_csv('countries_codes_and_coordinates.csv')
    data = []
    for tab_data, year, country in query_data:
        data.append({
            'country': country.country,
            'year': year.year,
            'measurement': tab_data.measurement,
            'country_code': country_code_map[country.country]
            #'country_code': country_to_code.loc[country_to_code['Country'] == fix_country_name('Poland')]['Alpha-3 code'].item().split('\"')[-2]
        })
    df = pd.DataFrame(data)

    # Group data by year, country to avoid duplicate entries
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
    ))

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
