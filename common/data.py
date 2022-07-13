import os

import pandas as pd
import common.mapping as mapping
from datetime import datetime
import json
import ntpath

print("loading dataset...")

df_state_grouped = None
df_county_grouped = None
df_region_grouped = None
UPLOAD_DIRECTORY = "./data/app_uploaded_files"

def get_grouped_data():
    """
        Prepares and returns grouped datasets
    """
    global df_state_grouped, df_county_grouped, df_region_grouped

    if df_state_grouped is None:
        df_county_grouped = df_mortality.pivot_table(
            index=['state', 'county', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent'],
            columns=['year_i'],
            values='deaths',
            aggfunc='sum').fillna(0).reset_index()
        
        df_region_grouped = df_mortality.pivot_table(
            index=['state', 'region', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent'],
            columns=['year_i'],
            values='deaths',
            aggfunc='sum').fillna(0).reset_index()

        df_county_grouped = pd.merge(df_county_grouped, mapping.df_county, left_on=['state', 'county'],
                                     right_on=['State', 'County'], how='inner')
        
        df_region_grouped = pd.merge(df_region_grouped, mapping.df_region, left_on=['state', 'region'],
                                     right_on=['state', 'region'], how='inner')

        df_county_grouped['County_Name_Full'] = df_county_grouped['County_Name'] + ',' + df_county_grouped['State_name']

        df_region_grouped['Region_Name_Full'] = df_region_grouped['state_name'] + ',' + df_region_grouped['region_name']

        cols = ['state', 'State_name', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent']
        years = df_mortality['year_i'].unique()
        df_state_grouped = df_county_grouped.groupby(cols)[years].sum().reset_index()

    return df_state_grouped, df_county_grouped, df_region_grouped

with open('config.json') as fp:
    config = json.load(fp)
try:
    if config['df_mortality_path'] and os.path.isfile(config['df_mortality_path']):
        file_path = config['df_mortality_path']
    else:
        print("Loading Default data")
        file_path = "./data/MortalityData_2001_2018_Final_v2.csv"
except OSError as e:
        print("Incorrect File Path - Loading Default data")
        file_path = "./data/MortalityData_2001_2018_Final_v2.csv"

filename = ntpath.basename(file_path).split(".")[0]
print(ntpath.basename(file_path))

if config['update_feather_file']:
    print("Reading the new File")
    df_mortality = pd.read_csv(file_path, dtype={"state": str, "county": str})
    df_mortality["year"] = df_mortality["year"].apply(lambda x: datetime(x, 1, 1, 0, 0, 0))
    df_mortality["sex"] = df_mortality["sex"].apply(lambda x: mapping.sex[x])
    df_mortality["race"] = df_mortality["race"].apply(lambda x: mapping.race[x])
    df_mortality["ethnicity"] = df_mortality["ethnicity"].apply(lambda x: mapping.ethnicity[x])
    df_mortality["cause"] = df_mortality["cause"].apply(lambda x: mapping.causes[x])
    df_mortality["intent"] = df_mortality["intent"].apply(lambda x: mapping.intent[x])

    df_mortality["county_fips"] = df_mortality["state"] + df_mortality["county"]
    df_mortality["state_name"] = df_mortality["state"].apply(lambda x: mapping.state[x])
    df_mortality["county_name"] = df_mortality["county_fips"].apply(lambda x: mapping.county[x])
    df_mortality["region"] =  df_mortality["state"].apply(lambda x: mapping.region_states[x])
    df_mortality["age"] = df_mortality["age"].apply(lambda x: int((x if x < 90 else 89) / 10))
    df_mortality["age_range"] = df_mortality["age"].apply(lambda x: mapping.age_ranges[x])
    df_mortality['year_i'] = df_mortality['year'].dt.year


    # initialize datasets
    get_grouped_data()

    df_mortality.to_feather("./data/feather_files/%s.feather"%filename)
    df_state_grouped.columns = df_state_grouped.columns.astype(str)
    df_state_grouped['age_range_all'] = 'All'
    df_state_grouped['race_all'] = 'All'
    df_state_grouped['sex_all'] = 'All'
    df_state_grouped['ethnicity_all'] = 'All'
    df_state_grouped.to_feather("./data/feather_files/%s_SG.feather"%filename)
    df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
    
    df_county_grouped.columns = df_county_grouped.columns.astype(str)
    df_county_grouped['age_range_all'] = 'All'
    df_county_grouped['race_all'] = 'All'
    df_county_grouped['sex_all'] = 'All'
    df_county_grouped['ethnicity_all'] = 'All'
    df_county_grouped.to_feather("./data/feather_files/%s_CG.feather"%filename)
    df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]
    
    df_region_grouped.columns = df_region_grouped.columns.astype(str)
    df_region_grouped['age_range_all'] = 'All'
    df_region_grouped['race_all'] = 'All'
    df_region_grouped['sex_all'] = 'All'
    df_region_grouped['ethnicity_all'] = 'All'
    df_region_grouped.to_feather("./data/feather_files/%s_RG.feather"%filename)
    df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]

    config['update_feather_file']=False
    with open('config.json','w') as fp:
        json.dump(config,fp,indent=4)

else:

    df_mortality = pd.read_feather("./data/feather_files/%s.feather"%filename)
    df_state_grouped = pd.read_feather("./data/feather_files/%s_SG.feather"%filename)
    df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
    df_county_grouped = pd.read_feather("./data/feather_files/%s_CG.feather"%filename)
    df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]
    df_region_grouped = pd.read_feather("./data/feather_files/%s_RG.feather"%filename)
    df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]

year_series = df_mortality["year"].drop_duplicates().sort_values()
year_options = []
for key, value in year_series.iteritems():
    year_options.append({"label": value.year, "value": value.year})
year_options_max = max(year_series).year
year_options_min = min(year_series).year

def reset_data_file(data_options,name):
    with open('config.json') as fp:
            config = json.load(fp)
    
    default_file = "./data/MortalityData_2001_2018_Final_v2.csv"
    if data_options == "default" or  not name:
        # use default file in next run
        config['df_mortality_path']=''
        config['current_file_used']='MortalityData_2001_2018_Final_v2.csv(Default)'
        config['update_feather_file']=False
        with open('config.json','w') as fp:
            json.dump(config,fp,indent=4)
    else:
        if data_options == "append":
            # append new file in file being used
            
            df_new = pd.read_csv(os.path.join(UPLOAD_DIRECTORY, name),dtype={"state": str, "county": str})
            if config['df_mortality_path']:
                # use the current MortalityData.csv file to append
                df_old = pd.read_csv("./data/MortalityData.csv",dtype={"state": str, "county": str})
            else:
                # use default file to append
                df_old = pd.read_csv(default_file,dtype={"state": str, "county": str})
            
            df_merge =  pd.concat([df_old, df_new], ignore_index=True, sort=False)
            df_merge.to_csv('./data/MortalityData.csv',index=False)
            config['df_mortality_path']='.//data//MortalityData.csv'
            config['current_file_used']="MortalityData.csv"
            config['update_feather_file']=True
            with open('config.json','w') as fp:
                json.dump(config,fp,indent=4)

        else:
            # overwrite file being used with new file
            df_new = pd.read_csv(os.path.join(UPLOAD_DIRECTORY, name),dtype={"state": str, "county": str})
            df_new.to_csv('./data/MortalityData.csv',index=False)
            config['df_mortality_path']='.//data//MortalityData.csv'
            config['current_file_used']="MortalityData.csv"
            config['update_feather_file']=True
            with open('config.json','w') as fp:
                json.dump(config,fp,indent=4)

def file_sanity_check(file):
    with open('./data/mapping_files/dtypes.json', 'r') as fp:
        dtypes = json.load(fp)
    # check if file exists
    if file and os.path.isfile(os.path.join(UPLOAD_DIRECTORY,file)):
        df = pd.read_csv(os.path.join(UPLOAD_DIRECTORY, file))
        # check if there are empty values
        if not df.isnull().any().any():
            # check if columns match
            if set(list(df.columns)) == set(list(dtypes.keys())):
                for t in df.dtypes.to_dict():
                    # check if dtypes of columns match
                    if not str(df.dtypes[t]) == dtypes[t]:
                        os.remove(os.path.join(UPLOAD_DIRECTORY,file))
                        return "File has a incorrect dtype for a columns,% should be %"%(t,dtypes[t])
                return True

            else:
                os.remove(os.path.join(UPLOAD_DIRECTORY,file))
                return "File contains mismatched columns!"
        else:
            os.remove(os.path.join(UPLOAD_DIRECTORY,file))
            return "File contains NaN or empty values!"
    else:
        return "No File Present!"

print("DONE!")