import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import fontus_db as db
import app

plot_type = 'scatter plot'
xpar = ''
ypar = ''
group_by = ''
max_x = -99
max_y = -99
min_x = -99
min_y = -99
bin_size = 0 
group_by_dic = {'station':'STATION_NAME','month':'MONTH','year':'YEAR'}
color_schema = "set1" # https://vega.github.io/vega/docs/schemes/#reference
bar_direction = ''

def init(plot_type_sel, xpar_sel, ypar_sel, group_by_sel, max_x_sel, max_y_sel, min_x_sel, min_y_sel, bin_size_sel, bar_direction_sel):
    global xpar
    global ypar
    global group_by
    global max_x
    global max_y
    global min_x
    global min_y
    global plot_type
    global bin_size
    global bar_direction
    
    plot_type = plot_type_sel
    xpar = xpar_sel
    ypar = ypar_sel
    group_by = group_by_sel
    max_x = max_x_sel
    max_y = max_y_sel
    min_x = min_x_sel
    min_y = min_y_sel
    bin_size = bin_size_sel
    bar_direction = bar_direction_sel

def get_pivot_data(df):
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

def plot(plt_title, source):
    if (plot_type  == 'scatter plot'):
        return plot_scatter(plt_title, source)
    elif (plot_type == 'time series'):
        return plot_time_series(plt_title, source)
    elif (plot_type == 'histogram'):
        return plot_histogram(plt_title, source)
    elif (plot_type == 'box plot'):
        return plot_boxplot(plt_title, source)
    elif (plot_type == 'schoeller'):
        return plot_schoeller(plt_title, source)
    elif (plot_type == 'bar chart' and bar_direction == 'horizontal'):
        return plot_bar_h(plt_title, source)
    elif (plot_type == 'bar chart' and bar_direction == 'vertical'):
        return plot_bar_v(plt_title, source)
    elif (plot_type == 'map'):
        plot_map(plt_title, source)
        return ''
    else:
        return 'invalid plottype'

def plot_schoeller(plt_title, df):
    source = data.iris()

    base = alt.Chart(source).transform_window(
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

def plot_boxplot(plt_title, df):
    result = []
    y_lab = get_label(ypar)
    x_lab = ''
    df = df[(df['PARM'] == ypar) & (df['RESULT'] > 0)]
    base = alt.Chart(df, title = plt_title).mark_boxplot().encode(
            alt.X(group_by_dic[group_by] + ':O', title = group_by.capitalize()),  #, axis=alt.Axis(labelAngle=0)
            alt.Y('RESULT:Q', title = y_lab)
            )
    result.append(base)
    result.append(df)
    return result

def plot_histogram(plt_title, df):
    result = []
    x_lab = get_label(ypar)
    df = df[(df['PARM'] == ypar) & (df['RESULT'] > 0)]
    df = df[['RESULT']]
    brush = alt.selection(type='interval', encodings=['x'])

    if max_x == min_x:
        scx = alt.Scale()
    else:
        scx = alt.Scale(domain=(min_x, max_x))
    #use bin width if user defined
    if bin_size > 0:
        bin_def = alt.Bin(step = bin_size)
    else:
        bin_def = alt.Bin()

    base = alt.Chart(df, title = plt_title).mark_bar().encode(
        alt.X("RESULT:Q", bin = bin_def, title = x_lab, scale = scx),
        
        y = 'count()',
    )
    
    result.append(base)
    result.append(df)
    return result

def plot_bar_h(plt_title, df):
    result = []
    y_lab = get_label(ypar)
    df = df[(df['PARM'] == ypar) & (df['RESULT'] > 0)]
    #brush = alt.selection(type='interval', encodings=['x'])
    if max_y == min_y:
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain=(min_y, max_y))

    base = alt.Chart(data = df, title = plt_title).mark_bar().encode(
        alt.Y(group_by_dic[group_by] + ':O', title = ''),
        alt.X('mean(RESULT):Q', title = y_lab, scale = scy),
    )

    avg = alt.Chart(df).mark_rule(color='red').encode(
        x='mean(RESULT):Q'
    )
    
    result.append(base + avg)
    result.append(df)
    return result

def plot_bar_v(plt_title, df):
    result = []
    y_lab = get_label(ypar)
    df = df[(df['PARM'] == ypar) & (df['RESULT'] > 0)]
    #brush = alt.selection(type='interval', encodings=['x'])
    if max_y == min_y:
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain=(min_y, max_y))
    
    base = alt.Chart(data = df, title = plt_title).mark_bar().encode(
        alt.X(group_by_dic[group_by] + ':O', title = ''),
        alt.Y('mean(RESULT):Q', title = y_lab, scale = scy),
    )

    avg = alt.Chart(df).mark_rule(color='red').encode(
        y = 'mean(RESULT):Q'
    )
    
    result.append(base + avg)
    result.append(df)
    return result

def plot_map(df): 
    #df = df[(df['STATION_NAME'] == 19006403102)]
    #df = pd.DataFrame(
    #   np.random.randn(1000, 2) / [50, 50] + [46., -80.5],
    #    columns=['lat', 'lon']
    #)
    #df = db.dfStations
    #df = df[df['RIVER_NAME'].isin(rivers_sel)]
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

def plot_time_series(plt_title, source):
    result = []
    x_lab = ''
    y_lab = get_label(ypar)
    source = source[(source['PARM'] == ypar) & (source['RESULT'] > 0)]

    if max_y == min_y:
        scy = alt.Scale()
    else:
        scy = alt.Scale(domain=(min_y, max_y))

    base = alt.Chart(source, title = plt_title).mark_line(point = True, clip=True).encode(
        x = alt.X('SAMPLE_DATE:T',
            axis=alt.Axis(title='')),
        y = alt.Y('RESULT:Q',
            scale = scy,
            axis = alt.Axis(title = y_lab)
        ),
        color = alt.Color('STATION_NAME',
            scale = alt.Scale(scheme = color_schema)
        ),
        tooltip = ['STATION_NAME', 'SAMPLE_DATE', 'RESULT']
        )
    result.append(base)
    result.append(source)
    return result

def plot_scatter(plt_title, df):
    ok = False
    result = []

    # remove value < 0
    df = df.reset_index()
    df = df[(df['PARM'].isin([xpar, ypar]))]
    df = get_pivot_data(df)
    ok = (set([xpar, ypar]).issubset(df.columns))

        #filter for non values
    if ok:
        df = df[(df[xpar] > 0) & (df[ypar] > 0)]
        ok = len(df) > 0
    if ok:
        df = df.reset_index()
        x_lab = get_label(xpar)
        y_lab = get_label(ypar)

        if max_x == min_x:
            scx = alt.Scale()
        else:
            scx = alt.Scale(domain=(min_x, max_x))
        
        if max_y == min_y:
            scy = alt.Scale()
        else:
            scy = alt.Scale(domain=(min_y, max_y))

        base = alt.Chart(df, title = plt_title).mark_circle(size=60, clip=True).encode(
            x = alt.X(xpar + ':Q',
                scale = scx,
                axis = alt.Axis(title = x_lab)),
            y = alt.Y(ypar + ':Q',
                scale = scy,
                axis = alt.Axis(title = y_lab)),
                color = alt.Color(group_by_dic[group_by] + ':O',
                    scale=alt.Scale(scheme=color_schema)
                ),
            tooltip=['SAMPLE_DATE', group_by_dic[group_by], xpar, ypar]
        )
    else:
        dfEmpty = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        base = alt.Chart(dfEmpty, title = plt_title).mark_circle(size = 60).encode()
        df = []
        
    result.append(base)
    result.append(df)
    return result