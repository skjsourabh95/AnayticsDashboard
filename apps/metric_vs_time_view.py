import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import common.filtering as filtering
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from app import app
from common.header import header_layout
from common.data import df_mortality
from common.mapping import race_options, age_ranges_options
from common.mapping import sex_options
from common.mapping import ethnicity_options
from common.mapping import intent_options
from common.mapping import causes_options
from common.mapping import county_options
from common.mapping import state_options

filter1 = filter2 = None

# create dropdown options for VARIABLES
var_options = []
for key in list(df_mortality.columns):
    var_options.append({"label":key.title(), "value":key.title()})


metric_vs_time_dash = html.Div([
	html.Div([
        dcc.Tabs([
            dcc.Tab(label='Filter One', children=[
                html.Div([
                    html.Div([
                        html.Label("Sex"),
                        dcc.Dropdown(
                            id="Sex",
                            options=sex_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("Race"),
                        dcc.Dropdown(
                            id="Race",
                            options=race_options,
                            placeholder="Select",
                            multi=True
                        )
                    ], className="two columns"),
                    html.Div([
                        html.Label("Ethnicity"),
                        dcc.Dropdown(
                            id="Ethnicity",
                            options=ethnicity_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("Intent"),
                        dcc.Dropdown(
                            id="Intent",
                            options=intent_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("State"),
                        dcc.Dropdown(
                            id="State",
                            options=state_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("County"),
                        dcc.Dropdown(
                            id="County",
                            options=county_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                ], className="row"),

                html.Div([
                    html.Div([
                        html.Label("Causes"),
                        dcc.Dropdown(
                            id="Cause",
                            options=causes_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="three columns"),
                    html.Div([
                        html.Label("Age"),
                        dcc.Dropdown(
                            id="Age",
                            options=age_ranges_options,
                            placeholder="Select",
                            multi=True
                        ),

                    ], className="three columns"),
                    html.Div([
                        html.Label("Year"),
                        dcc.RangeSlider(
                            id="Year",
                            min=2000,
                            max=2020,
                            step=1,
                            value=[2000, 2020],
                            marks={
                                2000:"2000",
                                2005:"2005",
                                2010:"2010",
                                2015:"2015",
                                2020:"2020",
                            }
                        ),
                    ], className="three columns"),
                ], className="row")
            ]),

            dcc.Tab(label='Filter Two', children=[
                html.Div([
                    html.Div([
                        html.Label("Sex"),
                        dcc.Dropdown(
                            id="Sex2",
                            options=sex_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("Race"),
                        dcc.Dropdown(
                            id="Race2",
                            options=race_options,
                            placeholder="Select",
                            multi=True
                        )
                    ], className="two columns"),
                    html.Div([
                        html.Label("Ethnicity"),
                        dcc.Dropdown(
                            id="Ethnicity2",
                            options=ethnicity_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("Intent"),
                        dcc.Dropdown(
                            id="Intent2",
                            options=intent_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("State"),
                        dcc.Dropdown(
                            id="State2",
                            options=state_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                    html.Div([
                        html.Label("County"),
                        dcc.Dropdown(
                            id="County2",
                            options=county_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="two columns"),
                ], className="row"),

                html.Div([
                    html.Div([
                        html.Label("Causes"),
                        dcc.Dropdown(
                            id="Cause2",
                            options=causes_options,
                            placeholder="Select",
                            multi=True
                        ),
                    ], className="three columns"),
                    html.Div([
                        html.Label("Age"),
                        dcc.Dropdown(
                            id="Age2",
                            options=age_ranges_options,
                            placeholder="Select",
                            multi=True
                        ),

                    ], className="three columns"),
                    html.Div([
                        html.Label("Year"),
                        dcc.RangeSlider(
                            id="Year2",
                            min=2000,
                            max=2020,
                            step=1,
                            value=[2000, 2020],
                            marks={
                                2000:"2000",
                                2005:"2005",
                                2010:"2010",
                                2015:"2015",
                                2020:"2020",
                            }
                        ),
                    ], className="three columns"),
                ], className="row")
            ])
        ])
    ]),

    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(
                    id="Deaths1"
                )
            ], className="row"),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Statistics', children=[
                        html.Div([
                            html.Label("Variable"),
                            dcc.Dropdown(
                                id="Variable1",
                                options=var_options,
                                value="Age"
                            ),
                        ], className="row"),

                        html.Div([
                            dcc.Graph(
                                id='Distribution1'
                            )
                        ])
                    ]),
                    dcc.Tab(label='Anomalies', children=[
                        html.Div([
                            dcc.Graph(
                                id='Anomalies1'
                            )
                        ])
                    ]),
                    dcc.Tab(label='Trends', children=[
                        html.Div([
                            dcc.Graph(
                                id='Trend1'
                            )
                        ])
                    ]),
                ])
            ], className="row")
        ], className="six columns"),

        html.Div([
            html.Div([
                dcc.Graph(
                    id="Deaths2"
                )
            ], className="row"),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Statistics', children=[
                        html.Div([
                            html.Label("Variable"),
                            dcc.Dropdown(
                                id="Variable2",
                                options=var_options,
                                value="Age"
                            ),
                        ], className="row"),

                        html.Div([
                            dcc.Graph(
                                id='Distribution2'
                            )
                        ])
                    ]),
                    dcc.Tab(label='Anomalies', children=[
                        html.Div([
                            dcc.Graph(
                                id='Anomalies2'
                            )
                        ])
                    ]),
                    dcc.Tab(label='Trends', children=[
                        html.Div([
                            dcc.Graph(
                                id='Trend2'
                            )
                        ])
                    ]),
                ])
            ], className="row")
        ], className="six columns")
    ], className="row")
])
# end metric-vs-time-dash

layout = html.Div([
    header_layout,
    html.Br(),
	metric_vs_time_dash
])

@app.callback(
    [dash.dependencies.Output("Deaths1", "figure"),
    dash.dependencies.Output("Distribution1", "figure"),
    dash.dependencies.Output("Anomalies1", "figure"),
    dash.dependencies.Output("Trend1", "figure")],
    [dash.dependencies.Input("Year", "value"),
    dash.dependencies.Input("Age", "value"),
    dash.dependencies.Input("Cause", "value"),
    dash.dependencies.Input("Intent", "value"),
    dash.dependencies.Input("Ethnicity", "value"),
    dash.dependencies.Input("Sex", "value"),
    dash.dependencies.Input("Race", "value"),
    dash.dependencies.Input("State", "value"),
    dash.dependencies.Input("County", "value"),
    dash.dependencies.Input("Variable1", "value")]
)

def update_fig(years, ages, cause, intent, ethnicity, sex, race, state, county, variable):
    # filter one
    filter1 = filtering.no_filter(df_mortality)
    filter1 = filtering.filter_year(df_mortality, filter1, years[0], years[1])
    filter1 = filtering.filter_age_range(df_mortality, filter1, ages)
    filter1 = filtering.filter_cause(df_mortality, filter1, cause)
    filter1 = filtering.filter_intent(df_mortality, filter1, intent)
    filter1 = filtering.filter_ethnicity(df_mortality, filter1, ethnicity)
    filter1 = filtering.filter_sex(df_mortality, filter1, sex)
    filter1 = filtering.filter_race(df_mortality, filter1, race)
    filter1 = filtering.filter_state(df_mortality, filter1, state)
    filter1 = filtering.filter_county(df_mortality, filter1, county)

    # apply filter one
    df_filtered1 = df_mortality[filter1]

    # compute total deaths aggregated per year
    deaths1 = df_filtered1.groupby(["year"])["deaths"].sum()

    # compute trends
    y = deaths1.values
    lr = LinearRegression()
    x = np.array(list(range(len(y)))).reshape(-1,1)
    lr.fit(x,y)
    y_reg = lr.predict(x)
    print("SLOPE:",lr.coef_[0])

    # plot anomalies
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(name='Points', x=deaths1.index, y=y, mode='markers'))
    fig2.add_trace(go.Scatter(name='Regression line', x=deaths1.index, y=y_reg, mode='lines'))

    # compute anomalies
    LAG = 5
    y = deaths1.pct_change().values*100
    ma = np.zeros(len(y))
    std = np.zeros(len(y))
    for i in range(LAG,len(y)):
        ma[i] = np.mean(y[i-LAG+1:i+1])
        std[i] = np.std(y[i-LAG+1:i+1])

    # plot anomalies
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(name='Percentage change', x=deaths1.index, y=deaths1.pct_change().values*100, mode='markers'))
    fig3.add_trace(go.Scatter(name='Moving average', x=deaths1.index, y=ma, mode='lines', line_color="#ff9900"))
    fig3.add_trace(go.Scatter(name='Upper bound', x=deaths1.index, y=ma + std, fill=None, mode='lines', line_color="#ff9900"))
    fig3.add_trace(go.Scatter(name='Lower bound', x=deaths1.index, y=ma - std, fill='tonexty', mode='lines', line_color="#ff9900"))

    # create figure for line plot
    return go.Figure(data=go.Scatter(x=deaths1.index, y=deaths1, name="Filter one", line_color="#0000ff")),\
            go.Figure(data=[go.Histogram(x=df_filtered1[variable.lower()], marker_color='rgb(0, 0, 255)')]),\
            fig3,\
            fig2

@app.callback(
    [dash.dependencies.Output("Deaths2", "figure"),
    dash.dependencies.Output("Distribution2", "figure"),
    dash.dependencies.Output("Anomalies2", "figure"),
    dash.dependencies.Output("Trend2", "figure")],
    [dash.dependencies.Input("Year2", "value"),
    dash.dependencies.Input("Age2", "value"),
    dash.dependencies.Input("Cause2", "value"),
    dash.dependencies.Input("Intent2", "value"),
    dash.dependencies.Input("Ethnicity2", "value"),
    dash.dependencies.Input("Sex2", "value"),
    dash.dependencies.Input("Race2", "value"),
    dash.dependencies.Input("State2", "value"),
    dash.dependencies.Input("County2", "value"),
    dash.dependencies.Input("Variable2", "value")]
)

def update_fig(years2, ages2, cause2, intent2, ethnicity2, sex2, race2, state2, county2, variable):
    # filter two
    filter2 = filtering.no_filter(df_mortality)
    filter2 = filtering.filter_year(df_mortality, filter2, years2[0], years2[1])
    filter2 = filtering.filter_age_range(df_mortality, filter2, ages2)
    filter2 = filtering.filter_cause(df_mortality, filter2, cause2)
    filter2 = filtering.filter_intent(df_mortality, filter2, intent2)
    filter2 = filtering.filter_ethnicity(df_mortality, filter2, ethnicity2)
    filter2 = filtering.filter_sex(df_mortality, filter2, sex2)
    filter2 = filtering.filter_race(df_mortality, filter2, race2)
    filter2 = filtering.filter_state(df_mortality, filter2, state2)
    filter2 = filtering.filter_county(df_mortality, filter2, county2)

    # apply filter one
    df_filtered2 = df_mortality[filter2]

    # compute total deaths aggregated per year
    deaths2 = df_filtered2.groupby(["year"])["deaths"].sum()

    # compute trends
    y = deaths2.values
    lr = LinearRegression()
    x = np.array(list(range(len(y)))).reshape(-1,1)
    lr.fit(x,y)
    y_reg = lr.predict(x)
    print("SLOPE:",lr.coef_[0])

    # plot anomalies
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(name='Points', x=deaths2.index, y=y, mode='markers'))
    fig2.add_trace(go.Scatter(name='Regression line', x=deaths2.index, y=y_reg, mode='lines'))

    # compute anomalies
    LAG = 5
    y = deaths2.pct_change().values*100
    ma = np.zeros(len(y))
    std = np.zeros(len(y))
    for i in range(LAG,len(y)):
        ma[i] = np.mean(y[i-LAG+1:i+1])
        std[i] = np.std(y[i-LAG+1:i+1])

    # plot anomalies
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(name='Percentage change', x=deaths2.index, y=deaths2.pct_change().values*100, mode='markers'))
    fig3.add_trace(go.Scatter(name='Moving average', x=deaths2.index, y=ma, mode='lines', line_color="#ff9900"))
    fig3.add_trace(go.Scatter(name='Upper bound', x=deaths2.index, y=ma + std, fill=None, mode='lines', line_color="#ff9900"))
    fig3.add_trace(go.Scatter(name='Lower bound', x=deaths2.index, y=ma - std, fill='tonexty', mode='lines', line_color="#ff9900"))

    # create figure for line plot
    return go.Figure(data=go.Scatter(x=deaths2.index, y=deaths2, name="Filter one", line_color="#ff0000")),\
            go.Figure(data=[go.Histogram(x=df_filtered2[variable.lower()], marker_color='rgb(255, 0, 0)')]),\
            fig3,\
            fig2
