import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import plots as plt

rivers = list()
dfSamples = pd.DataFrame
dfStations = pd.DataFrame
year = 0
color_schema = "set1" # https://vega.github.io/vega/docs/schemes/#reference

plot_type_list = ['scatter plot','time series','histogram','boxplot'] #, 'schoeller', 'map',
group_by_list = ['station','year','month']
group_by_dic = {'station':'STATION_NAME','month':'MONTH','year':'YEAR'}
months_list = ['<all>','1','2','3','4','5','6','7','8','9','10','11','12']
year_min = 1994 # todo! make dynamic
year_max = 2016 # todo! make dynamic
month_sel = 0
year_sel = 0
xpar_sel = ''
max_x_sel = -99
max_y_sel = -99
main_x_sel = -99
min_y_sel = -99
stations_sel = ''
plot_width = 600
plot_height = 400
filter_by_year_sel = False
filter_by_month_sel = False

#functions

# General plot routine. Calls the appropriate plot function depending on the active plot type

@st.cache
def read_samples():
    df = pd.read_csv(r"data/pwqmn_chemistry_data.txt",sep='\t',encoding = "ISO-8859-1", float_precision='high')
    df['SAMPLE_DATE'] = pd.to_datetime(df['SAMPLE_DATE'])
    df['MONTH'] = df['SAMPLE_DATE'].dt.month
    df['YEAR'] = df['SAMPLE_DATE'].dt.year
    df['LONGITUDE'] = df['LONGITUDE'].astype(np.float, 10)
    df['LATITUDE'] = df['LATITUDE'].astype(np.float, 10)
    df['RESULT'] = df['RESULT'].astype(np.float, 10)
    return df

@st.cache
def read_stations():
    result = pd.read_csv(r"data/pwqmn_stations.txt",sep='\t', encoding = "ISO-8859-1", float_precision = 'round_trip')
    result.set_index("STATION_NAME", inplace = True)
    return result

@st.cache
def read_parameters():
    result = pd.read_csv(r"data\PWQMN_Parameters.txt",sep='\t',encoding = "ISO-8859-1")
    return result

def get_pivot_data(df):
    if group_by_sel == 'station':
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'STATION_NAME', 'RIVER_NAME', 'MONTH', 'YEAR'], columns=['PARM'], aggfunc=np.average)
    elif group_by_sel == 'month':
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'MONTH', 'RIVER_NAME','YEAR'], columns=['PARM'], aggfunc=np.average)
    else:
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'YEAR', 'RIVER_NAME'], columns=['PARM'], aggfunc=np.average)
    
    return result

def get_rivers():
    result = dfStations.RIVER_NAME.unique()
    result.sort()
    return result

def get_stations(df):
    result = df.STATION_NAME.unique()
    result = np.insert(result,0,'<all stations>')
    result.sort()
    return result

def get_parameters(df):
    result = df.PARM.unique()
    result.sort()
    return result

# start
#prepare data
dfSamples = read_samples()
dfStations = read_stations()
rivers_list = get_rivers()
stations_list = get_stations
parameters_list = get_parameters(dfSamples)

st.header('Provincial (Stream) Water Quality Monitoring Network Data 1964 - 2014')
lnk = '[PMNWQ Home](https://www.ontario.ca/data/provincial-stream-water-quality-monitoring-network "download data")'
st.markdown(lnk)

#sidebar

plot_type_sel = st.sidebar.selectbox('Plot type', plot_type_list)
group_by_sel = st.sidebar.selectbox('Group by', pd.Series(group_by_list))
rivers_sel = st.sidebar.multiselect('Surface water body', pd.Series(rivers_list))
#multi_parameters = st.sidebar.multiselect('Parameters', pd.Series(parameters_list))

if plot_type_sel != 'time series':
    xpar_sel = st.sidebar.selectbox('X-parameter',pd.Series(parameters_list), index = 4)

ypar_sel = st.sidebar.selectbox('Y-parameter', pd.Series(parameters_list), index = 21)

if plot_type_sel != 'time series':
    filter_month_sel = st.sidebar.checkbox('Filter data by month', value=False, key=None)
    if filter_month_sel:
        month_sel = st.sidebar.slider('Month', min_value = 0, max_value = 12, value=None)
    filter_year_sel = st.sidebar.checkbox('Filter data by year', value=False, key=None)
    if filter_year_sel:
        year_sel = st.sidebar.slider('Year', min_value = year_min, max_value = year_max, value=None)

min_x_sel = st.sidebar.number_input('Minimum X')
max_x_sel = st.sidebar.number_input('Maximum X')
max_y_sel = st.sidebar.number_input('Minimum y')
min_y_sel = st.sidebar.number_input('Maximum y')
show_data_sel = st.sidebar.checkbox('Show detail data', value=False, key=None)

if plot_type_sel != 'map':
    for riv in rivers_sel:
        dfRiver = dfSamples[(dfSamples['RIVER_NAME'] == riv)]
        if filter_month_sel:
            dfRiver = dfRiver[(dfRiver.MONTH == int(month_sel))]
        if filter_year_sel:
            dfRiver = dfRiver[(dfRiver.YEAR == int(year_sel))]

        if plot_type_sel != 'map':
            if len(rivers_sel) == 1:
                plot_title = riv
                stations_sel = st.selectbox('Stations', pd.Series(get_stations(dfRiver)))
                show_all_stations = (stations_sel == '<all stations>')
                if not show_all_stations:
                    dfRiver = dfRiver[(dfRiver['STATION_NAME'] == stations_sel)]
                    plot_title += ': ' + stations_sel

            plot_results_list = plot(plot_title, dfRiver)
            st.write(plot_results_list[0].properties(width = plot_width, height = plot_height))
            
            # if a station has been selected display a link to visit site on google mpas
            if show_all_stations == False:
                lnk = '[Visit station on GOOGLE maps](https://www.google.com/maps/search/?api=1&query={0},{1} "open in GOOGLE maps")'.format(dfStations.at[stations_sel,'lat'], dfStations.at[stations_sel,'lon'])
                st.markdown(lnk)
            if show_data_sel:
                st.dataframe(plot_results_list[1])
else:
    plot('', dfStations)



    