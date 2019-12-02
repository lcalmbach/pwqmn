import streamlit as st
import pandas as pd
import fontus_db as db

def get_table(rivers_sel):
    result = db.dfSamples[(db.dfSamples['RIVER_NAME'].isin(rivers_sel))]
    return result