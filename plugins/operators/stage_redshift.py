from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from psycopg2 import Error

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    def __init__(self,
                 # Operators params (with defaults) here
                 redshift_conn_id = '',
                 table = '',
                 copy_sql = '',
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.copy_sql = copy_sql

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)

        self.log. \
            info('Copying data from S3 bucket {} to Redshift table {}'. \
            format(self.s3_bucket, self.table))
        try:
            redshift.run(self.copy_sql)
            self.log.info('Data copied to {} susseccfully :)'.format(self.table))

        except Error as e:
            self.log.error(e)
