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
    
#     html.Div([
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df2)




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


from dash import Dash, html, dcc

app = Dash(__name__)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text)
])

if __name__ == '__main__':
    app.run(debug=True)


