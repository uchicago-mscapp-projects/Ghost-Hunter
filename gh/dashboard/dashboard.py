# Run this app with python -m gh and
# visit http://127.0.0.1:8060/ in your web browser.


# import libraries
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


# import data
from gh.data_viz.data_analysis import (
    merge_data_visualization,
    get_matches_percentage_data,
)

# import graph
from gh.data_viz.viz_graphs import (
    bar_graph_providertype_match,
    bar_graph_providertype_match_percentage,
    nonmatch_zicode_choropleth_graph,
)


def create_card():
    """
    Returns (dbc.Card): A Dash Card that will be information box.
    """

    # https://www.census.gov/content/dam/Census/library/publications/2023/demo/p60-281.pdf
    usa_medicaid = "18.8%"
    # https://hfs.illinois.gov/info/factsfigures/program-enrollment/cook.html
    illinois_medicaid = "30%"

    data = merge_data_visualization()

    
# ]]⁠Code
#     - Total unique Primary Care Providers
#     - Total unique specialists
# •⁠  ⁠Paula 
#     - Total numbers or searches / total
#     - Write up on the merge

    #County Care https://countycare.com/
    total_ccare = "160,277"
    primary_care = "6,600"
    specialist = "26,000"

#     - Total unique Primary Care Providers
#     - Total unique specialists

    #scrape
    total_scrape = len(data)
    match_percentage = (data["npi"].count()/len(data)*100).round(2)
    nonmatch_percentage = (data["npi"].isna().sum()/len(data)*100).round(2)

    header_style = {
        "color": "white",
        "font-weight": "bold",
        "font-family": "Roboto",
        "text-align": "center",
        "font-size": "2rem",
    }

    body_style = {
        "color": "white",
        "font-family": "Roboto",
        "text-align": "center",
        "font-size": "1.5rem",
    }

    card_content2 = [
        dbc.CardHeader("COUNTY CARES WEB", style=header_style),
        dbc.CardBody(
            [
                html.P(f"#Search results {total_ccare}", style=body_style, className="card-title"),
                html.P(
                    f"#Primary Care Providers {primary_care}",
                    style=body_style,
                    className="card-text",
                ),
                html.P(
                    f"#Specialist {specialist}",
                    style=body_style,
                    className="card-text",
                )
            ]
        ),
    ]

    card_content3 = [
        dbc.CardHeader("SCRAPE", style=header_style),
        dbc.CardBody(
            [
                html.P(
                    f"#Unique Providers {total_scrape}",
                    style=body_style,
                    className="card-title",
                ),
                html.P(
                    f"Match {match_percentage}%",
                    style=body_style,
                    className="card-text",
                ),
                html.P(
                    f"Non Match {nonmatch_percentage}%",
                    style=body_style,
                    className="card-text",
                ),
            ]
        ),
    ]

    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content2, color="#007cb9", outline=True)),
                    dbc.Col(dbc.Card(card_content3, color="#9fd3c7", outline=True)),
                ],
                className="mb-4",
            )
        ]
    )

    return cards


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"""
Creates a Dash application and adds it to a Flask server.
"""

project_title = html.H1(
    children="Ghost Hunter",
    style={
        "color": "white",
        "font-weight": "bold",
        "background-color": "#24527a",
        "font-family": "Roboto",
        "text-align": "center",
        "font-size": "5rem",
    },
)

abstract_text = """# Project Abstract

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
zip codes to look for trends across specialities and geography."""

abstract = dcc.Markdown(
    abstract_text,
    style={
        "color": "#24527a",
        "background-color": "#ececec",
        "font-family": "Roboto",
        "text-align": "center",
        "font-size": "1rem",
    },
)


info_cards = create_card()

graphs_title = html.H3(
    children="County Care Scrape",
    style={
        "color": "#007cb9",
        "font-weight": "bold",
        "background-color": "white",
        "font-family": "Roboto",
        "text-align": "center",
        "font-size": "3rem",
    },
)


# Importing data
df = merge_data_visualization()
providertype_data = get_matches_percentage_data(df, 'type')
zipcode_data = get_matches_percentage_data(df, 'zip_code')

# Importing graphs
graph1 = bar_graph_providertype_match(
    data=providertype_data,
    title="Total Matches and Non-Matches by each Provider Type",
    match_color="#9fd3c7",
    nonmatch_color="#007cb9",
)
graph2 = bar_graph_providertype_match_percentage(
    data=providertype_data,
    title="Percentage of Matches by each Provider Type",
    match_color="#9fd3c7",
)
graph3 = nonmatch_zicode_choropleth_graph(
    data=zipcode_data,
    title="Choropleth graph with the percentage of Non-Matches by Zip Code",
    nonmatch_color="blues",
)


app.layout = html.Div(
    children=[project_title, abstract, info_cards, graphs_title, graph1, graph2, graph3]
)

if __name__ == "__main__":
    app.run_server(port=8060)
