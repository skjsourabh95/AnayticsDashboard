import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import base64
import datetime
import io,os
from flask import Flask, send_from_directory
from common.header import header_layout
from app import app
from common.mapping import data_loading_options
import warnings
from pandas.core.common import SettingWithCopyWarning
from common.data import reset_data_file,file_sanity_check
import json
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)



UPLOAD_DIRECTORY = "./data/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


layout = html.Div([
    header_layout,
    html.Br(),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Upload Files', children=[
                html.Div([  
                html.H2("Upload"),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    ]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=True,
                ), 
                ],
                style={"max-width": "500px",
                    "textAlign": "center",
                    "justify-content": "center",
                    "align-items": "center"}
                ),
                html.Div([
                    dcc.Loading(
                            id="loading",
                            type="dot",
                            children=html.Div(id="loading-output")
                    ),
                ]),
                html.Div([
                    html.Div([
                        html.H6("Select One For Next Run"),
                        dcc.RadioItems(
                            id='data_options',
                            options=data_loading_options,
                            labelStyle={'display': 'inline-block'}
                        ), 
                    ],style={"textAlign": "center",
                            "justify-content": "center",
                            "align-items": "center"},),
                    html.Hr(),
                    html.Div(id='current_file'),
                    html.H6("Select Data File For Next Run"),
                    dcc.Dropdown(id='file-list',placeholder="Select",), 
                    html.Hr(),
                    html.Div([
                        dcc.ConfirmDialogProvider(
                            children=html.Button(
                                'Submit',
                            ),
                            id='submit-provider',
                            message='Are you sure you want to continue?'
                        ),
                        html.Br(),
                        html.Div([
                            dcc.Loading(
                                    id="loading-1",
                                    type="default",
                                    children=html.Div(id="loading-confirm")
                            ),
                        ]),
                        html.Div(id='output-provider'),
                        
                     ],style={"textAlign": "center",
                            "justify-content": "center",
                            "align-items": "center"},
                    ),
                ],
                style={"max-width": "500px"})
            ]),
            dcc.Tab(label='Preview', children=[
                html.Div([  
                    html.H2("Files Uploaded"),  
                    html.Div(id='output-data-upload'), 
                ],
                style={
                    "textAlign": "center",
                    "justify-content": "center",
                    "align-items": "center"}
                ),
            ])
        ])
    ],
    
    ),  
])

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in name:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in name:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div([
            'Incorrect File Format.'
        ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.H5(name),
        dash_table.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line
    ])

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


@app.callback(
    [dash.dependencies.Output("output-data-upload", "children"),
    dash.dependencies.Output("file-list", "options"),
    dash.dependencies.Output("current_file", "children"),
    dash.dependencies.Output("loading-output", "children"),],
    [dash.dependencies.Input("upload-data", "filename"), 
    dash.dependencies.Input("upload-data", "contents")],
)
def save_preview_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        children = [save_file(name, data) for name, data in zip(uploaded_filenames, uploaded_file_contents)]
    else:
        children =[]

    upload_files = uploaded_files()
    files = [{"value":name,"label":name} for name in upload_files]
    with open('config.json') as fp:
        config = json.load(fp)
    current_file = html.Label("File Being Used - %s"%config['current_file_used'])
    return children,files,current_file,""



@app.callback(
    [dash.dependencies.Output('output-provider', 'children'),
    dash.dependencies.Output("loading-confirm", "children"),],
    [dash.dependencies.Input('submit-provider', 'submit_n_clicks'),
    dash.dependencies.Input("data_options", "value"),
    dash.dependencies.Input("file-list", "value")],
)
def update_output(submit_n_clicks, data_options,new_file):
    """Show uploaded files"""
    if submit_n_clicks:
        if data_options is not None and new_file is not None:
            sanity = file_sanity_check(new_file)
            if type(sanity) == bool and sanity:
                reset_data_file(data_options,new_file)
                return "Submitted!",""
            else:
                return "Removing File - %s"%sanity,""
        elif data_options is not None and data_options=='default':
            reset_data_file(data_options,None)
            return "Changed to default File!",""
        else:
            return "Please Choose a File!",""
    else:
        return "",""
