class SqlQueries:
    staging_temperatues_create_sql = ('''
        CREATE TABLE public.staged_temperatures (
        date DATE,
        average_temprature NUMERIC(18,0) NOT NULL,
        average_temprature_unertainty NUMERIC(18,0),
        city VARCHAR(256) NOT NULL,
        country VARCHAR(256),
        latitude VARCHAR(256),
        longitude VARCHAR(256)
        );
    ''')

    staging_demographics_create_sql = ('''
        CREATE TABLE public.staged_demographics (
        city VARCHAR(256),
        state VARCHAR(256),
        median_age NUMERIC(18,0),
        male_population INT4,
        female_population INT4,
        total_population INT4,
        number_of_veterans INT4,
        foreign-born INT4,
        average_household_size NUMERIC(18,0),
        state_code VARCHAR(2),
        race VARCHAR(256),
        count INT4
        );
    ''')

    temperatures_demographics_fact_table_create_sql = ('''
    CREATE TABLE IF NOT EXISTS public.temperatures_demographics_fact_table
    AS SELECT
        date,
        city,
        state,
        state_code,
        latitude,
        longitude,
        average_temperature,
        median_age,
        total_population,
        male_population,
        female_population,
        race,
        count,
        foreign-born

    FROM public.staged_temperatures LEFT JOIN public.staged_demographics
    ON staged_temperatures.city = staged_demographics.city

    WHERE staged_temperatures.country = 'United States'
    WITH NO SCHEMA BINDING;
    ''')

    race_temperatures_view_create_sql = ('''
    CREATE OR REPLACE VIEW public.race_temperatures_view
    AS SELECT
        race,
        count,
        city,
        state_code,
        average_temperature
    
    FROM public.temperatures_demographics_fact_table;
    ''')

    gender_temperatures_view_create_sql = ('''
    CREATE OR REPLACE VIEW public.race_temperatures_view
    AS SELECT
        male_population,
        female_population,
        city,
        state_code,
        average_temperature
    
    FROM public.temperatures_demographics_fact_table;
    ''')

    age_temperatures_view_create_sql = ('''
    CREATE OR REPLACE VIEW public.race_temperatures_view
    AS SELECT
        median_age,
        city,
        state_code,
        average_temperature
    
    FROM public.temperatures_demographics_fact_table;
    ''')

    data_quality_sql = ('''
    SELECT COUNT (*)

    FROM public.staged_temperatures LEFT JOIN public.staged_demographics
    ON staged_temperatures.city = staged_demographics.city
    
    WHERE average_temperature OR city IS NULL;
    ''')
