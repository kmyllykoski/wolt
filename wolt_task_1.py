# -*- coding: utf-8 -*-
__author__ = 'KM'
#
# Conda environment: python 3.8
#
# ==============================================================================
#
# Task 1
#   - SQL query that produces a table showing profitability of each purchase
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


# Connect to Postgres database

con_wolt = psycopg2.connect(host=wolt_config.DATABASE_HOST, dbname=wolt_config.DBNAME, user=wolt_config.USER,
                            password=wolt_config.PASSWORD, port=wolt_config.PORT)
cur_wolt = con_wolt.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Read SQL query from text file

sql_file = r'task1_final.sql'

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

    css_string = '''

        .wolt_style {
            font-size: 11pt;
            font-family: Arial;
            border-collapse: collapse;
            border: 1px solid silver;
            max-width: 960px;
            margin: auto;
        }
        
        .wolt_style td, th {
            padding: 5px;
        }
        
        .wolt_style tr:nth-child(even) {
            background: #E0E0E0;
        }
        
        .wolt_style tr:hover {
            background: silver;
            cursor: pointer;
        }
        '''

    # save css-file so the browser can use it when rendering html
    with open(wolt_config.file_path_for_output + 'wolt_df_style.css', 'w') as f:
        f.write(css_string)

    html_string = '''
    <html>
      <head><title>Wolt Task 1 - Profitability of each purchase</title></head>
      <link rel="stylesheet" type="text/css" href="wolt_df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''

    # OUTPUT HTML FILES - First and last 20 rows in dataframe
    with open(wolt_config.file_path_for_output + 'task_1_first_20_rows.html', 'w') as f:
        f.write(html_string.format(table=df_from_query.loc[0:20].to_html(classes='wolt_style')))

    with open(wolt_config.file_path_for_output + 'task_1_last_20_rows.html', 'w') as f:
        f.write(html_string.format(table=df_from_query.tail(20).to_html(classes='wolt_style')))


