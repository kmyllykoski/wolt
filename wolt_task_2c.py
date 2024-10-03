# -*- coding: utf-8 -*-
__author__ = 'KM'
#
# Conda environment: python 3.8
#
# ==============================================================================
#
# Task 2 - Part C - monthly woltwide margin
#   - Plot cumulative monthly woltwide margin
#   
#   - Uses parameters imported from file wolt.config.py
#   - Uses SQL query imported from a text file
#
# ==============================================================================
import os
import psycopg2
import psycopg2.extras
import wolt_config
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go
import datetime

# Connect to Postgres database

con_wolt = psycopg2.connect(host=wolt_config.DATABASE_HOST, dbname=wolt_config.DBNAME, user=wolt_config.USER,
                            password=wolt_config.PASSWORD, port=wolt_config.PORT)
cur_wolt = con_wolt.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Read SQL from text file

sql_file = r'task2-c_final.sql'

with open(sql_file) as file:
    SQL_WOLT = file.read()
    
    print(SQL_WOLT)

    if not os.path.isfile(wolt_config.file_path_for_pickle_files + sql_file + '.pkl'):
        print('pickle not found on disk - saving query results as pickle file')
        df_from_query = pd.read_sql(SQL_WOLT, con_wolt)
        df_from_query.to_pickle(wolt_config.file_path_for_pickle_files + sql_file + '.pkl')
    else:
        print('pickle found on disk - reading from pickle file')
        df_from_query = pd.read_pickle(wolt_config.file_path_for_pickle_files + sql_file + '.pkl')

    print(df_from_query)

    # -------------------------------------------------------------------------
    # To keep the layout of the chart intact when new data is added
    # following adjustments to plot axis ranges are made based on current data

    # xaxis range adjusted to begin 15 days before beginning of first month in data
    first_date_in_data = datetime.datetime.strptime(df_from_query['year_month'].iloc[0], '%Y-%m')
    xaxis_range_start_date = first_date_in_data - datetime.timedelta(days=15)

    # xaxis range adjusted to stop 15 days after beginning of last month in data
    last_date_in_data = datetime.datetime.strptime(df_from_query['year_month'].iloc[-1], '%Y-%m')
    xaxis_range_stop_date = last_date_in_data + datetime.timedelta(days=15)

    # yaxis range adjusted with 10 % of maximum value in data
    yaxis_max_value = df_from_query['cumulative_margin'].iloc[-1]
    yaxis_adjustment_amount = yaxis_max_value * 0.1
    # yaxis range adjusted to start below zero
    yaxis_range_start = yaxis_adjustment_amount * -1
    # yaxis range adjusted to stop above maximum value in data
    yaxis_range_stop = yaxis_max_value + yaxis_adjustment_amount
    # -------------------------------------------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_from_query['year_month'],
            y=df_from_query['cumulative_margin'],
            name="Cumulative Woltwide margin",
            text=df_from_query['cumulative_margin'],
            textposition='middle center',
            textfont=dict(
                size=13,
                color='white'),
            mode='lines+markers+text',
            marker={'size': 45},
            line=dict(color='rgb(0, 194, 232)', width=3),
            marker_color='rgb(0, 194, 232)',
            marker_line_color='rgb(17, 69, 126)',
            marker_line_width=2,
            opacity=1.0,
            showlegend=False,
            fill='tozeroy'
        )
    )

    fig.update_layout(
        title={
            'text': '<b>Woltwide cumulative margin</b>',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(color="black")
    )

    fig.update_layout(
        showlegend=True,
        plot_bgcolor="rgb(240,240,240)",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Margin (euro)',
            titlefont_size=16,
            tickfont_size=14),
        bargap=0.15,
    )

    fig.update_layout(yaxis_range=[yaxis_range_start, yaxis_range_stop])
    fig.update_traces(texttemplate='%{text:.3s}')
    fig.update_xaxes(autorange=False)
    fig.update_layout(xaxis_range=[xaxis_range_start_date, xaxis_range_stop_date])
    fig.write_html(wolt_config.file_path_for_output + sql_file[:-3] + 'html', auto_open=True)
    fig.write_image(wolt_config.file_path_for_output + sql_file[:-3] + 'svg')

print('xxxxxxx end xxxxxxx')