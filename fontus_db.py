"""
## Fontus

Fontus is a tool to 

Author: [Lukas Calmbach](mailto:lcalmbach@gmail.com))\n
Source: [Github](https://github.com/lcalmbach)
"""
import streamlit as st
import pandas as pd
import numpy as np
import constants as cn

dfSamples = pd.DataFrame
dfStations = pd.DataFrame
dfParameters = pd.DataFrame
number_of_samples = 0
number_of_stations = 0
number_of_parameters = 0
dfSamples_all = pd.DataFrame
first_year = 0
last_year = 0

def init():
    import app
    global dfSamples
    global dfStations
    global dfParameters
    global dfSamples_all
    global number_of_samples
    global number_of_stations
    global number_of_parameters
    global first_year
    global last_year
    global all_parameters_list
    global all_rivers_list

    dfSamples = read_samples()
    dfStations = read_stations()
    dfParameters = read_parameters()
    dfSamples_all = dfSamples.groupby(['RIVER_NAME','STATION_NAME','SAMPLE_DATE']).size()
    
    number_of_samples = get_number_of_samples(dfSamples)
    number_of_stations = len(dfStations.index)
    number_of_parameters = len(dfParameters.index)
    first_year = dfSamples['YEAR'].min()
    last_year = dfSamples['YEAR'].max()

@st.cache
def read_samples():
    df = pd.read_csv(cn.data_path + r"pwqmn_chemistry_data.txt",sep='\t',encoding = "ISO-8859-1")
    df['SAMPLE_DATE'] = pd.to_datetime(df['SAMPLE_DATE'])
    df['MONTH'] = df['SAMPLE_DATE'].dt.month
    df['YEAR'] = df['SAMPLE_DATE'].dt.year
    return df

@st.cache
def read_stations():
    result = pd.read_csv(cn.data_path + r"pwqmn_stations.txt", sep='\t', encoding = "ISO-8859-1",)
    return result

@st.cache
def read_parameters():
    result = pd.read_csv(cn.data_path + r"pwqmn_parameters.txt", sep='\t',encoding = "ISO-8859-1")
    result['LABEL'] = result["LABEL"].replace(to_replace = np.nan, value = result["PARM"])
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

def get_number_of_samples(df):
    df = df.groupby(['RIVER_NAME','STATION_NAME','SAMPLE_DATE']).size()
    return df.count()

