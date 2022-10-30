from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from psycopg2 import Error

class LoadTableOperator(BaseOperator):
    ui_color = '#80BD9E'

    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id = '',
                 table = '',
                 load_sql = '',
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.load_sql = load_sql

    def execute(self):
        redshift = PostgresHook(self.redshift_conn_id)
        
        try:
            self.log.info('Loading {} table...'.format(self.table))
            redshift.run(self.load_sql)
            self.log.info('Loaded {} table successfully :)'.format(self.table))

        except Error as e:
            self.log.error(e)
