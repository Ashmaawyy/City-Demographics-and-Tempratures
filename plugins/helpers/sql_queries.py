class SqlQueries:
    staging_temperatues_create_sql = ('''
        CREATE TABLE public.staged_temperatures (
        date DATE
        average_temprature NUMERIC(18,0)
        average_temprature_unertainty NUMERIC(18,0)
        city VARCHAR(256)
        country VARCHAR(256)
        latitude VARCHAR(256)
        longitude VARCHAR(256)
        );
    ''')

    staging_demographics_create_sql = ('''
        CREATE TABLE public.staged_demographics (
        city VARCHAR(256)
        state VARCHAR(256)
        median_age NUMERIC(18,0)
        male_population INT4
        female_population INT4
        total_population INT4
        number_of_veterans INT4
        foreign-born INT4
        average_household_size NUMERIC(18,0)
        state_code VARCHAR(2)
        race VARCHAR(256)
        count INT4
        );
    ''')

    songplays_table_create_sql = ('''
    
    ''')

    users_table_create_sql = ('''
    
    ''')

    songs_table_create_sql = ('''
    
    ''')

    artists_table_create_sql = ('''
    
    ''')

    time_table_create_sql = ('''

    ''')
   
    userId_data_quality_check = ("""
    
    """)
