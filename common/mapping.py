import pandas as pd
import json

# RACE
race = dict()
race.update({1:"white"})
race.update({2:"black"})
race.update({3:"indian/native"})
race.update({4:"asian"})

# create dropdown options for RACE
race_options = []
for key, value in race.items():
    race_options.append({"label":value.title(), "value":value.title()})


# ETHNICITY
ethnicity = dict()
ethnicity.update({1:"non-hispanic"})
ethnicity.update({2:"hispanic"})
ethnicity.update({3:"unknown"})

# create dropdown options for ETHNICITY
ethnicity_options = []
for key, value in ethnicity.items():
    ethnicity_options.append({"label":value.title(), "value":value.title()})


# SEX
sex = dict()
sex.update({1:"male"})
sex.update({2:"female"})

# create dropdown options for SEX
sex_options = []
for key, value in sex.items():
    sex_options.append({"label":value.title(), "value":value.title()})


# AGE
age = dict()


# INTENT
intent = dict()
intent.update({0:"adverse effects"})
intent.update({1:"unintentional"})
intent.update({2:"suicide"})
intent.update({3:"homicide"})
intent.update({5:"undetermined intent"})
intent.update({6:"legal intervention"})
intent.update({7:"other specified"})

# create dropdown options for INTENT
intent_options = []
for key, value in intent.items():
    intent_options.append({"label":value.title(), "value":value.title()})


# CAUSES
df_causes = pd.read_csv("./data/mapping_files/Codebook_Cause_Labels.csv")
df_causes["cause"] = df_causes["cause"].astype("int")
df_causes["Causelbl"] = df_causes["Causelbl"].astype("str")
df_causes = df_causes.set_index("cause")
causes = dict()
for index, row in df_causes.iterrows():
    causes.update({index:row["Causelbl"].lower()})

# create dropdown options for CAUSES
causes_options = []
for key, value in causes.items():
    causes_options.append({"label":value.title(), "value":value.title()})

# COUNTY
df_county = pd.read_csv("./data/mapping_files/StateCounty_Labels.csv",dtype={"State": str,
                                                          "County":str})
df_county["county_fips"] = df_county["State"] + df_county["County"]
df_county = df_county.set_index("county_fips")
county = dict()
for index, row in df_county.iterrows():
    county.update({index:row["County_Name"]})

# create dropdown options for COUNTY
county_options = []
for key,value in county.items():
    county_options.append({"label":value, "value":key})


# STATE
df_state = df_county[["State","State_name"]].drop_duplicates()
df_state = df_state.set_index("State")
state = dict()
for index, row in df_state.iterrows():
    state.update({index:row["State_name"]})

# create dropdown options for STATE
state_options = []
for key,value in state.items():
    state_options.append({"label":value, "value":key})


# REGIONAL
df_region = pd.read_csv("./data/mapping_files/states_region_mapping.csv",dtype={"state": str,
                                                          "region":str})
region_mapping = df_region[["region","region_name"]]
region_mapping = region_mapping.set_index("region")

region_state_mapping = df_region[["state","region"]]
region_state_mapping = region_state_mapping.set_index("state")
region_states = dict()
for index, row in region_state_mapping.iterrows():
    region_states.update({index:row["region"]})

regions = dict()
for index, row in region_mapping.iterrows():
    regions.update({index:row["region_name"]})

# create dropdown options for REGIONAL
region_options = []
for key,value in regions.items():
    region_options.append({"label":"Region- %s"%value, "value":str(key)})


# create dropdown options for MAP SCALE
map_scale_options = [{'value': 'state', 'label': 'States'},
                     {'value': 'county_fips', 'label': 'Counties'},
                     {'value': 'region', 'label': 'Regional'}]

# create dropdown options for DATA LOADING
data_loading_options = [{'value': 'default', 'label': 'Default'},
                    {'value': 'append', 'label': 'Append'},
                     {'value': 'overwrite', 'label': 'Overwrite'}]


# create dropdown options for YEAR COMPARISON
analytics_options = [{'value': 'last_year', 'label' : 'Compare with year before selected'},
                     {'value': 'year_range', 'label': 'Compare range of years'},
                     {'value': 'combined_report', 'label' : 'Combined report: show intent with max death percentual      compared with year before'}]

# age ranges
age_ranges = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
age_ranges_options = [{'value': i, 'label': f'{a}'} for i, a in enumerate(age_ranges)]
