class SqlQueries:
    staging_temperatues_create_sql = ('''
        CREATE TABLE public.staged_temperatures (
        date DATE,
        average_temperature NUMERIC(18,0) NOT NULL,
        average_temperature_unertainty NUMERIC(18,0),
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
        foreign_born INT4,
        average_household_size NUMERIC(18,0),
        state_code VARCHAR(2),
        race VARCHAR(256),
        count INT4
        );
    ''')

    temperatures_demographics_fact_table_create_sql = ('''
    CREATE TABLE IF NOT EXISTS public.temperatures_demographics_fact_table (
        date VARCHAR(256),
        city VARCHAR(256),
        state VARCHAR(256),
        state_code VARCHAR(2),
        latitude VARCHAR(256),
        longitude VARCHAR(256),
        average_temperature NUMERIC(18,0),
        median_age NUMERIC(18,0),
        total_population INT4,
        male_population INT4,
        female_population INT4,
        race INT4,
        count INT4,
        foreign_born INT4
        );
    ''')

    temperatures_demographics_fact_table_load_sql = ('''
    SELECT DISTINCT
        date,
        staged_demographics.city,
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
        foreign_born

    FROM public.staged_temperatures LEFT JOIN public.staged_demographics
    ON staged_temperatures.city = staged_demographics.city

    WHERE staged_temperatures.country = 'United States'
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
    CREATE OR REPLACE VIEW public.gender_temperatures_view
    AS SELECT
        male_population,
        female_population,
        city,
        state_code,
        average_temperature
    
    FROM public.temperatures_demographics_fact_table;
    ''')

    age_temperatures_view_create_sql = ('''
    CREATE OR REPLACE VIEW public.age_temperatures_view
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
    
    WHERE average_temperature OR staegd_demographics.city IS NULL;
    ''')
