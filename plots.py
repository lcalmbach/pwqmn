import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import fontus_db as db

plot_type = 'scatter plot'
xpar = '567'
ypar = '123'
group_by = ''
max_x = -99
max_y = -99
min_x = -99
min_y = -99
group_by_dic = {'station':'STATION_NAME','month':'MONTH','year':'YEAR'}
color_schema = "set1" # https://vega.github.io/vega/docs/schemes/#reference

def init(plot_type_sel, xpar_sel, ypar_sel, group_by_sel, max_x_sel, max_y_sel, min_x_sel, min_y_sel):
    global xpar
    global ypar
    global group_by
    global max_x
    global max_y
    global min_x
    global min_y
    global plot_type

    plot_type = plot_type_sel
    xpar = xpar_sel
    ypar = ypar_sel
    group_by = group_by_sel
    max_x = max_x_sel
    max_y = max_y_sel
    min_x = min_x_sel
    min_y = min_y_sel

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
    if plot_type  == 'scatter plot':
        return plot_scatter(plt_title, source)
    elif plot_type == 'time series':
        return plot_time_series(plt_title, source)
    elif plot_type == 'histogram':
        return plot_histogram(plt_title, source)
    elif plot_type == 'boxplot':
        return plot_boxplot(plt_title, source)
    elif plot_type == 'schoeller':
        return plot_schoeller(plt_title, source)
    elif plot_type == 'map':
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

    if max_x == min_x:
        scx = alt.Scale()
    else:
        scx = alt.Scale(domain=(min_x, max_x))

    base = alt.Chart(df, title = plt_title).mark_bar().encode(
        alt.X("RESULT:Q", bin=True, title = x_lab, scale = scx),
        y = 'count()',
    )
    result.append(base)
    result.append(df)
    return result

def plot_map(plt_title, df): 
    df = df[(df['STATION_NAME'] == 19006403102)]
    df1 = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [46., -86.5],
        columns=['lat', 'lon']
    )
    #df = df[['LATITUDE','LONGITUDE']]
    #df = df.rename(index=str, columns={"LATITUDE": "lat", "LONGITUDE": "lon"})
    st.deck_gl_chart(
        viewport={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 10,
        },
        layers=[
            {
                "type": "ScatterplotLayer",
                "data": data,
                "radius": 100,
                "elevationScale": 4,
                "elevationRange": [0, 10000],
                "pickable": True,
                "extruded": False,
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

    base = alt.Chart(source, title = plt_title).mark_line(point = True).encode(
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
    result = []
    x_lab = get_label(xpar)
    y_lab = get_label(ypar)
    df = get_pivot_data(df)
    if set([xpar, ypar]).issubset(df.columns):
        df = df[(df[xpar] > 0) & (df[ypar] > 0)]
        df = df.reset_index()

        if max_x == min_x:
            scx = alt.Scale()
        else:
            scx = alt.Scale(domain=(min_x, max_x))
        
        if max_y == min_y:
            scy = alt.Scale()
        else:
            scy = alt.Scale(domain=(min_y, max_y))

        base = alt.Chart(df, title = plt_title).mark_circle(size=60).encode(
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
        base = alt.Chart(df, title = plt_title).mark_circle(size = 60).encode()
    
    result.append(base)
    result.append(df)
    return result