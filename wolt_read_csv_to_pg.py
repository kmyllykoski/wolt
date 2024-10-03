# -*- coding: utf-8 -*-
__author__ = 'KM'
#
# Conda environment: python 3.8
#
# ==============================================================================
#
# Create Postgres tables and read assigment data from csv files to tables:
#   - purchase
#   - purchase_item
#   - item
#
# Uses parameters imported from file wolt_config.py
# ==============================================================================
import csv
import psycopg2
import psycopg2.extras
import wolt_config

# Connect to Postgres database

con_wolt = psycopg2.connect(host=wolt_config.DATABASE_HOST, dbname=wolt_config.DBNAME,
                            user=wolt_config.USER, password=wolt_config.PASSWORD, port=wolt_config.PORT)
cur_wolt = con_wolt.cursor(cursor_factory=psycopg2.extras.DictCursor)

#
# Function for reading a single csv file into Postgres
#
def read_csv_to_postgres(csvfile_in, SQL_insert_command):
    reader = csv.DictReader(csvfile_in, delimiter=',')
    fields_with_missing_data = []
    for row in reader:
        for field in row:
            if row[field] == '':
                row[field] = None
                if field not in fields_with_missing_data:
                    fields_with_missing_data.append(field)

        data_insert = tuple(list(row.values())[1:])
        cur_wolt.execute(SQL_insert_command, data_insert)

    if len(fields_with_missing_data) > 0:
        print('---------------------------------')
        print('Fields with missing data:')
        for f in fields_with_missing_data:
            print(f)
        print('')


with open(wolt_config.file_purchase, encoding="utf-8") as csvfile:
    print(f'reading file {wolt_config.file_purchase}...')
    SQL_command = '''DROP TABLE IF EXISTS purchase'''
    cur_wolt.execute(SQL_command)
    SQL_command = '''CREATE TABLE purchase(
                        purchase_id CHAR(10) PRIMARY KEY,
                        time_received TIMESTAMP,
                        time_delivered TIMESTAMP,
                        currency CHAR(3),
                        country CHAR(3),
                        venue_id CHAR(10) ) '''
    #
    cur_wolt.execute(SQL_command)
    SQL_insert_purchase = '''INSERT INTO purchase(
                                purchase_id,
                                time_received,
                                time_delivered,
                                currency,
                                country,
                                venue_id )
                             VALUES (%s, %s, %s, %s, %s, %s) '''

    read_csv_to_postgres(csvfile, SQL_insert_purchase)

    print('done!')

with open(wolt_config.file_purchase_item, encoding="utf-8") as csvfile:
    print(f'reading file {wolt_config.file_purchase_item}...')
    SQL_command = '''DROP TABLE IF EXISTS purchase_item'''
    cur_wolt.execute(SQL_command)
    SQL_command = '''CREATE TABLE purchase_item(
                        product_id CHAR(10),
                        purchase_id CHAR(10),
                        count INT,
                        venue_id CHAR(10),
                        baseprice FLOAT,
                        vat_percentage FLOAT ) '''
    #
    cur_wolt.execute(SQL_command)
    SQL_insert_purchase_item = '''INSERT INTO purchase_item(
                                     product_id,
                                     purchase_id,
                                     count,
                                     venue_id,
                                     baseprice,
                                     vat_percentage )
                                VALUES (%s, %s, %s, %s, %s, %s) '''
    #
    read_csv_to_postgres(csvfile, SQL_insert_purchase_item)

    print('done!')

with open(wolt_config.file_item, encoding="utf-8") as csvfile:
    print(f'reading file {wolt_config.file_item}...')
    command = '''DROP TABLE IF EXISTS item'''
    cur_wolt.execute(command)
    command = '''CREATE TABLE item(
                    venue_id CHAR(10),
                    available_date DATE,
                    brand VARCHAR,
                    manufacturer VARCHAR,
                    cost_per_unit FLOAT,
                    cost_per_unit_eur FLOAT,
                    currency CHAR(3),
                    applicable_tax_perc FLOAT,
                    product_id CHAR(10),
                    item_identifier_gtin CHAR(10),
                    external_id CHAR(10) ) '''
    #
    cur_wolt.execute(command)
    SQL_insert_item = '''INSERT INTO item(
                            venue_id,
                            available_date,
                            brand,
                            manufacturer,
                            cost_per_unit,
                            cost_per_unit_eur,
                            currency,
                            applicable_tax_perc,
                            product_id,
                            item_identifier_gtin,
                            external_id )
                          VALUES (%s, %s, %s, %s, %s,
                                  %s, %s, %s, %s, %s, %s) '''

    read_csv_to_postgres(csvfile, SQL_insert_item)

    print('done!')

# ==============================================================================
#
# Create indexes
#
# ==============================================================================

print('Generating indexes...')

# item table

SQL_create_index = '''CREATE INDEX index_venue_product
                          ON item(venue_id, product_id) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

SQL_create_index = '''CREATE INDEX index_available_date
                          ON item(available_date DESC NULLS LAST) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

SQL_create_index = '''CREATE INDEX index_venue
                          ON item(venue_id) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

SQL_create_index = '''CREATE INDEX index_product
                          ON item(product_id) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

# purchase_item table

SQL_create_index = '''CREATE INDEX index_purchase
                          ON purchase_item(purchase_id) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

# purchase table

SQL_create_index = '''CREATE INDEX index_country
                          ON purchase(country) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

SQL_create_index = '''CREATE INDEX index_time_received
                          ON purchase(time_received DESC NULLS LAST) '''
print(SQL_create_index)
cur_wolt.execute(SQL_create_index)

print('All done!')

# ---- COMMIT -------
con_wolt.commit()
con_wolt.close()
print('xxxxxxxxx end xxxxxxxxxx')

