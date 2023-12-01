import platform
ops = platform.processor()
print(ops)
if ops == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
    print('suoritetaan PC-koneella 1')
        
    # ---------------------------------------
    # Postgres Database
    DATABASE_HOST = 'localhost'
    PORT = 5432
    DBNAME = 'wolt'
    USER = 'postgres'
    PASSWORD = 'wolt'

    # ---------------------------------------
    # Location of csv files to import
    file_purchase = r'D:/kennet/cv/wolt/data/bi_intern_assignment_data/purchase_data_final.csv'
    file_purchase_item = r'D:/kennet/cv/wolt/data/bi_intern_assignment_data/purchase_item_data_final.csv'
    file_item = r'D:/kennet/cv/wolt/data/bi_intern_assignment_data/item_data.csv'
    # ---------------------------------------
    # Location of pickle files to save SQL query results from Pandas
    file_path_for_pickle_files = r'D:/kennet/cv/wolt/pickle/'
    # ---------------------------------------
    # Location of output files of assigment tasks: HTML, CSS, SVG
    file_path_for_output = r'D:/kennet/cv/wolt/output/'
    # file_path_for_output = r'./output/'

if ops == 'Intel64 Family 6 Model 94 Stepping 3, GenuineIntel':
    print('suoritetaan koneella 2')

    # ---------------------------------------
    # Postgres Database
    DATABASE_HOST = 'localhost'
    PORT = 5433
    DBNAME = 'wolt'
    USER = 'postgres'
    PASSWORD = 'wolt'

    # ---------------------------------------
    # Location of csv files to import
    file_purchase = r'D:/kennet/cv/wolt/bi_intern_assignment_data/purchase_data_final.csv'
    file_purchase_item = r'D:/kennet/cv/wolt/bi_intern_assignment_data/purchase_item_data_final.csv'
    file_item = r'D:/kennet/cv/wolt/bi_intern_assignment_data/item_data.csv'
    # ---------------------------------------
    # Location of pickle files to save SQL query results from Pandas
    file_path_for_pickle_files = r'D:/kennet/cv/wolt/pickle/'
    # ---------------------------------------
    # Location of output files of assigment tasks: HTML, CSS, SVG
    file_path_for_output = r'D:/kennet/cv/wolt/output/'


    
