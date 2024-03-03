# https://stackoverflow.com/questions/63459424/how-to-add-multiple-graphs-to-dash-app-on-a-single-browser-page


# from dash import Dash, html, dcc
# import plotly.express as px
# import pandas as pd

# # import dash
# # import dash_core_components as dcc
# # import dash_html_components as html
# from dash.dependencies import Input, Output
# # import pandas as pd
# import plotly.express as px

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df_bar = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     # All elements from the top of the page
#     html.Div([
#         html.H1(children='Hello Dash'),

#         html.Div(children='''
#             Dash: A web application framework for Python.
#         '''),

#         dcc.Graph(
#             id='graph1',
#             figure=fig
#         ),  
#     ]),
#     # New Div for all elements in the new 'row' of the page
#     html.Div([
#         html.H1(children='Hello Dash'),

#         html.Div(children='''
#             Dash: A web application framework for Python.
#         '''),

#         dcc.Graph(
#             id='graph2',
#             figure=fig
#         ),  
#     ]),
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")

# Data for the tip-graph
df_tip = px.data.tips()

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([ 
        dcc.Graph(id='tip-graph'),
        html.Label([
            "colorscale",
            dcc.Dropdown(
                id='colorscale-dropdown', clearable=False,
                value='bluyl', options=[
                    {'label': c, 'value': c}
                    for c in px.colors.named_colorscales()
                ])
        ]),
    ])
])

# Callback function that automatically updates the tip-graph based on chosen colorscale
@app.callback(
    Output('tip-graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_tip_figure(colorscale):
    return px.scatter(
        df_color, x="total_bill", y="tip", color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )

if __name__ == '__main__':
    app.run_server(debug=True)


# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.


# from dash import Dash, html, dcc
# import plotly.express as px
# import pandas as pd

# app = Dash(__name__)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Provider Type": ["Behavioral Health", "Hospitals", "Surgery", "Surgery", "Hospitals", "Behavioral Health"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "Match": ["Total", "Total", "Total", "Match", "Match", "Match"]


# })

# fig = px.bar(df, x="Provider Type", y="Amount", color="Match", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Ghost Hunters'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
    
# ])

# if __name__ == '__main__':
#     app.run(debug=True)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# from dash import Dash, html
# import pandas as pd

# df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


# app = Dash(__name__)

# app.layout = html.Div([
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df2)
# ])

# if __name__ == '__main__':
#     app.run(debug=True)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# from dash import Dash, dcc, html
# import plotly.express as px
# import pandas as pd


# app = Dash(__name__)

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

# fig = px.scatter(df, x="gdp per capita", y="life expectancy",
#                  size="population", color="continent", hover_name="country",
#                  log_x=True, size_max=60)

# app.layout = html.Div([
#     dcc.Graph(
#         id='life-exp-vs-gdp',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run(debug=True)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# from dash import Dash, html, dcc

# app = Dash(__name__)

# markdown_text = '''
# ### Dash and Markdown

# Dash apps can be written in Markdown.
# Dash uses the [CommonMark](http://commonmark.org/)
# specification of Markdown.
# Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
# if this is your first introduction to Markdown!
# '''

# app.layout = html.Div([
#     dcc.Markdown(children=markdown_text)
# ])

# if __name__ == '__main__':
#     app.run(debug=True)


