import streamlit as st
import pandas as pd
import numpy as np

dfSamples = pd.DataFrame
dfStations = pd.DataFrame
dfParameters = pd.DataFrame

def init():
    global dfSamples
    global dfStations
    global dfParameters

    dfSamples = read_samples()
    dfStations = read_stations()
    dfParameters = read_parameters()

@st.cache
def read_samples():
    df = pd.read_csv(r"data/pwqmn_chemistry_data.txt", sep='\t',encoding = "ISO-8859-1", float_precision='high')
    df['SAMPLE_DATE'] = pd.to_datetime(df['SAMPLE_DATE'])
    df['MONTH'] = df['SAMPLE_DATE'].dt.month
    df['YEAR'] = df['SAMPLE_DATE'].dt.year
    return df

@st.cache
def read_stations():
    result = pd.read_csv(r"data/pwqmn_stations.txt", sep='\t', encoding = "ISO-8859-1", float_precision = 'round_trip')
    result.set_index("STATION_NAME", inplace = True)
    return result

@st.cache
def read_parameters():
    result = pd.read_csv(r"data/pwqmn_parameters.txt", sep='\t',encoding = "ISO-8859-1")
    return result

def get_rivers(df):
    result = df.RIVER_NAME.unique()
    result.sort()
    return result

def get_stations(df):
    result = df.STATION_NAME.unique()
    result = np.insert(result, 0, '<all stations>')
    result.sort()
    return result

