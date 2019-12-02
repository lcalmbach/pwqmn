import streamlit as st
import pandas as pd

dfTexts = pd.DataFrame
text_file = r"fontus_texts.txt"

def init():
    global dfTexts
    dfTexts = pd.read_csv(text_file,sep='\t', encoding = "ISO-8859-1")
    dfTexts.set_index("key")

def print_info(dfStations, dfParameters, dfSamples):
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR001', 'text'].values[0])
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR002', 'text'].values[0])
    
    st.markdown('Summary of data available in the dataset:')
    st.markdown('* Number of stations: {0}'.format(len(dfStations.index)))
    st.markdown('* Number of parameters: {0}'.format(len(dfParameters.index)))
    st.markdown('* Number of sampling events: {0}'.format(len(dfSamples.index)))