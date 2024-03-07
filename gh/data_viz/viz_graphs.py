# import libraries
from dash import dcc
import plotly.express as px
import urllib3


def bar_graph_providertype_match(data, match_color, nonmatch_color):
    """
    Create a graph bar with the total match and non-match for each provider type.

    Inputs:
    data (dataframe)
    title (str)
    match_color (str)
    nonmatch_color(str)

    Returns (object): DCC Graph.
    """

    fig = px.bar(
        data,
        x=['Match', 'Non-Match'],
        y='type',
        color_discrete_map={'Match': match_color, 'Non-Match': nonmatch_color},
        orientation="h",
    )
    fig.update_xaxes(tickformat=",")

    return dcc.Graph(id=f"total_match_providertype", figure=fig)


def bar_graph_providertype_match_percentage(data, match_color):
    """
    Create a graph bar with the percentage matches for each provider type.

    Inputs:
    data (dataframe)
    title (str)
    match_color (str)

    Returns (object): DCC Graph.
    """

    fig = px.bar(
        data,
        x='type',
        y='Percentage Match',
        color_discrete_sequence=[match_color] * len(data),
        range_y=(0, 100), text_auto=True
    )
    fig.update_xaxes(tickformat=".2%")
    
    return dcc.Graph(id=f"percentage_match_providertype", figure=fig)


def nonmatch_zicode_choropleth_graph(data, nonmatch_color):
    """
    Create a choropleth graph with all the zip code of the providers address and
    color with the scale for nonmatches percentage.

    Inputs:
    data (dataframe)
    title (str)
    color (str)

    Returns (object): DCC Graph.
    """

    # Load Illinois zipcode coordinates
    url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json"
    response = urllib3.request("GET", url)
    zipcodes = response.json()

    # Create a figure
    fig = px.choropleth(
        data,
        geojson = zipcodes,
        locations = 'zip_code',
        color='Percentage Non-Match',
        color_continuous_scale = nonmatch_color,
        range_color=(0, 100),
        featureidkey="properties.ZCTA5CE10",
        scope="usa",
        labels={"Cluster": "Cluster_Category"},
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return dcc.Graph(id=f"nonmatch_zipcode_graph", figure=fig)

