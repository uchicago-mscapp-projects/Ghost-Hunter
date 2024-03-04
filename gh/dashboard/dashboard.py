# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


#import libraries
import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import urllib3
import json
import circlify
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc

#import graph
from gh.data_viz.viz_graphs import bar_graph_providertype_match, bar_graph_providertype_prob_match, zicode_choropleth_graph

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"""
Creates a Dash application and adds it to a Flask server.
"""


def create_card():
    """
    Returns (dbc.Card): A Dash Card that will be information box. 
    """ 

    prov_il = 1000
    prov_medicaid = 500
    prov_county_care = 100

    
    # https://www.census.gov/content/dam/Census/library/publications/2023/demo/p60-281.pdf
    usa_medicaid = "18.8%"
    # https://hfs.illinois.gov/info/factsfigures/program-enrollment/cook.html
    illinois_medicaid = "30%"

    total_scrape = 100
    total_match = "50%"
    total_nonmatch = "50%"


    header_style = {"color": "#0092ca", 
            "font-weight": "bold",
            "background-color":"white",
            "font-family" :"Roboto",
            "text-align" : "center",
            "font-size": "2rem"}
    
    body_style = {"color": "#757a79", 
            "background-color":"white",
            "font-family" :"Roboto",
            "text-align" : "center",
            "font-size": "1.5rem"}

    card_content1 = [
        dbc.CardHeader("TOTAL PROVIDERS", style=header_style),
        dbc.CardBody(
            [
                html.P(f"Illinois {prov_il}", style=body_style, className="card-title"),
                html.P(f"Accept Medicaid(Illinois) {prov_medicaid}", style=body_style,
                    className="card-text",
                ),
                html.P(f"County Care (Medicaid) {prov_county_care}", style=body_style,
                    className="card-text",
                )
            ]
        ),
    ]

    card_content2 = [
        dbc.CardHeader("MEDICAID PATIENTES", style=header_style),
        dbc.CardBody(
            [
                html.P(f"USA {usa_medicaid}", style=body_style, className="card-title"),
                html.P(f"Illinois {illinois_medicaid}", style=body_style,
                    className="card-text",
                ),
            ]
        ),
    ]


    card_content3 = [
        dbc.CardHeader("COUNTY CARE SCRAPE",style=header_style),
        dbc.CardBody(
            [
                html.P(f"Total scrape {total_scrape}", style=body_style, className="card-title"),
                html.P(f"Match {total_match}", style=body_style,
                    className="card-text",
                ),
                html.P(f"Non Match {total_nonmatch}", style=body_style,
                    className="card-text",
                )
            ]
        ),
    ]

    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content1, color="#5dacbd", outline=True)),
                    dbc.Col(
                        dbc.Card(card_content2, color="#a7bcb9", outline=True)
                    ),
                    dbc.Col(dbc.Card(card_content3, color=" #e0ebeb", outline=True)),
                ],
                className="mb-4",
            )
        ]
    )
    
    return cards


abstract_text = '''# Project Abstract

Our application audits the medicaid network of County Care, one of Illinois five 
Medicaid Managed Care Organizations to see how what percentage of [County Care’s](https://countycare.valence.care/member/#findAProvider) 
network can be independently verified. First, we scrape County Care’s find a 
provider tool  to construct a database which presents a sample of their health care service provider 
network.  Second we attempt to locate each provider listed in County Care’s network 
in the State of Illinois’ [IMPACT data](https://ext2.hfs.illinois.gov/hfsindprovdirectory/) 
which tracks all providers approved to bill Illinois Medicaid. Finally we attempt 
to identify unmatched providers in the [National NPI Registry](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination)  
which is a national data base of all health care providers. From this analysis we 
estimate groups of providers that while listed in County Care’s directory are not 
actually seeing or billing Medicaid patients, and whose presence in County Care’s 
directory is misleading to patients and inflates the strength of their network. 
Finally we examine these estimates against sub-groups of medical providers and across 
zip codes to look for trends across specialities and geography.'''

abstract = dcc.Markdown(abstract_text, style={"color": "#24527a",
                   "background-color":"#ececec",
                   "font-family" :"Roboto",
                   "text-align" : "center",
                   "font-size": "1rem"})
info_cards = create_card() 
graph1 = bar_graph_providertype_match('Matches by Provider Type', '#9fd3c7', '#007cb9')
graph2 = bar_graph_providertype_prob_match('Probability of Macth for Provider Type','#9fd3c7')
graph3 = zicode_choropleth_graph(df)

title = html.H1(children='Ghost Hunter', 
            style={"color": "#24527a", 
                   "font-weight": "bold",
                   "background-color":"white",
                   "font-family" :"Roboto",
                   "text-align" : "center",
                   "font-size": "8rem"})

graph_title = html.H3(children='County Care Scrape', 
            style={"color": "#007cb9", 
                   "font-weight": "bold",
                   "background-color":"white",
                   "font-family" :"Roboto",
                   "text-align" : "center",
                   "font-size": "4rem"})

app.layout = html.Div(children=[
    title,
    abstract,
    info_cards,
    graph_title, 
    graph1,
    graph2,
    graph3
    
])

if __name__ == '__main__':
    app.run_server(port=8050)