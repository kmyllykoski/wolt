# -*- coding: utf-8 -*-
__author__ = 'KM'
#
# Conda environment: python 3.8
#
# ==============================================================================
#
# Task 2 - Part A
#   - Plot top 10 venues with highest margins and relation to average order size
#   
#   - Uses parameters and output directory imported from file wolt.config.py
#   - Uses SQL query imported from a text file
#
# ==============================================================================
import os
import psycopg2
import psycopg2.extras
import wolt_config
import pandas as pd
import plotly.graph_objects as go

# Connect to Postgres database

con_wolt = psycopg2.connect(host=wolt_config.DATABASE_HOST, dbname=wolt_config.DBNAME, user=wolt_config.USER,
                            password=wolt_config.PASSWORD, port=wolt_config.PORT)
cur_wolt = con_wolt.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Read SQL from text file

sql_file = r'task2-a_final.sql'

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

    # yaxis range adjusted with 10 % of maximum value in data
    yaxis_max_value = df_from_query['margin_per_venue_ex_vat_eur'].iloc[0]
    yaxis_adjustment_amount = yaxis_max_value * 0.1
    # yaxis range adjusted to stop above maximum value in data
    yaxis_range_stop = yaxis_max_value + yaxis_adjustment_amount

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_from_query['venue_id'],
            y=df_from_query['purchase_avg_count'],
            name="Order size avg",
            text=df_from_query['purchase_avg_count'],
            textposition='middle center',
            textfont=dict(
                size=13,
                color='white'),
            mode='lines+markers+text',
            marker={'size': 24},
            line=dict(color='firebrick', width=3),
            yaxis="y2"
        ))
    fig.add_trace(
        go.Bar(
            x=df_from_query['venue_id'],
            y=df_from_query['margin_per_venue_ex_vat_eur'],
            name="Margin",
            text=df_from_query['margin_per_venue_ex_vat_eur'],
            textposition='outside',
            textfont=dict(
                size=13,
                color='#1f77b4'),
            marker_color='rgb(0, 194, 232)',
            marker_line_color='rgb(17, 69, 126)',
            marker_line_width=2,
            opacity=1.0
        ))
    # 
    fig.update_layout(
        title={
            'text': '<b>Top 10 venues with highest margin and their average order size</b>',
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
            title='Margin Euro',
            titlefont_size=16,
            tickfont_size=14),
        yaxis2=dict(
            title='Order size',
            overlaying="y",
            side="right",
            titlefont_size=16,
            tickfont_size=14,
            color="firebrick"),
        bargap=0.15
    )
    fig.update_layout(legend=dict(
            x=0.5,
            y=-0.25,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            yanchor="top",
            xanchor="center",
            orientation="h"
        ),)
    fig.update_layout(yaxis_range=[0, yaxis_range_stop])
    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(yaxis2=dict(showgrid=False))
    fig.write_html(wolt_config.file_path_for_output + sql_file[:-3] + 'html', auto_open=True)
    fig.write_image(wolt_config.file_path_for_output + sql_file[:-3] + 'svg')

