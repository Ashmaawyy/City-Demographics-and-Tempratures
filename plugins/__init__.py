from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin
import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "sparkify_plugin"
    operators = [
        operators.StageCsvToRedshiftOperator,
        operators.StageJsonToRedshiftOperator,
        operators.LoadFactsOperator,
        operators.LoadTableOperator,
        operators.DataQualityOperator,
        operators.CreateTableOperator
    ]
    helpers = [
        helpers.SqlQueries
    ]
