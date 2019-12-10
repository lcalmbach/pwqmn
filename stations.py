import streamlit as st
import pandas as pd
import fontus_db as db

dfStations = pd.DataFrame
all_rivers_list = []
    
def init(df):
    global dfStations
    global all_rivers_list
    
    dfStations = df
    all_rivers_list = db.get_rivers(df)

def get_table(all_rivers, rivers):
    global dfStations

    if all_rivers:
        result = dfStations
    else:
        result = dfStations
        result = dfStations[(dfStations['RIVER_NAME'].isin(rivers))]
        #result.sort(['RIVER_NAME', 'STATION_NAME'])
    return result