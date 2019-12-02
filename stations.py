import streamlit as st
import pandas as pd

dfStations = pd.DataFrame

def init(df):
    global dfStations

    dfStations = df

def get_table(all_rivers_sel, rivers_sel):
    global dfStations

    if all_rivers_sel:
        result = dfStations
    else:
        result = dfStations
        result = dfStations[(dfStations['RIVER_NAME'].isin(rivers_sel))]
        #result.sort(['RIVER_NAME', 'STATION_NAME'])
    return result