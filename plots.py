import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

def plot(plt_title, source):
    if plot_type_sel == 'scatter plot':
        return plot_scatter(plt_title, source)
    elif plot_type_sel == 'time series':
        return plot_time_series(plt_title, source)
    elif plot_type_sel == 'histogram':
        return plot_histogram(plt_title, source)
    elif plot_type_sel == 'boxplot':
        return plot_boxplot(plt_title, source)
    elif plot_type_sel == 'schoeller':
        return plot_schoeller(plt_title, source)
    elif plot_type_sel == 'map':
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
    x_lab = xpar_sel
    y_lab = ypar_sel
    df = df[(df['PARM'] == ypar_sel) & (df['RESULT'] > 0)]
    base = alt.Chart(df, title = plt_title).mark_boxplot().encode(
            alt.X('YEAR:O', title = group_by_sel.capitalize()),
            alt.Y('RESULT:Q', title = y_lab )
            )
    result.append(base)
    result.append(df)
    return result

def plot_histogram(plt_title, df):
    result = []
    x_lab = xpar_sel
    y_lab = ypar_sel
    df = df[(df['PARM'] == ypar_sel) & (df['RESULT'] > 0)]
    df = df[['RESULT']]
    base = alt.Chart(df, title = plt_title).mark_bar().encode(
        alt.X("RESULT:Q", bin=True, title = y_lab),
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
    y_lab = ypar_sel
    source = source[(source['PARM'] == ypar_sel) & (source['RESULT'] > 0)]

    base = alt.Chart(source, title = plt_title).mark_line(point = True).encode(
        x = alt.X('SAMPLE_DATE:T',
            axis=alt.Axis(title='')
        ),
        y = alt.Y('RESULT:Q',
            #scale=alt.Scale(
            #    domain=(0, 250000),
            #),
            axis = alt.Axis(title = y_lab)
        ),
        color = alt.Color('STATION_NAME',
            scale=alt.Scale(scheme = color_schema)
        ),
        tooltip = ['STATION_NAME', 'SAMPLE_DATE', 'RESULT']
        )
    result.append(base)
    result.append(source)
    return result

def plot_scatter(plt_title, df): 
    result = []
    x_lab = xpar_sel
    y_lab = ypar_sel
    df = get_pivot_data(df)
    if set([xpar_sel, ypar_sel]).issubset(df.columns):
        df = df[(df[xpar_sel] > 0) & (df[ypar_sel] > 0)]
        df = df.reset_index()
        if max_x_sel == min_x_sel:
            scx = alt.Scale()
        else:
            scx = alt.Scale(domain=(min_x_sel, max_x_sel))
        
        if max_y_sel == min_y_sel:
            scy = alt.Scale()
        else:
            scy = alt.Scale(domain=(min_y_sel, max_y_sel))

        base = alt.Chart(df, title = plt_title).mark_circle(size=60).encode(
            x = alt.X(xpar_sel + ':Q',
                scale = scx,
                axis = alt.Axis(title = x_lab)),
            y = alt.Y(ypar_sel + ':Q',
                scale = scy,
                axis = alt.Axis(title = y_lab)),
                color = alt.Color(group_by_dic[group_by_sel] + ':O',
                    scale=alt.Scale(scheme=color_schema)
                ),
            tooltip=['SAMPLE_DATE', group_by_dic[group_by_sel], x_lab, y_lab]
        )
    else:
        base = alt.Chart(df, title = plt_title).mark_circle(size=60).encode(
        )
    result.append(base)
    result.append(df)
    return result