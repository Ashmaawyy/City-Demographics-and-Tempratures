import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from plugins.operators.stage_to_redshift import StageToRedshiftOperator
from plugins.operators.data_quality_checks import DataQualityOperator
from plugins.operators.creat_tables import CreateTableOperator
from plugins.helpers.sql_queries import SqlQueries

default_args = {
  'owner': 'ashmawy',
  'start_date': datetime(2019, 1, 12),
  'retries': 3,
  'retry_delay': timedelta(minutes = 5),
  'depends_on_past': False,
  'email_on_retry': False,
  'email_on_failure': False,
  'catchup': False
}

dag = \
  DAG(
    'temperatures_and_demographics_dag',
    default_args = default_args,
    description = '''
      Stage data from an S3 bucket to a redshift cluster,
      and then moves the data from the staged tables to the database tables,
      and then feeds the data to a linear regression model
      to analyze the relation between the two variables
      ''',
    schedule_interval = '@yearly'
  )

start_operator = DummyOperator(task_id = 'Begin_execution',  dag = dag)

create_staging_temperatures_table = \
  CreateTableOperator(
    task_id = 'create_staging_temperatures_table',
    dag = dag,
    redshift_conn_id = 'redshift',
    table = 'staging_events',
    create_sql = SqlQueries.staging_temperatures_create_sql
  )

create_staging_demographics_table = \
  CreateTableOperator(
    task_id = 'create_staging_demographics_table',
    dag = dag,
    redshift_conn_id = 'redshift',
    create_sql = SqlQueries.staging_demographics_create_sql
  )

aws_hook = AwsHook('aws_credentials')
aws_credentials = aws_hook.get_credentials()

stage_temperatures_to_redshift = \
  StageToRedshiftOperator(
    task_id = 'stage_temperatures',
    dag = dag,
    redshift_conn_id = 'redshift',
    aws_credentials_id = 'aws_credentials',
    region = 'us-west-2',
    table = 'staged_temperatures',
    s3_bucket = 'tempratures-and-demographics',
    s3_key = 'temperatures-data'
  )

stage_demographics_to_redshift = \
  StageToRedshiftOperator(
    task_id = 'stage_demographgics',
    dag = dag,
    redshift_conn_id = 'redshift',
    aws_credentials_id = 'aws_credentials',
    region = 'us-west-2',
    table = 'staged_demographics',
    delimiter = ';',
    s3_bucket = 'temperatures-and-demographics',
    s3_key = 'demographics-data'
  )

create_temperatures_demographics_fact_table = \
  CreateTableOperator(
    task_id = 'create_temperatures_demographics_fact_table',
    dag = dag,
    redshift_conn_id = 'redshift',
    table = 'temperatures_demographics_fact',
    create_sql = SqlQueries.temperatures_demographics_fact_table_create_sql
  )

create_race_temperatures_view = \
  CreateTableOperator(
    task_id = 'create_race_temperatures_view',
    dag = dag,
    redshift_conn_id = 'redshift',
    table = 'race_temperatures_view',
    create_sql = SqlQueries.race_temperatures_view_create_sql
  )

create_gender_temperatures_view = \
  CreateTableOperator(
    task_id = 'create_gender_temperatures_view',
    dag = dag,
    redshift_conn_id = 'redshift',
    table = 'gender_temperatures_view',
    create_sql = SqlQueries.gender_temperatures_view_create_sql
  )

create_age_temperatures_view = \
  CreateTableOperator(
    task_id = 'create_age_temperatures_view',
    dag = dag,
    redshift_conn_id = 'redshift',
    table = 'age_temperatures_view',
    create_sql = SqlQueries.age_temperatures_view_create_sql
  )

run_data_quality_checks = \
  DataQualityOperator(
    task_id = 'run_data_quality_checks',
    dag = dag,
    redshift_conn_id = 'redshift',
    test_count_query = SqlQueries.data_quality_sql
  )

end_operator = DummyOperator(task_id = 'stop_execution',  dag = dag)

# First Stage
start_operator >> create_staging_temperatures_table
start_operator >> create_staging_demographics_table

# Second Stage
create_staging_temperatures_table >> stage_temperatures_to_redshift
create_staging_demographics_table >> stage_demographics_to_redshift

# Third Stage
stage_temperatures_to_redshift >> run_data_quality_checks
stage_demographics_to_redshift >> run_data_quality_checks

# Fourth Stage
run_data_quality_checks >> create_temperatures_demographics_fact_table

# Fifth Stage
create_temperatures_demographics_fact_table >> create_age_temperatures_view
create_temperatures_demographics_fact_table >> create_gender_temperatures_view
create_temperatures_demographics_fact_table >> create_race_temperatures_view

# Sixth (and last) stage
create_age_temperatures_view >> end_operator
create_gender_temperatures_view >> end_operator
create_race_temperatures_view >> end_operator
