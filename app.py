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

bin_size_sel = 0    #width of bin for histograms
rivers = list()
# dfSamples = pd.DataFrame
# dfStations = pd.DataFrame
txt.init()

plot_type_list = ['bar chart','box plot','scatter plot','time series','histogram','map'] #, 'schoeller', ,
group_by_list = ['station','year','month']
months_list = ['<all>','1','2','3','4','5','6','7','8','9','10','11','12']
menu_list = ['Plotting', 'Station information', 'Parameters information', 'Settings', 'Help', 'About']
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
bin_size_sel = 0
year_sel = 0
bar_direction_sel = 'vertical'

#prepare data
db.init()
#dfSamples = db.dfSamples
#dfStations = db.dfStations
#dfParameters = db.dfParameters
rivers_list = db.get_rivers(db.dfStations)
stations_list = db.get_stations
parameters_list = parameters.get_parameters(db.dfParameters)

#sidebar
st.sidebar.header('Menu')
menu_sel = st.sidebar.radio('', menu_list, index=5, key=None) # format_func=<class 'str'>, 
st.sidebar.markdown('---')

if menu_sel == 'About':
    txt.print_main_about(db.dfStations, db.dfParameters, db.dfSamples)
elif menu_sel == 'Help':
    txt.print_help()
elif menu_sel == 'Station information':
    st.header(menu_sel)
    stations.init(db.dfStations)
    #sidebar menu
    all_rivers_sel = st.sidebar.checkbox('All stations', value=False, key=None)
    if not all_rivers_sel:
        rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist()) 
    # content
    df = stations.get_table(all_rivers_sel, rivers_sel)
    df.reset_index(inplace = True) #needed so station_name can be selected on plotly table
    values =[df.STATION_NAME, df.RIVER_NAME, df.LOCATION, df.lon, df.lat, df.STATUS, df.FIRST_YR, df.LAST_YR, df.TOTAL_YRS, df.MISS_YRS]
    txt.show_table(df,values)
    if not all_rivers_sel:
        text = "This list only includes stations from the selected surface water bodies."
    else:
        text = "This list includes all stations of the monitoring network."
    st.markdown(text)
elif menu_sel == 'Parameters information':
    st.header(menu_sel)
    parameters.init(db.dfParameters, db.dfSamples)
    #sidebar menu
    all_rivers_sel = st.sidebar.checkbox('All stations', value=False, key=None)
    if not all_rivers_sel:
        rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist()) 
    # content
    df = parameters.get_table(all_rivers_sel, rivers_sel)
    df = df[['PARM', 'PARM_DESCRIPTION', 'DESCRIPTION']]
    values = [df.PARM, df.PARM_DESCRIPTION, df.DESCRIPTION]
    txt.show_table(df,values)
    if not all_rivers_sel:
        text = "This parameter list only includes parameters having been measured in the selected rivers or lakes."
    else:
        text = "This parameter list includes all parameters having been measured in the monitoring network."
    st.markdown(text)
elif menu_sel == 'Plotting':
    plot_type_sel = st.sidebar.selectbox('Plot type', plot_type_list)
    if plot_type_sel not in ['time series']:
        group_by_sel = st.sidebar.selectbox('Group by', pd.Series(group_by_list))
    rivers_sel = st.sidebar.multiselect(label = 'Surface water body', default = ('Grand River',), options = pd.Series(rivers_list).tolist())

    parameters_list = parameters.get_sample_parameters(rivers_sel)
    if plot_type_sel not in ['time series', 'histogram', 'boxplot', 'bar chart']:
        xpar_sel = parameters.get_parameter_key(st.sidebar.selectbox('X-parameter', parameters_list, index = 0))
    ypar_sel = parameters.get_parameter_key(st.sidebar.selectbox('Y-parameter', parameters_list, index = 1))
    if plot_type_sel not in ['time series']:
        filter_month_sel = st.sidebar.checkbox('Filter data by month', value = False, key=None)
        if filter_month_sel:
            month_sel = st.slider('Month', min_value = 0, max_value = 12, value=None)
        filter_year_sel = st.sidebar.checkbox('Filter data by year', value=False, key=None)
        if filter_year_sel:
            year_sel = st.slider('Year', min_value = int(db.first_year), max_value = int(db.last_year), value = int(db.first_year)) #db.first_year, max_value = db.last_year)
    if plot_type_sel == 'histogram':
        bin_size_sel = st.sidebar.number_input('Bin width')
    define_axis_limits = st.sidebar.checkbox('Define axis limits', value=False, key=None)
    if define_axis_limits:
        if plot_type_sel not in ['time series']:
            min_x_sel = st.sidebar.number_input('Minimum X')
            max_x_sel = st.sidebar.number_input('Maximum X')
        min_y_sel = st.sidebar.number_input('Minimum y')
        max_y_sel = st.sidebar.number_input('Maximum y')
    if plot_type_sel == 'bar chart':
        bar_direction_sel = st.sidebar.radio('Bars', ['vertical', 'horizontal'])

    define_axis_length = st.sidebar.checkbox('Define axis length', value=False)
    if define_axis_length:
        plot_width = st.sidebar.number_input('Width (pixel)', value = plot_width)
        plot_height = st.sidebar.number_input('Height (pixel)', value = plot_height)
    
    show_data_sel = st.sidebar.checkbox('Show detail data', value = False, key = None)
    plt.init(plot_type_sel, xpar_sel, ypar_sel, group_by_sel, max_x_sel, max_y_sel, min_x_sel, min_y_sel, bin_size_sel, bar_direction_sel)
    
    if plot_type_sel != 'map':
        for riv in rivers_sel:
            dfRiver = db.dfSamples[(db.dfSamples['RIVER_NAME'] == riv)]
            if filter_month_sel:
                dfRiver = dfRiver[(dfRiver.MONTH == int(month_sel))]
            if filter_year_sel:
                dfRiver = dfRiver[(dfRiver.YEAR == int(year_sel))]
            plot_title = riv
            show_all_stations = True
            
            if len(rivers_sel) == 1:
                stations_sel = st.selectbox('Stations', pd.Series(db.get_stations(dfRiver)))
                show_all_stations = (stations_sel == '<all stations>')
                if not show_all_stations:
                    dfRiver = dfRiver[(dfRiver['STATION_NAME'] == stations_sel)]
                    plot_title += ': ' + stations_sel
            plot_results_list = plt.plot(plot_title, dfRiver)
            # verify if the data has rows
            if (len(plot_results_list[1]) > 0):
                st.write(plot_results_list[0].properties(width = plot_width, height = plot_height))
                # if a station has been selected display a link to visit site on google maps
                if not show_all_stations and len(rivers_sel) == 1:
                    db.dfStations.set_index('STATION_NAME', inplace = True)
                    lat = db.dfStations.at[stations_sel,'lat']
                    lon = db.dfStations.at[stations_sel,'lon']
                    loc = db.dfStations.at[stations_sel,'LOCATION']
                    lnk = 'Location: {0}. [Visit station on GOOGLE maps](https://www.google.com/maps/search/?api=1&query={1},{2} "open in GOOGLE maps")'.format(loc, lat, lon)
                    st.markdown(lnk)
                if show_data_sel:
                    st.dataframe(plot_results_list[1])
            else:
                st.write('No data found')
    else:
        dfRiver = []
        show_all_stations = True
        if len(rivers_sel) == 0:
            dfRiver = db.dfStations
        elif len(rivers_sel) == 1:
            dfRiver = db.dfStations[(db.dfStations['RIVER_NAME'] == rivers_sel[0])]
            show_all_stations = (stations_sel == '<all stations>')
            if not show_all_stations:
                dfRiver = dfRiver[(dfRiver['STATION_NAME'] == stations_sel)]
        plt.plot_map(dfRiver)

st.sidebar.markdown('---')
txt.info_sideboard('ABOUT')