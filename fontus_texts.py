import streamlit as st
import pandas as pd
import constants as cn
import fontus_db as db

dfTexts = pd.DataFrame
help_content = ''
helpfile = 'help.md'
text_file = r"fontus_texts.txt"

def init():
    global dfTexts
    global help_content
    dfTexts = pd.read_csv(cn.text_path + text_file,sep='\t', encoding = "ISO-8859-1")
    dfTexts.set_index("key")
    with open(cn.text_path + helpfile) as f:
        help_content = f.read().replace('%version%', cn.version)
        help_content = help_content.replace('%samples%', str(db.number_of_samples))
        help_content = help_content.replace('%stations%', str(db.number_of_stations))
        help_content = help_content.replace('%parameters%', str(db.number_of_parameters))
        #help_content = [x.strip() for x in help_content]

def print_info(dfStations, dfParameters, dfSamples):
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR001', 'text'].values[0])
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR002', 'text'].values[0])
    
    st.markdown('Summary of data available in the dataset:')
    st.markdown('* Number of stations: {0}'.format(len(dfStations.index)))
    st.markdown('* Number of parameters: {0}'.format(len(dfParameters.index)))
    st.markdown('* Number of sampling events: {0}'.format(db.number_of_samples))

def print_help():
    st.markdown(help_content,unsafe_allow_html=True)
