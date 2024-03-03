
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import urllib3
import json


#Data NPI
#Data scrape (County_Care)
#Data Impact (Illinoiss NPI)
#Match Data



#MEDICAID VIZ
#Medicade in USA 18.8% https://www.census.gov/content/dam/Census/library/publications/2023/demo/p60-281.pdf
#patients in county care
#% patientes in illinois 30%
# https://hfs.illinois.gov/info/factsfigures/program-enrollment/cook.html
#cook county https://hfs.illinois.gov/info/factsfigures/program-enrollment/cook.html

#PROVIDERS VIZ
# num providers (NPI) in illinois
# num providers (Impact) accept patience in Medicaid
# num providers scrape (county care)

# CountyCare offers access to more than 6,600 primary care providers, 
# 26,000 specialists and 70 hospitals in Cook County. 
# With a robust network, Cook County residents always have access to providers nearby.

#treemap cicular
#https://plotly.com/python/treemaps/
# Circlify 
# matplotlib


 


#MATCH VIZ
#Load data Match/Non-Match for visualization
df = pd.read_csv("")

#Graph 1 : Ranking of total amount of provider per provider type.
def get_total_providertype_data(df):
    '''
    Calculates the total providers for each provider type. 

    Returns: dataframe
    '''

    list_of_tuples = []

    for provider_type in df['ProviderType'].unique():
        #total for each provider type
        total = df.loc[df['ProviderType'] == provider_type].shape[0]
        list_of_tuples.append((provider_type, total))

    #sorted descending by Total
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1],reverse=True)

    data = pd.DataFrame(list_of_tuples,
                    columns=['ProviderType', 'Total'])

    return data

def bar_graph_total_providertype():
    """
    Returns (object): DCC Graph.
    """ 
    
    #Load data
    df = get_total_providertype_data(df)

    #Create a figure
    #label    
    fig = px.bar(df, x='ProviderType', y='Total',orientation='h', height=400,)

    return dcc.Graph(id=f'total_providertype', figure=fig)
    
    
    
#Graph 2: count Match - Non-match Per type provider type. 
def get_match_providertype_data(df):
    '''
    Calculates the total match and non_match providers for each 
    provider type. 

    Returns: dataframe
    '''

    list_of_tuples = []

    for provider_type in df['ProviderType'].unique():
        #total for each provider type
        df_provider = df.loc[df['ProviderType'] == provider_type]
        num_match = df_provider.loc[df_provider['Match'] == 'Match'].shape[0]
        num_nonmatch = df_provider.loc[df_provider['Match'] == 'Non-Match'].shape[0]
        list_of_tuples.append((provider_type, num_match,num_nonmatch ))

   
    data = pd.DataFrame(list_of_tuples,
                    columns=['ProviderType', 'Match', 'Non-Match'])

    return data



def bar_graph_providertype_match():
    """
    Returns (object): DCC Graph.
    """ 

    #Load data
    df = get_match_providertype_data(df)

    #Create a figure
    #label ? , title ?    
    fig = px.bar(df, x='ProviderType', y=['Match', 'Non-Match'],
                color='variable', height=400)
    
    dcc.Graph(id=f'total_match_providertype', figure=fig)

    

#Graph 3: 

def get_providertype_match_prob():
    '''
    Calculates the percentage of providers that match for each 
    provider type. 

    Returns: dataframe
    '''

    list_of_tuples = []

    for provider_type in df['ProviderType'].unique():

        df_provider = df.loc[df['ProviderType'] == provider_type]
        df_match = df_provider.loc[df_provider['Match'] == 'Match']
        prob_match = df_match.shape[0]/df_provider.shape[0]
    
        list_of_tuples.append((provider_type, prob_match))

   
    data = pd.DataFrame(list_of_tuples,
                    columns=['ProviderType', 'Prob_Match'])

    return data

def bar_graph_total_providertype():
    """
    Returns (object): DCC Graph.
    """ 
    
    #Load data
    df = get_total_providertype_data(df)

    #Create a figure
    #label    
    fig = px.bar(df, x='ProviderType', y='Prob_Match', height=400,)

    return dcc.Graph(id=f'percentage_match_providertype', figure=fig)


#mismo grafico de barras de arriba poner los porcentajes
# # https://plotly.com/python/multiple-axes/
# import plotly.graph_objects as go
# from plotly.data import tips

# df = tips()

# summed_values = df.groupby(by="day", as_index=False).sum(numeric_only=True)
# day_order_mapping = {"Thur": 0, "Fri": 1, "Sat": 2, "Sun": 3}
# summed_values["order"] = summed_values["day"].apply(lambda day: day_order_mapping[day])
# summed_values = summed_values.sort_values(by="order")

# days_of_week = summed_values["day"].values
# total_bills = summed_values["total_bill"].values
# number_of_diners = summed_values["size"].values


# fig = go.Figure(
#     data=go.Bar(
#         x=days_of_week,
#         y=number_of_diners,
#         name="Total number of diners",
#         marker=dict(color="paleturquoise"),
#     )
# )

# fig.add_trace(
#     go.Scatter(
#         x=days_of_week,
#         y=total_bills,
#         yaxis="y2",
#         name="Total bill amount",
#         marker=dict(color="crimson"),
#     )
# )

# fig.update_layout(
#     legend=dict(orientation="h"),
#     yaxis=dict(
#         title=dict(text="Total number of diners"),
#         side="left",
#         range=[0, 250],
#     ),
#     yaxis2=dict(
#         title=dict(text="Total bill amount"),
#         side="right",
#         range=[0, 2000],
#         overlaying="y",
#         tickmode="sync",
#     ),
# )

# fig.show()


#Zip non match Map
# https://plotly.com/python/county-choropleth/
#https://plotly.com/python/choropleth-maps/
#FIPS 
# http://www.champaigncountyema.org/index.php/fips

#https://medium.com/@mm.fuenteslopez/using-plotly-express-to-make-zip-code-level-choropleth-maps-a8ac8212b7ed
# https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json

def get_zicode_data(df):
    '''
    '''
    list_of_tuples = []

    for zip_code in df['Zip_code'].unique():

        df_zip = df.loc[df['ProviderType'] == zip_code]
        df_nonmatch = df_zip.loc[df_zip['Match'] == 'Non-Match']
        prob_nonmatch = df_nonmatch.shape[0]/df_zip.shape[0]
    
        list_of_tuples.append((zip_code, prob_nonmatch))

   
    data = pd.DataFrame(list_of_tuples,
                    columns=['Zipcode', 'Prob_NonMatch'])

    return data


def zicode_choropleth_graph(df):
    '''
    '''

    # import urllib3
    # import json

    df = get_zicode_data(df)

    #Illinois Zip code (gives the coordinates)
    url='https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json'
    response = urllib3.request('GET',url)
    zipcodes = response.json()

    fig = px.choropleth(df, 
                        geojson=zipcodes, 
                        locations='Zipcode', 
                        color='Prob_NonMatch',
                        color_continuous_scale="blues",
                        range_color=(0,1),
                        featureidkey="properties.ZCTA5CE10",
                        scope="usa",
                        labels={'Cluster':'Cluster_Category'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return dcc.Graph(id=f'percentage_match_providertype', figure=fig)


#https://plotly.com/python/choropleth-maps/ usar para match y nonmatch 

# from urllib.request import urlopen
# import json
# import requests

# # Nevada Zip code
# url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nv_nevada_zip_codes_geo.min.json'
# with urlopen(url) as response:
#     nv_zip_json = json.load(response)

# zip_code = []
# for i in range(len(nv_zip_json['features'])):
#     code = nv_zip_json['features'][i]['properties']['ZCTA5CE10']
#     zip_code.append(code)

# import pandas as pd
# import numpy as np
# df = pd.DataFrame({'zip_code': zip_code, 'value': np.random.randint(0,30, len(nv_zip_json['features']))})
# df['zip_code'] = df['zip_code'].astype(str)

# import plotly.express as px

# fig = px.choropleth(df,
#                     geojson= nv_zip_json,
#                     locations='zip_code',
#                     featureidkey="properties.ZCTA5CE10",
#                     color='value',
#                     color_continuous_scale="blues",
#                     projection="mercator",
#                     )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# fig.show()









