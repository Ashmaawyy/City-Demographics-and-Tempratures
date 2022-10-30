import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from plugins.operators.stage_redshift import StageToRedshiftOperator
from plugins.operators.load_facts import LoadFactsOperator
from plugins.operators.load_dimensions import LoadDimensionsOperator
from plugins.operators.data_quality import DataQualityOperator
from plugins.operators.creat_table import CreateTableOperator
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

dag = DAG(
  'demographic_temperature_relation_dag',
  default_args = default_args,
  description = '''
    Stage data from an S3 bucket to a redshift cluster,
    and then moves the data from the staged tables to the database tables,
    and then feeds the data to a linear regression model to analyze the relation between the two variables
    ''',
  schedule_interval = '@yearly'
  )

start_operator = DummyOperator(task_id = 'Begin_execution',  dag = dag)

create_staging_events_table = CreateTableOperator(
  task_id = 'create_staging_events_table',
  dag = dag,
  redshift_conn_id = 'redshift',
  aws_credentials_id = 'aws_credentials',
  region = 'us-west-2',
  table = 'staging_events',
  create_sql = SqlQueries.staging_temperatures_create_sql
  )

create_staging_songs_table = CreateTableOperator(
  task_id = 'create_staging_songs_table',
  dag = dag,
  redshift_conn_id = 'redshift',
  aws_credentials_id = 'aws_credentials',
  region = 'us-west-2',
  table = 'songplays',
  create_sql = SqlQueries.staging_demographics_create_sql
  )

aws_hook = AwsHook('aws_credentials')
aws_credentials = aws_hook.get_credentials()

stage_temperatures_to_redshift = StageToRedshiftOperator(
  task_id = 'stage_temperatures',
  dag = dag,
  redshift_conn_id = 'redshift',
  copy_sql = SqlQueries.staged_temperatures_copy_sql_without_aws_keys. \
    format(aws_credentials.access_key, aws_credentials.secret_key)
  )

stage_demographics_to_redshift = StageToRedshiftOperator(
  task_id = 'stage_demographics',
  dag = dag,
  redshift_conn_id = 'redshift',
  copy_sql = SqlQueries.staged_demographics_copy_sql_without_aws_keys. \
    format(aws_credentials.access_key, aws_credentials.secret_key)
  )

end_operator = DummyOperator(task_id = 'stop_execution',  dag = dag)
