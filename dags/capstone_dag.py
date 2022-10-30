import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
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

dag = DAG('demographic_temperature_relation_dag',
          default_args = default_args,
          description = '''
            Stage data from an S3 bucket to a redshift cluster,
            and then moves the data from the staged tables to the database tables,
            and then feeds the data to a linear regression model to analyze the relation between the two variables
            ''',
          schedule_interval = '@yearly'
        )