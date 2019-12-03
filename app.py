import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

import constants as cn
import fontus_texts as info
import fontus_db as db
import plots as plt
import stations, parameters, samples

rivers = list()
dfSamples = pd.DataFrame
dfStations = pd.DataFrame
year = 0
info.init()

plot_type_list = ['scatter plot','time series','histogram','boxplot'] #, 'schoeller', 'map',
group_by_list = ['station','year','month']
months_list = ['<all>','1','2','3','4','5','6','7','8','9','10','11','12']
menu_list = ['Plotting', 'Station information', 'Parameters information', 'Help', 'About']
year_min = 1994 # todo! make dynamic
year_max = 2016 # todo! make dynamic
month_sel = 0
year_sel = 0
xpar_sel = ''
max_x_sel = -99
max_y_sel = -99
min_x_sel = -99
min_y_sel = -99
stations_sel = ''
plot_width = 600
plot_height = 400
filter_by_year_sel = False      #check box if you want to select a year
filter_by_month_sel = False     #check box if you want to select a month
filter_month_sel = False        #holds selected month
filter_year_sel = False         #holds selected year
group_by_sel = ''

# start
#prepare data
db.init()
dfSamples = db.dfSamples
dfStations = db.dfStations
dfParameters = db.dfParameters
rivers_list = db.get_rivers(dfStations)
stations_list = db.get_stations
parameters_list = parameters.get_parameters(dfParameters)

#sidebar
st.sidebar.header('Menu')
menu_sel = st.sidebar.radio('', menu_list, index=4, key=None) # format_func=<class 'str'>, 
st.sidebar.markdown('---')

if menu_sel == 'About':
    st.header('Ontario Provincial (Stream) Water Quality Monitoring Network Data 1964 - 2014')
    info.print_info(dfStations, dfParameters, dfSamples)
elif menu_sel == 'Help':
    info.print_help()
elif menu_sel == 'Station information':
    st.header(menu_sel)
    stations.init(dfStations)
    #sidebar menu
    all_rivers_sel = st.sidebar.checkbox('All stations', value=False, key=None)
    if not all_rivers_sel:
        rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist()) 
    # content
    df = stations.get_table(all_rivers_sel, rivers_sel)
    st.write(df)
elif menu_sel == 'Parameters information':
    st.header(menu_sel)
    parameters.init(dfParameters, dfSamples)
    #sidebar menu
    all_rivers_sel = st.sidebar.checkbox('All stations', value=False, key=None)
    if not all_rivers_sel:
        rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist()) 
    # content
    df = parameters.get_table(all_rivers_sel, rivers_sel)
    st.write(df)
elif menu_sel == 'Plotting':
    st.header(menu_sel)
    plot_type_sel = st.sidebar.selectbox('Plot type', plot_type_list)
    if plot_type_sel not in ['time series']:
        group_by_sel = st.sidebar.selectbox('Group by', pd.Series(group_by_list))
    rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist())

    parameters_list = parameters.get_sample_parameters(rivers_sel)
    if plot_type_sel not in ['time series', 'histogram', 'boxplot']:
        xpar_sel = parameters.get_parameter_key(st.sidebar.selectbox('X-parameter', parameters_list, index = 0))
    ypar_sel = parameters.get_parameter_key(st.sidebar.selectbox('Y-parameter', parameters_list, index = 1))
    if plot_type_sel not in ['time series']:
        filter_month_sel = st.sidebar.checkbox('Filter data by month', value=False, key=None)
        if filter_month_sel:
            month_sel = st.slider('Month', min_value = 0, max_value = 12, value=None)
        filter_year_sel = st.sidebar.checkbox('Filter data by year', value=False, key=None)
        if filter_year_sel:
            year_sel = st.slider('Year', min_value = year_min, max_value = year_max, value=None)

    define_axis_limits = st.sidebar.checkbox('Define axis limits', value=False, key=None)
    if define_axis_limits:
        if plot_type_sel not in ['time series']:
            min_x_sel = st.sidebar.number_input('Minimum X')
            max_x_sel = st.sidebar.number_input('Maximum X')
        min_y_sel = st.sidebar.number_input('Minimum y')
        max_y_sel = st.sidebar.number_input('Maximum y')

    show_data_sel = st.sidebar.checkbox('Show detail data', value = False, key = None)
    plt.init(plot_type_sel, xpar_sel, ypar_sel, group_by_sel, max_x_sel, max_y_sel, min_x_sel, min_y_sel)
    if plot_type_sel != 'map':
        for riv in rivers_sel:
            dfRiver = dfSamples[(dfSamples['RIVER_NAME'] == riv)]
            if filter_month_sel:
                dfRiver = dfRiver[(dfRiver.MONTH == int(month_sel))]
            if filter_year_sel:
                dfRiver = dfRiver[(dfRiver.YEAR == int(year_sel))]

            if plot_type_sel != 'map':
                plot_title = riv
                show_all_stations = True
                if len(rivers_sel) == 1:
                    stations_sel = st.selectbox('Stations', pd.Series(db.get_stations(dfRiver)))
                    show_all_stations = (stations_sel == '<all stations>')
                    if not show_all_stations:
                        dfRiver = dfRiver[(dfRiver['STATION_NAME'] == stations_sel)]
                        plot_title += ': ' + stations_sel
                plot_results_list = plt.plot(plot_title, dfRiver)
                st.write(plot_results_list[0].properties(width = plot_width, height = plot_height))
                # if a station has been selected display a link to visit site on google maps
                if not show_all_stations and len(rivers_sel) == 1:
                    lat = dfStations.at[stations_sel,'lat']
                    lon = dfStations.at[stations_sel,'lon']
                    loc = dfStations.at[stations_sel,'LOCATION']
                    lnk = 'Location: {0}. [Visit station on GOOGLE maps](https://www.google.com/maps/search/?api=1&query={1},{2} "open in GOOGLE maps")'.format(loc, lat, lon)
                    st.markdown(lnk)
                if show_data_sel:
                    st.dataframe(plot_results_list[1])
    else:
        plot('', dfStations)