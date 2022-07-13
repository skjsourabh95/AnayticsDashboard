from datetime import datetime

import numpy as np


def no_filter(df_mortality):
    return np.full(df_mortality.shape[0], True, dtype=bool)


def filter_age(df_mortality, filters, a=0, b=999):
    return filters & (df_mortality["age"] > a) & (df_mortality["age"] < b)


def filter_sex(df_mortality, filters, sex):
    if sex is None:
        return filters
    filters2 = None
    for s in sex:
        if filters2 is None:
            filters2 = (df_mortality["sex"] == s.lower())
        else:
            filters2 |= (df_mortality["sex"] == s.lower())
    if filters2 is None:
        return filters
    return filters & filters2


def filter_race(df_mortality, filters, race):
    if race is None:
        return filters
    filters2 = None
    for r in race:
        if filters2 is None:
            filters2 = (df_mortality["race"] == r.lower())
        else:
            filters2 |= (df_mortality["race"] == r.lower())
    if filters2 is None:
        return filters
    return filters & filters2


def filter_ethnicity(df_mortality, filters, ethnicity):
    if ethnicity is None:
        return filters
    filters2 = None
    for e in ethnicity:
        if filters2 is None:
            filters2 = (df_mortality["ethnicity"] == e.lower())
        else:
            filters2 |= (df_mortality["ethnicity"] == e.lower())
    if filters2 is None:
        return filters
    return filters & filters2


def filter_cause(df_mortality, filters, cause):
    if cause is None:
        return filters
    filters2 = None
    for c in cause:
        if filters2 is None:
            filters2 = (df_mortality["cause"] == c.lower())
        else:
            filters2 |= (df_mortality["cause"] == c.lower())
    if filters2 is None:
        return filters
    return filters & filters2


def filter_intent(df_mortality, filters, intent):
    if intent is None:
        return filters
    filters2 = None
    for i in intent:
        if filters2 is None:
            filters2 = (df_mortality["intent"] == i.lower())
        else:
            filters2 |= (df_mortality["intent"] == i.lower())
    if filters2 is None:
        return filters
    return filters & filters2


def filter_state(df_mortality, filters, state):
    if state is None:
        return filters
    filters2 = None
    for s in state:
        if filters2 is None:
            filters2 = (df_mortality["state"] == s)
        else:
            filters2 |= (df_mortality["state"] == s)
    if filters2 is None:
        return filters
    return filters & filters2


def filter_county(df_mortality, filters, county):
    if county is None:
        return filters
    filters2 = None
    for c in county:
        if filters2 is None:
            filters2 = (df_mortality["county_fips"] == c)
        else:
            filters2 |= (df_mortality["county_fips"] == c)
    if filters2 is None:
        return filters
    return filters & filters2

def filter_region(df_mortality, filters, region):
    if region is None:
        return filters
    filters2 = None
    for s in region:
        if filters2 is None:
            filters2 = (df_mortality["region"] == s)
        else:
            filters2 |= (df_mortality["region"] == s)
    if filters2 is None:
        return filters
    return filters & filters2

def filter_year(df_mortality, filters, a=2000, b=2020):
    start = datetime(a, 1, 1, 0, 0, 0)
    end = datetime(b, 1, 1, 0, 0, 0)
    return filters & (df_mortality["year"] >= start) & (df_mortality["year"] <= end)


def filter_age_range(df_mortality, filters, age_range):
    if age_range is None:
        return filters
    filters2 = None
    for c in age_range:
        if filters2 is None:
            filters2 = (df_mortality["age"] == c)
        else:
            filters2 |= (df_mortality["age"] == c)
    if filters2 is None:
        return filters
    return filters & filters2


def apply_filter(df, column, values, make_lower=True):
    if values is None:
        return df
    elif type(values) is not list:
        values = [values]
    if len(values) == 0:
        return df
    if make_lower:
        values = [v.lower() for v in values]

    return df[df[column].isin(values)]
