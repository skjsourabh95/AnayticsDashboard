import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import metric_vs_time_view, map_view, table_view, data_view
from common.header import header_layout

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# index layout
app.layout = url_bar_and_content_div

# "complete" layout, dynamic layout validation for multi page app
app.validation_layout = html.Div([
    url_bar_and_content_div,
    header_layout,
    metric_vs_time_view.layout,
    map_view.layout,
    table_view.layout,
    data_view.layout
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/metric-vs-time-view':
        return metric_vs_time_view.layout
    elif pathname == '/apps/map-view':
        return map_view.layout
    elif pathname == '/apps/table-view':
        return table_view.layout
    elif pathname == '/apps/data-view':
        return data_view.layout
    else:
        return metric_vs_time_view.layout


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', threaded=True)

