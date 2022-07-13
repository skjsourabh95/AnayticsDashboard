import dash_html_components as html
import dash_core_components as dcc


header_layout = html.Div([
	html.Div([
		html.Div([
			html.H2(children="Fatal Injury and Violence Analytics"),
		], className="six columns",style={'color':'white'}),
		html.Div([
			html.Div([
				html.Div([
					dcc.Link('Metric vs time view', href='/apps/metric-vs-time-view'),
				],className="three columns"),
				html.Div([
					dcc.Link('Map view', href='/apps/map-view'),
				],className="three columns"),
				html.Div([
					dcc.Link('Table view', href='/apps/table-view'),
				],className="three columns"),
				html.Div([
					dcc.Link('Data view', href='/apps/data-view'),
				],className="three columns")
			], className="row"),
		], className="six columns"),
	],className="row",
	style={'background-color':'#212121',
		"textAlign": "center",
		"justify-content": "center",
		"align-items": "center"})
])
