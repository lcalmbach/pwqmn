import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import fontus_db as db
import constants as cn


group_by_dic = {'station':'STATION_NAME','month':'MONTH','year':'YEAR'}

def get_pivot_data(df, group_by):
    if group_by == 'station':
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'STATION_NAME', 'RIVER_NAME', 'MONTH', 'YEAR'], columns=['PARM'], aggfunc=np.average)
    elif group_by == 'month':
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'MONTH', 'RIVER_NAME','YEAR'], columns=['PARM'], aggfunc=np.average)
    else:
        result = pd.pivot_table(df, values='RESULT', index=['SAMPLE_DATE', 'YEAR', 'RIVER_NAME'], columns=['PARM'], aggfunc=np.average)
    
    return result

# returns the label for a given parameter key. 
def get_label(value):
    df = db.dfParameters[(db.dfParameters['PARM'] == value)]
    df = df.set_index("PARM", drop = False)
    return  df.at[value, 'LABEL']

def plot(plt_title, df, ctrl):
    if (ctrl['plot_type']  == 'scatter plot'):
        return plot_scatter(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'time series'):
        return plot_time_series(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'histogram'):
        return plot_histogram(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'box plot'):
        return plot_boxplot(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'schoeller'):
        return plot_schoeller(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'bar chart' and ctrl['bar_direction'] == 'horizontal'):
        return plot_bar_h(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'bar chart' and ctrl['bar_direction'] == 'vertical'):
        return plot_bar_v(plt_title, df, ctrl)
    elif (ctrl['plot_type'] == 'map'):
        plot_map(plt_title, df, ctrl)
        return ''
    else:
        return 'invalid plottype'

def plot_schoeller(plt_title, df, ctrl):
    df = data.iris()

    base = alt.Chart(df).transform_window(
        index='count()'
        ).transform_fold(
            ['petalLength', 'petalWidth', 'sepalLength', 'sepalWidth']
        ).mark_line().encode(
            x='key:N',
            y='value:Q',
            color='species:N',
            detail='index:N',
            opacity=alt.value(0.5)
        )
    return base

def plot_boxplot(plt_title, df, ctrl):
    result = []
    y_lab = get_label(ctrl['ypar'])
    x_lab = ''
    df = df[(df['PARM'] == ctrl['ypar']) & (df['RESULT'] > 0)]
    
    if ctrl['max_y'] == ctrl['min_y']:
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain=(ctrl['min_y'], ctrl['max_y']))
    
    base = alt.Chart(df, title = plt_title).mark_boxplot(clip=True).encode(
            alt.X(group_by_dic[ctrl['group_by']] + ':O', title = ctrl['group_by'].capitalize()),  #, axis=alt.Axis(labelAngle=0)
            alt.Y('RESULT:Q', title = y_lab, scale = scy)
            )
    result.append(base)
    result.append(df)
    return result

def plot_histogram(plt_title, df, ctrl):
    result = []
    x_lab = get_label(ctrl['ypar'])
    df = df[(df['PARM'] == ctrl['ypar']) & (df['RESULT'] > 0)]
    df = df[['RESULT']]
    brush = alt.selection(type='interval', encodings=['x'])

    if ctrl['max_x'] == ctrl['min_x']:
        scx = alt.Scale()
    else:
        scx = alt.Scale(domain=(ctrl['min_x'], ctrl['max_x']))
    #use bin width if user defined
    if ctrl['bin_size'] > 0:
        bin_def = alt.Bin(step = ctrl['bin_size'])
    else:
        bin_def = alt.Bin()

    base = alt.Chart(df, title = plt_title).mark_bar().encode(
        alt.X("RESULT:Q", bin = bin_def, title = x_lab, scale = scx),
        
        y = 'count()',
    )
    
    result.append(base)
    result.append(df)
    return result

def plot_bar_h(plt_title, df, ctrl):
    result = []
    y_lab = get_label(ctrl['ypar'])
    df = df[(df['PARM'] == ctrl['ypar']) & (df['RESULT'] > 0)]
    #brush = alt.selection(type='interval', encodings=['x'])
    if (ctrl['max_y'] == ctrl['min_y']):
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain = [ctrl['min_y'], ctrl['max_y']])

    base = alt.Chart(data = df, title = plt_title).mark_bar().encode(
        alt.Y(group_by_dic[ctrl['group_by']] + ':O', title = ''),
        alt.X('mean(RESULT):Q', title = y_lab, scale = scy),
    )

    avg = alt.Chart(df).mark_rule(color='red').encode(
        x='mean(RESULT):Q'
    )
    
    result.append(base + avg)
    result.append(df)
    return result

def plot_bar_v(plt_title, df, ctrl):
    result = []
    y_lab = get_label(ctrl['ypar'])
    df = df[(df['PARM'] == ctrl['ypar']) & (df['RESULT'] > 0)]
    #brush = alt.selection(type='interval', encodings=['x'])
    if (ctrl['max_y'] == ctrl['min_y']):
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain= [ctrl['min_y'], ctrl['max_y']])
    
    base = alt.Chart(data = df, title = plt_title).mark_bar().encode(
        alt.X(group_by_dic[ctrl['group_by']] + ':O', title = ''),
        alt.Y('mean(RESULT):Q', title = y_lab, scale = scy),
    )

    avg = alt.Chart(df).mark_rule(color='red').encode(
        y = 'mean(RESULT):Q'
    )
    
    result.append(base + avg)
    result.append(df)
    return result

def plot_map(df, ctrl): 
    #df = df[(df['STATION_NAME'] == 19006403102)]
    #df = pd.DataFrame(
    #   np.random.randn(1000, 2) / [50, 50] + [46., -80.5],
    #    columns=['lat', 'lon']
    #)
    #df = db.dfStations
    #df = df[df['RIVER_NAME'].isin(rivers)]
    #if df.count == 0:
    #    df = dfStations

    midpoint = (np.average(df['lat']), np.average(df['lon']))
    st.deck_gl_chart(
        viewport={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 20,
            "pitch": 0,
        },
        layers=[
            {
                'type': 'ScatterplotLayer',
                'data': df,
                'radiusScale': 10,
                'radiusMinPixels': 5,
                'radiusMaxPixels': 15,
                'elevationScale': 4,
                'elevationRange': [0, 10000],
                'getFillColor': [255,0,0]
            }
        ],
    )

def plot_time_series(plt_title, df, ctrl):
    result = []
    x_lab = ''
    y_lab = get_label(ctrl['ypar'])
    df = df[(df['PARM'] == ctrl['ypar']) & (df['RESULT'] > 0)]
    if ctrl['max_y'] == ctrl['min_y']:
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain=(ctrl['min_y'], ctrl['max_y']))

    base = alt.Chart(df, title = plt_title).mark_line(point = True, clip=True).encode(
        x = alt.X('SAMPLE_DATE:T',
            axis=alt.Axis(title = '')),
        y = alt.Y('RESULT:Q',
            scale = scy,
            axis = alt.Axis(title = y_lab)
        ),
        color = alt.Color('STATION_NAME',
            scale = alt.Scale(scheme = cn.color_schema)
        ),
        tooltip = ['STATION_NAME', 'SAMPLE_DATE', 'RESULT']
        )
    result.append(base)
    result.append(df)
    return result

def plot_scatter(plt_title, df, ctrl):
    ok = False
    result = []

    # remove value < 0
    df = df.reset_index()
    df = df[(df['PARM'].isin([ctrl['xpar'], ctrl['ypar']]))]
    df = get_pivot_data(df, ctrl['group_by'])
    ok = (set([ctrl['xpar'], ctrl['ypar']]).issubset(df.columns))

    #filter for non values
    if ok:
        df = df[(df[ctrl['xpar']] > 0) & (df[ctrl['ypar']] > 0)]
        ok = len(df) > 0
    if ok:
        df = df.reset_index()
        x_lab = get_label(ctrl['xpar'])
        y_lab = get_label(ctrl['ypar'])

        if (ctrl['max_x'] == ctrl['min_x']):
            scx = alt.Scale()
        else:
            scx = alt.Scale(domain=(ctrl['min_x'], ctrl['max_x']))
        
        if ctrl['max_y'] == ctrl['min_y']:
            scy = alt.Scale()
        else:
            scy = alt.Scale(domain=(ctrl['min_y'], ctrl['max_x']))

        base = alt.Chart(df, title = plt_title).mark_circle(size = cn.symbol_size, clip = True).encode(
            x = alt.X(ctrl['xpar'] + ':Q',
                scale = scx,
                axis = alt.Axis(title = x_lab)),
            y = alt.Y(ctrl['ypar'] + ':Q',
                scale = scy,
                axis = alt.Axis(title = y_lab)),
                color = alt.Color(group_by_dic[ctrl['group_by']] + ':O',
                    scale=alt.Scale(scheme = cn.color_schema)
                ),
            tooltip=['SAMPLE_DATE', group_by_dic[ctrl['group_by']], ctrl['xpar'], ctrl['ypar']]
        )
    else:
        dfEmpty = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        base = alt.Chart(dfEmpty, title = plt_title).mark_circle(size = cn.symbol_size).encode()
        df = []
        
    result.append(base)
    result.append(df)
    return result