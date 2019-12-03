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

    st.markdown('![title pic](https://github.com/lcalmbach/pwqmn/raw/master/static/images/river_background.png)')
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR001', 'text'].values[0])
    st.markdown(dfTexts.loc[dfTexts.key == 'PAR002', 'text'].values[0])
    
    st.markdown('### Summary of data available in the dataset:')
    st.markdown('* Number of stations: {0}'.format(len(dfStations.index)))
    st.markdown('* Number of parameters: {0}'.format(len(dfParameters.index)))
    st.markdown('* Number of sampling events: {0}'.format(db.number_of_samples))
    st.markdown('* Data last modified: {0}'.format(cn.data_last_modified)) 

    st.markdown('### Metadata from data owner:')
    st.markdown('* Publisher: Environment, Conservation and Parks')
    st.markdown('* Ontario Time captured: January 1, 1964 – December 31, 2016')
    st.markdown('* Update frequency: Yearly')
    st.markdown('* Geographical coverage: Ontario')
    st.markdown('* Technical documentation: [Metadata Record](https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/metadata.show?id=13826)')  


def print_help():
    st.markdown(help_content,unsafe_allow_html=True)
