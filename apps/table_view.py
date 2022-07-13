import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd

from app import app, cache
from common import filtering
from common.data import year_options, year_options_max, year_options_min, get_grouped_data
from common.header import header_layout
from common.mapping import intent_options, causes_options, state_options, region_options, map_scale_options, analytics_options
from common.metrics import cusum

import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

filter_layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Label('Intent'),
                dcc.Dropdown(
                    id='Intent',
                    options=intent_options,
                    placeholder='Select',
                    multi=True
                ),
            ], className='six columns'),
            html.Div([
                html.Label('Causes'),
                dcc.Dropdown(
                    id='Cause',
                    options=causes_options,
                    placeholder='Select',
                    multi=True
                ),
            ], className='six columns'),
        ], className='row'),
    ], id='filter_layout')
])

filter2_layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Label('Show all:'),
                dcc.Checklist(
                    id='ShowAll',
                    options=[
                        {'label': '   Ages         ', 'value': 'ages'},
                        {'label': '   Races        ', 'value': 'races'},
                        {'label': '   Genders      ', 'value': 'genders'},
                        {'label': '   Ethnicities  ', 'value': 'etnicitys'}
                    ],
                    value=[],
                    labelStyle={'display': 'inline-block'}
                )

            ], className='ten columns'),
        ], className='row'),
    ], id='filter_layout')
])

year_choice_layout = html.Div([
    html.Div([
        html.Label('Year'),
        dcc.Dropdown(
            id='year',
            options=year_options[1:],
            value=year_options_max,
            clearable=False,
            multi=False
        )
    ], className='three columns')
], id='year_choice', className='ten columns')

year_range_layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Comparison Years'),
            dcc.RangeSlider(
                id='years_comparison',
                min=year_options_min,
                max=year_options_max,
                step=1,
                value=[year_options_max - 1, year_options_max - 1],
                marks={
                    year_options_min: str(year_options_min),
                    2000: '2000',
                    2005: '2005',
                    2010: '2010',
                    2015: '2015',
                    year_options_max: str(year_options_max),
                }
            )
        ]),
    ], className='row'),
    html.Div([
        html.Div([
            html.Label('Base Years'),
            dcc.RangeSlider(
                id='years_base',
                min=year_options_min,
                max=year_options_max,
                step=1,
                value=[year_options_max, year_options_max],
                marks={
                    year_options_min: str(year_options_min),
                    2000: '2000',
                    2005: '2005',
                    2010: '2010',
                    2015: '2015',
                    year_options_max: str(year_options_max),
                }
            )
        ]),
    ], className='row'),
], id='year_range', style={'display': 'none'})


COMPARISON_METHOD_OPTIONS = [{'value': 'Relative', 'label': 'Relative % increase/decrease'},
                             {'value': 'HLM', 'label': 'Historical limits method'},
                             {'value': 'CUSUM1', 'label': 'CUSUM method'}]

COLUMNS = [{'name': 'Location', 'id': 'location'},
           {'name': 'Age', 'id': 'age_range'},
           {'name': 'Race', 'id': 'race'},
           {'name': 'Gender', 'id': 'sex'},
           {'name': 'Ethnicity', 'id': 'ethnicity'},
           {'name': 'Relative %', 'id': 'relative'}]


layout = html.Div([
    header_layout,
    html.Br(),
    html.Div([
        html.Div([
            html.Label('', id='error', style={'color': 'red', 'font-weight': 'bold'}),
        ],
        id='alert', hidden=True,  className='row'),
        html.Div([
            html.Div([
                html.Label('Detail level'),
                dcc.RadioItems(
                    id='tab_scale',
                    options=map_scale_options,
                    value='state'
                ),
            ], className='two columns'),
            html.Div([
                html.Label('Analytics options'),
                dcc.RadioItems(
                    id='analytics_option',
                    options=analytics_options[:-1],
                    value='last_year'
                ),
            ], className='four columns'),
            html.Div([
                html.Label('Comparison method'),
                dcc.RadioItems(
                    id='metric',
                    options=COMPARISON_METHOD_OPTIONS,
                    value='Relative',
                ),
            ], className='four columns'),

            html.Div([
                dcc.Dropdown(
                    id='limit',
                    options=[{'value': 10, 'label': 'Top 10'},
                             {'value': 50, 'label': 'Top 50'},
                             {'value': 100, 'label': 'Top 100'}],
                    value=10,
                    clearable=False,
                    multi=False
                ),
            ], className='two columns'),
        ], className='row', style={'border-top': '2px solid lightgray', 'padding-top': '1em'}),

        html.Div([
            html.Div([
                html.Label('State'),
                dcc.Dropdown(
                    id='State',
                    options=state_options,
                    placeholder='Select',
                    multi=True
                ),
            ], id='state_choice', className='two columns'),
            html.Div([
                html.Label('Region'),
                dcc.Dropdown(
                    id='Region',
                    options=region_options,
                    placeholder='Select',
                    multi=True
                ),
            ], id='state_choice', className='two columns'),
            html.Div([
                year_choice_layout,
                year_range_layout,
            ], className='four columns'),
            html.Div([
                html.Label('Summary'),
                html.Div(id='tv_summary'),
            ], className='four columns'),
        ], className='row', style={'margin-top': '1ex', 'margin-bottom': '1ex'}),

        filter_layout,
        filter2_layout

    ], className='ten columns', style={'border-bottom': '2px solid lightgray', 'padding-bottom': '10px'}),

    html.Div([
        dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="loading-output-1")
        ),
    ]),
    html.Div([
        html.H4(children=[html.Div(id='table_inc_label', style={'display': 'inline'})]),
        dash_table.DataTable(id='table_inc',
                             columns=COLUMNS,
                             style_cell_conditional=[
                                 {'if': {'column_id': 'location'},
                                  'width': '40%', 'textAlign': 'left'},
                                 {'if': {'column_id': 'age_range'},
                                  'width': '10%', 'textAlign': 'center'},
                                 {'if': {'column_id': 'race'},
                                  'width': '10%', 'textAlign': 'left'},
                                 {'if': {'column_id': 'sex'},
                                  'width': '10%', 'textAlign': 'left'},
                                 {'if': {'column_id': 'ethnicity'},
                                  'width': '20%', 'textAlign': 'left'},
                                 {'if': {'column_id': 'relative'},
                                  'width': '10%'},
                             ],
                             tooltip_delay=0,
                             tooltip_duration=None
                             ),

        html.Div([
            html.H4(children=[html.Div(id='table_dec_label', style={'display': 'inline'})]),
            dash_table.DataTable(id='table_dec',
                                 columns=COLUMNS,
                                 style_cell_conditional=[
                                     {'if': {'column_id': 'location'},
                                      'width': '40%', 'textAlign': 'left'},
                                     {'if': {'column_id': 'age_range'},
                                      'width': '10%', 'textAlign': 'center'},
                                     {'if': {'column_id': 'race'},
                                      'width': '10%', 'textAlign': 'left'},
                                     {'if': {'column_id': 'sex'},
                                      'width': '10%', 'textAlign': 'left'},
                                     {'if': {'column_id': 'ethnicity'},
                                      'width': '20%', 'textAlign': 'left'},
                                     {'if': {'column_id': 'relative'},
                                      'width': '10%'},
                                 ])
        ], style={'width': '100%'}, id='datatable-container')

    ], className='ten columns')

])


def format_tooltips(metric, df, years1, years2):
    """
    Generate Markdown tooltips with death counts for given years
    from DataFrame.
    """

    if 'MAX_year' in df and metric == 'HLM':
        df = df[[years1, years2, 'SD', 'MAX_year']]
        for deaths1, deaths2, sd, max_year in df.itertuples(index=False):
            tt = (F'\n|      Year      |     Deaths     |      SD      |    MaxYear   '
                  F'\n|----------------|----------------|--------------|--------------'
                  F'\n|    {years1}    |  {deaths1:,g}  |    {sd:g}    |              '
                  F'\n|    {years2}    |  {deaths2:,g}  |              |  {max_year}  ')
            yield {'relative': {'value': tt, 'type': 'markdown'}}
    elif 'SD' in df and metric == 'HLM':
        df = df[[years1, years2, 'SD']]
        for deaths1, deaths2, sd in df.itertuples(index=False):
            tt = (F'\n|      Year      |     Deaths     |      SD      '
                  F'\n|----------------|----------------|--------------'
                  F'\n|    {years1}    |  {deaths1:,g}  |    {sd:g}    '
                  F'\n|    {years2}    |  {deaths2:,g}  |              ')
            yield {'relative': {'value': tt, 'type': 'markdown'}}
    else:
        df = df[[years1, years2]]
        for deaths1, deaths2 in df.itertuples(index=False):
            tt = (F'\n|      Year      |     Deaths     '
                  F'\n|----------------|----------------'
                  F'\n|    {years1}    |  {deaths1:,g}  '
                  F'\n|    {years2}    |  {deaths2:,g}  ')
            yield {'relative': {'value': tt, 'type': 'markdown'}}


@cache.memoize()
def populate_table_data(tab_scale, analytics_option, year, years_base, years_comparison,
                        cause, intent, state, region, show_all, limit, metric):
    """
        Creates and caches data for a increases/decreases tables
    """
    alert_value = ''
    error = False

    year1 = year - 1
    year2 = year

    if tab_scale == 'county_fips':
        _, df, _ = get_grouped_data()
        location = 'County_Name_Full'
    elif tab_scale == 'region':
        _, _, df = get_grouped_data()
        location = 'Region_Name_Full'
    else:
        df, _ , _= get_grouped_data()
        location = 'State_name'
    
    df_filtered = filtering.apply_filter(df, 'state', state)
    df_filtered = filtering.apply_filter(df, 'region', region)
    df_filtered = filtering.apply_filter(df_filtered, 'intent', intent)
    df_filtered = filtering.apply_filter(df_filtered, 'cause', cause)

    if metric in ['HLM', 'CUSUM1']:
        if years_comparison[0] == years_comparison[1]:
            alert_value = 'Comparison years must be different.'
            error = True
            return None, None, None, None, None, None, None, None, None, alert_value, not error, ''

    if analytics_option == 'year_range':

        year1 = f'{years_comparison[0]}-{years_comparison[1]}'
        year2 = f'{years_base[0]}-{years_base[1]}'

        if years_comparison[0] == years_comparison[1]:
            year1 = years_comparison[0]
        if years_base[0] == years_base[1]:
            year2 = years_base[0]

        if year1 == year2:
            alert_value = 'Comparison and base years must be different.'
            error = True
            return None, None, None, None, None, None, None, None, None, alert_value, not error, ''

        years1 = list(range(years_comparison[0], years_comparison[1] + 1))
        years2 = list(range(years_base[0], years_base[1] + 1))
    else:
        years1 = list(range(year_options_min, year1 + 1))
        years2 = list(range(year_options_min, year2 + 1))


    cols = [location,
            'age_range' if 'ages' not in show_all else 'age_range_all',
            'race' if 'races' not in show_all else 'race_all',
            'sex' if 'genders' not in show_all else 'sex_all',
            'ethnicity' if 'etnicitys' not in show_all else 'ethnicity_all']

    cols_out = ['location', 'age_range', 'race', 'sex', 'ethnicity', 'relative']
    column_names_inc = COLUMNS.copy()
    column_names_dec = COLUMNS.copy()

    target = f'{year1}{year2}'
    ylist_comparison = list(range(years_comparison[0], years_comparison[1] + 1))
    ylist_base = list(range(years_base[0], years_base[1] + 1))

    df = df_filtered.filter(cols + ylist_comparison + ylist_base)
    df = df.groupby(cols).sum().reset_index()

    if len(ylist_comparison) > 1:
        df_years = df[ylist_comparison]
        df[year1] = df_years.mean(axis=1)
        df['SD'] = df_years.mad(axis=1)

    if len(ylist_base) > 1:
        df_years = df[ylist_base]
        if metric == 'Relative':
            df[year2] = df_years.mean(axis=1)
        else:
            df[year2] = df_years.max(axis=1)
            df['MAX_year'] = df_years.idxmax(axis=1)
        del df_years

    if metric == 'Relative':
        column_names_inc[-1] = column_names_inc[-1].copy()
        column_names_dec[-1] = column_names_dec[-1].copy()
        column_names_inc[-1]['name'] = 'Relative % increase'
        column_names_dec[-1]['name'] = 'Relative % decrease'

        if len(df) > 0:
            df[target] = pd.DataFrame((df[year2] - df[year1]) / df[year1] * 100).fillna(0).replace(np.inf, 100)
        else:
            df = pd.DataFrame(data=[['All', None, None, None, None]], columns=cols)
            df[target] = 0


    elif metric.startswith('CUSUM'):
        column_names_inc[-1]['name'] = 'CUSUM'

        if len(df) > 0:
            x = df[years1 + years2].values
            t = np.apply_along_axis(cusum, 1, x, threshold_std=int(metric[-1]))
            df[target] = t[:, -1]
        else:
            df = pd.DataFrame(data=[['All', None, None, None, None]], columns=cols)
            df[target] = 0
    elif metric == 'HLM':
        column_names_inc[-1] = column_names_inc[-1].copy()
        column_names_dec[-1] = column_names_dec[-1].copy()
        column_names_inc[-1]['name'] = 'k * SD above mean'
        column_names_dec[-1]['name'] = 'k * SD below mean'

        # Adjusting SD here to max(SD, 1.0) to avoid division by very small numbers (or zero).
        df[target] = (df[year2] - df[year1]) / df['SD'].clip(lower=1.0)


    res_inc = df.sort_values([target], ascending=False).head(limit)
    res_dec = df.sort_values([target], ascending=True).head(limit)


    if not metric.startswith('CUSUM'):

        if res_inc.shape[0] > 1:

            res_inc_t = list(format_tooltips(metric, res_inc, year1, year2))
            res_inc = res_inc[cols + [target]]
            res_inc[target] = res_inc[target].map('{:,.2f}'.format)

            res_inc.columns = cols_out

            res_dec_t = list(format_tooltips(metric, res_dec, year1, year2))
            res_dec[target] = res_dec[target] * (-1)
            res_dec = res_dec[cols + [target]]
            res_dec[target] = res_dec[target].map('{:,.2f}'.format)

            res_dec.columns = cols_out
        else:
            res_inc_t = None
            res_dec_t = None

        style = {'display': 'block'}
    else:

        res_inc = res_inc[cols + [target]]
        res_inc[target] = res_inc[target].map('{:,.2f}'.format)
        res_inc.columns = cols_out

        res_inc_t = None
        res_dec_t = None

        style = {'display': 'none'}


    cause = '' if cause is None or len(cause) == 0 else cause
    intent = '' if intent is None or len(intent) == 0 else intent
    by = 'by' if len(cause) > 0 or len(intent) > 0 else ''

    inc_lbl = f'Top {limit} increases {by} {cause} {intent} for {year2} with comparison year {year1}'
    dec_lbl = f'Top {limit} decreases {by} {cause} {intent} for {year2} with comparison year {year1}'


    return column_names_inc, res_inc.to_dict('records'), res_inc_t, column_names_dec, \
        res_dec.to_dict('records'), res_dec_t, inc_lbl, dec_lbl, style, alert_value, error, ''


@app.callback(
    dash.dependencies.Output('table_inc', 'columns'),
    dash.dependencies.Output('table_inc', 'data'),
    dash.dependencies.Output('table_inc', 'tooltip_data'),
    dash.dependencies.Output('table_dec', 'columns'),
    dash.dependencies.Output('table_dec', 'data'),
    dash.dependencies.Output('table_dec', 'tooltip_data'),
    dash.dependencies.Output('table_inc_label', 'children'),
    dash.dependencies.Output('table_dec_label', 'children'),
    dash.dependencies.Output('datatable-container', 'style'),
    dash.dependencies.Output('error', 'children'),
    dash.dependencies.Output('alert', 'hidden'),
    dash.dependencies.Output("loading-output-1", "children"),
    [dash.dependencies.Input('tab_scale', 'value'),
     dash.dependencies.Input('analytics_option', 'value'),
     dash.dependencies.Input('year', 'value'),
     dash.dependencies.Input('years_base', 'value'),
     dash.dependencies.Input('years_comparison', 'value'),
     dash.dependencies.Input('Cause', 'value'),
     dash.dependencies.Input('Intent', 'value'),
     dash.dependencies.Input('State', 'value'),
     dash.dependencies.Input('Region', 'value'),
     dash.dependencies.Input('ShowAll', 'value'),
     dash.dependencies.Input('limit', 'value'),
     dash.dependencies.Input('metric', 'value')]
)
def update_table(tab_scale, analytics_option, year, years_base, years_comparison,
                 cause, intent, state,region, show_all, limit, metric):
    """
        Input callback handler
    """
    return populate_table_data(tab_scale, analytics_option, year,
                               years_base, years_comparison, cause, intent, state, region,show_all, limit, metric)


@app.callback(
     dash.dependencies.Output('tv_summary', 'children'),
     [dash.dependencies.Input('analytics_option', 'value'),
      dash.dependencies.Input('metric', 'value'),
      dash.dependencies.Input('year', 'value'),
      dash.dependencies.Input('years_base', 'value'),
      dash.dependencies.Input('years_comparison', 'value')]
)
def update_summary(analytics_option, comparison_method, *args):
    inputs = dash.callback_context.inputs
    chunks = []
    for option in COMPARISON_METHOD_OPTIONS:
        if comparison_method == option['value']:
            comparison_method_label = option['label']
            break
    else:
        comparison_method_label = comparison_method
    if analytics_option == 'year_range':
        year_b0, year_b1 = inputs['years_base.value']
        year_c0, year_c1 = inputs['years_comparison.value']
    else:
        year_b0 = year_b1 = inputs['year.value']
        year_c0 = year_c1 = year_b0 - 1
    if year_c0 == year_c1:
        if comparison_method in ('HLM', 'CUSUM1'):
            return F"{comparison_method_label} requires a range of comparison years."
        chunks.append(F"Comparing deaths from {year_c0}")
    else:
        chunks.append(F"Comparing average deaths from {year_c0}-{year_c1}")
    if year_b0 == year_b1:
        chunks.append(F" with {year_b0}")
    else:
        chunks.append(F" with {year_b0}-{year_b1}")
    chunks.append(F" using {comparison_method_label}")
    chunks.append('.')
    return ''.join(chunks)
