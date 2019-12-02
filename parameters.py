import streamlit as st
import pandas as pd
import fontus_db as db

dfParameters = pd.DataFrame
dfSamples = pd.DataFrame

def init(dfPar, dfSam):
    global dfParameters
    global dfSamples

    dfParameters = dfPar
    dfSamples = dfSam

def get_table(all_rivers_sel, rivers_sel):
    global dfParameters
    global dfSamples

    if all_rivers_sel:
        result = dfParameters
    else:
        result = dfParameters
        #result = dfParameters[(dfStations['RIVER_NAME'].isin(rivers_sel))]
        #result.sort(['RIVER_NAME', 'STATION_NAME'])
    return result

def get_parameters(df):
    result = df.PARM_DESCRIPTION.unique()
    result.sort()
    return result

def get_sample_parameters(rivers_sel):
    # filter samples to include only samples listed in the rivers-selection
    result = db.dfSamples[(db.dfSamples['RIVER_NAME'].isin(rivers_sel))]
    # make unqique list of parameters from the filtered table
    lst_par = result.PARM.unique()
    # filter the parameter table to include only parameters from the filtered sample list
    result = db.dfParameters[(db.dfParameters['PARM'].isin(lst_par))]
    result = result.PARM_DESCRIPTION
    return result.tolist()

# returns the key for a given parameter description. the lists hold parameter descriptions, so they are easier to understand
# in the graphs, we need to reference the keys. e.g. Description: CALCIUM and key: CAUT.
def get_parameter_key(value):
    df = db.dfParameters[(db.dfParameters['PARM_DESCRIPTION'] == value)]
    df = df.set_index("PARM_DESCRIPTION", drop = False)
    return  df.at[value,'PARM']