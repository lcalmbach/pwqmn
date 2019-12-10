"""This example is a Streamlit implementation of an interactive water quality data app.
This app allows to explore the Ontario Provincial Water Quality Network dataset encompssing 
over 53 years of data. The data can be explored using various Altair plots.
Author: Lukas Calmbach lcalmbach@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

import constants as cn
import fontus_texts as txt
import fontus_db as db
import plots as plt
import stations, parameters, samples

_controls = {}

def ctrl(key):
    return _controls[key]

def main():
    init()
    show_menu()
    st.sidebar.markdown('---')
    txt.info_sideboard('ABOUT')

def init():
    global _controls

    _controls = init_controls()
    db.init()
    stations.init(db.dfStations)
    txt.init()

# register all widgets
def init_controls():
    result = {
        'menu': ''
        , 'plot_type': ''
        , 'all_rivers': True
        , 'rivers': []
        , 'station': ''
        , 'xpar': ''
        , 'ypar': ''
        , 'group_by': 'station'
        , 'define_axis_limits': False
        , 'max_x': 0
        , 'max_y': 0
        , 'min_x': 0
        , 'min_y': 0
        , 'bin_size': 0
        , 'bar_direction': ''
        , 'filter_by_year': False       #check box if you want to select a year
        , 'filter_by_month': False      #check box if you want to select a month
        , 'filter_month': 0             #holds selected month
        , 'filter_year': 0              #holds selected year
        , 'plot_width' : cn.plot_width
        , 'plot_height' : cn.plot_height
        , 'show_data': False
    }
    return result

def station_menu():
    global _controls

    st.header(ctrl('menu'))
    stations.init(db.dfStations)
    #sidebar menu
    _controls['all_rivers'] = st.sidebar.checkbox('All stations', value=False, key=None)
    if not _controls['all_rivers']:
        _controls['rivers'] = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(stations.all_rivers_list).tolist()) 
    # content
    df = stations.get_table(ctrl('all_rivers'), ctrl('rivers'))
    df.reset_index(inplace = True) #needed so station_name can be selected on plotly table
    column_values = [df.STATION_NAME, df.RIVER_NAME, df.LOCATION, df.lon, df.lat, df.STATUS, df.FIRST_YR, df.LAST_YR, df.TOTAL_YRS, df.MISS_YRS]
    txt.show_table(df, column_values)
    if not ctrl('all_rivers'):
        text = "This list only includes stations from the selected surface water bodies."
    else:
        text = "This list includes all stations of the monitoring network."
    st.markdown(text)

def parameters_menu():
    global _controls

    st.header(_controls['menu'])
    parameters.init(db.dfParameters, db.dfSamples)
    #sidebar menu
    _controls['all_rivers'] = st.sidebar.checkbox('All stations', value=False, key=None)
    if not ctrl('all_rivers'):
        _controls['rivers'] = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(stations.all_rivers_list).tolist()) 
    # content
    df = parameters.get_table(ctrl('all_rivers'), ctrl('rivers'))
    df = df[['PARM', 'PARM_DESCRIPTION', 'DESCRIPTION']]
    values = [df.PARM, df.PARM_DESCRIPTION, df.DESCRIPTION]
    txt.show_table(df,values)
    if not ctrl('all_rivers'):
        text = "This parameter list only includes parameters having been measured in the selected rivers or lakes."
    else:
        text = "This parameter list includes all parameters having been measured in the monitoring network."
    st.markdown(text)

def plots_menu():
    global _controls

    _controls['plot_type'] = st.sidebar.selectbox('Plot type', cn.plot_type_list)
    if ctrl('plot_type') not in ['time series']:
        _controls['group_by'] = st.sidebar.selectbox('Group by', pd.Series(cn.group_by_list))
    _controls['rivers'] = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(stations.all_rivers_list).tolist())

    if len(ctrl('rivers')) > 0:
        parameters_list = parameters.get_sample_parameters(ctrl('rivers'))
    else:
        parameters_list = parameters.get_sample_parameters(db.dfStations)

    if ctrl('plot_type') not in ['time series', 'histogram', 'boxplot', 'bar chart']:
        _controls['xpar'] = parameters.get_parameter_key(st.sidebar.selectbox('X-parameter', parameters_list, index = 0))
    _controls['ypar'] = parameters.get_parameter_key(st.sidebar.selectbox('Y-parameter', parameters_list, index = 1))
    if ctrl('plot_type') not in ['time series']:
        _controls['filter_month'] = st.sidebar.checkbox('Filter data by month', value = False, key=None)
        if _controls['filter_month']:
            _controls['month'] = st.slider('Month', min_value = 0, max_value = 12, value=None)
        _controls['filter_year'] = st.sidebar.checkbox('Filter data by year', value=False, key=None)
        if _controls['filter_year']:
            _controls['year'] = st.slider('Year', min_value = int(db.first_year), max_value = int(db.last_year), value = int(db.first_year)) #db.first_year, max_value = db.last_year)
    if _controls['plot_type'] == 'histogram':
        _controls['bin_size'] = st.sidebar.number_input('Bin width')
    
    _controls['define_axis_limits'] = st.sidebar.checkbox('Define axis limits', value=False, key=None)
    if ctrl('define_axis_limits'):
        if ctrl('plot_type') not in ['time series']:
            _controls['min_x'] = st.sidebar.number_input('Minimum X')
            _controls['max_x'] = st.sidebar.number_input('Maximum X')
        _controls['min_y'] = st.sidebar.number_input('Minimum y')
        _controls['max_y'] = st.sidebar.number_input('Maximum y')
    if _controls['plot_type'] == 'bar chart':
        _controls['bar_direction'] = st.sidebar.radio('Bars', ['vertical', 'horizontal'])

    _controls['define_axis_length'] = st.sidebar.checkbox('Define axis length', value=False)
    if _controls['define_axis_length']:
        _controls['plot_width'] = st.sidebar.number_input('Width (pixel)', value = ctrl('plot_width'))
        _controls['plot_height'] = st.sidebar.number_input('Height (pixel)', value = ctrl('plot_height'))
    
    _controls['show_data'] = st.sidebar.checkbox('Show detail data', value = False, key = None)
    
    if _controls['plot_type'] != 'map':
        for riv in ctrl('rivers'):
            dfRiver = db.dfSamples[(db.dfSamples['RIVER_NAME'] == riv)]
            if ctrl('filter_month'):
                dfRiver = dfRiver[(dfRiver.MONTH == int(ctrl('month')))]
            if ctrl('filter_year'):
                dfRiver = dfRiver[(dfRiver.YEAR == int(ctrl('year')))]
            plot_title = riv
            show_all_stations = True
            
            if len(ctrl('rivers')) == 1:
                _controls['station'] = st.selectbox('station', pd.Series(db.get_stations(dfRiver)))
                show_all_stations = (ctrl('station') == '<all stations>')
                if not show_all_stations:
                    dfRiver = dfRiver[(dfRiver['STATION_NAME'] == ctrl('station'))]
                    plot_title += ': ' + _controls['station']
            plot_results_list = plt.plot(plot_title, dfRiver, _controls)
            # verify if the data has rows
            if (len(plot_results_list[1]) > 0):
                st.write(plot_results_list[0].properties(width = ctrl('plot_width'), height = ctrl('plot_height')))
                # if a station has been selected display a link to visit site on google maps
                if not show_all_stations and len(_controls['rivers']) == 1:
                    db.dfStations.set_index('STATION_NAME', inplace = True)
                    lat = db.dfStations.at[_controls['station'],'lat']
                    lon = db.dfStations.at[_controls['station'],'lon']
                    loc = db.dfStations.at[_controls['station'],'LOCATION']
                    lnk = 'Location: {0}. [Visit station on GOOGLE maps](https://www.google.com/maps/search/?api=1&query={1},{2} "open in GOOGLE maps")'.format(loc, lat, lon)
                    st.markdown(lnk)
                if ctrl('show_data'):
                    st.dataframe(plot_results_list[1])
            else:
                st.write('Insufficient data for: ' + plot_title)
    else:
        dfRiver = pd.DataFrame
        show_all_stations = True
        plot_title = 'Map'
        dfRiver = db.dfStations
        if len(ctrl('rivers')) == 1:
            df = db.dfStations[(db.dfStations['RIVER_NAME'] == ctrl('rivers')[0])]
            _controls['station'] = st.selectbox('Select a station or <all stations>', pd.Series(db.get_stations(df)))
            show_all_stations = (ctrl('station') == '<all stations>')
            if not show_all_stations:
                dfRiver = dfRiver[(dfRiver['STATION_NAME'] == ctrl('station'))]
                plot_title += ': ' + _controls['station']
            else:
                dfRiver = dfRiver[(dfRiver['RIVER_NAME'] == ctrl('rivers')[0])]
        elif len(ctrl('rivers')) > 1:
            dfRiver = db.dfStations[(db.dfStations['RIVER_NAME'].isin(ctrl('rivers')))]
            if not show_all_stations:
                dfRiver = dfRiver[(dfRiver['STATION_NAME'] == ctrl('station'))]
        
        if dfRiver.shape[0] > 0:
            plt.plot_map(dfRiver, ctrl)
            st.write('if map appears empty, use mouse wheel to zoom out, until markers appear.')
        else:
            st.write('Insufficient data')
        

def show_menu():
    global _controls

    st.sidebar.header('Menu')
    _controls['menu'] = st.sidebar.radio('', cn.menu_list, index = 5, key = None) # format_func=<class 'str'>, 
    st.sidebar.markdown('---')

    if _controls['menu'] == 'About':
        txt.print_main_about(db.dfStations, db.dfParameters, db.dfSamples)
    elif _controls['menu'] == 'Help':
        txt.print_help()
    elif _controls['menu'] == 'Station information':
        station_menu()
    elif _controls['menu'] == 'Parameters information':
        parameters_menu()
    elif _controls['menu'] == 'Plotting':
        plots_menu()

if __name__ == "__main__":
    main()