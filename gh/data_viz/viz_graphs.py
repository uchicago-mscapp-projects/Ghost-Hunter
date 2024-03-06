#import libraries
from dash import dcc
import plotly.express as px
import urllib3



#import functions
from gh.data_viz.data_analysis import merge_data_visualization, get_match_providertype_data, get_match_zipcode_data



def bar_graph_providertype_match(title, match_color, nonmatch_color):
        """
        Returns (object): DCC Graph.
        """ 
        #Load data
        df = merge_data_visualization()
        data = get_match_providertype_data(df)

        #Create a figure
        fig = px.bar(data, x=['Match', 'Non-Match'], y='Provider Type',
                     title = title,
                     color_discrete_map={
        'Match': match_color,
        'Non-Match': nonmatch_color},
                     orientation='h')
        
        return dcc.Graph(id=f'total_match_providertype', figure=fig)


def bar_graph_providertype_prob_match(title, match_color):
    """
    Returns (object): DCC Graph.
    """ 

    #Load data
    df = merge_data_visualization()
    data = get_match_providertype_data(df)

    #Create a figure   
    fig = px.bar(data, x='Provider Type', y='Prob Match', 
                 title= title,
                 color_discrete_sequence =[match_color]*len(df),  
                 range_y=(0,1))

    return dcc.Graph(id=f'percentage_match_providertype', figure=fig)



def zicode_choropleth_graph():
    '''
    '''
    df = merge_data_visualization()
    data =  get_match_zipcode_data(df)

    #Illinois Zip code (gives the coordinates)
    url='https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json'
    response = urllib3.request('GET',url)
    zipcodes = response.json()

    fig = px.choropleth(data, 
                        geojson=zipcodes, 
                        locations='Zip Code', 
                        color='Prob Non-Match',
                        color_continuous_scale="blues",
                        range_color=(0,1),
                        featureidkey="properties.ZCTA5CE10",
                        scope='usa', 
                        labels={'Cluster':'Cluster_Category'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    return dcc.Graph(id=f'percentage_match_providertype', figure=fig)


