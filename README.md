# Data Engineering Nanodegree Capstone Project

## Project Description

This project aims to prepare the data for analysis to inspect if there is a relation between cities demographics and their tempratures and study the relation if exists.

<br>

## Pipeline Walkthrough

- First staging tables are created and loaded from S3,
- Then data_quality_checks are performed on the data to see if there is NULL values in the cities and temperatures fields,
- Then the temperatures_demographics_fact_table is created and loaded,
- Then age_temperatures, gender_temperatures, and race_temperatures views are creaeted to analyze each variable against average_temperature field.
- The pipeline is run '@yearly' as the datasets are updated annually.

<br>

## project Build Manual

<br>

- First you need airflow setup to build this project, to install airflow copy these commands in your terminal:

<pre><code>
# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/airflow

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.4.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.4.2/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow standalone

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
</code></pre>

- Then you need to install some essential airflow providers:

<pre><code>
pip install apache-airflow[postgres]
pip install apache-airflow[amazon]
</code></pre>

- Then copy the dags and plugins folders to the airflow folder in your home directory.

- Open up a terminal and start airflow webserver and scheduler through these commands:

<pre><code>
airflow webserver
airflow scheduler
</code></pre>
Note: you need to instantiate the scheduler in a diffrent terminal window

- You should be able to see the dag in your DAGs page in the airflow UI.

- If you see dag import error: no module named plugins, this error is because airflow automatically adds plugins to your imports so you just need to remove the word plugins from the imports in the sparkify_dag.py file : )

## Data Scale Strategy

- Optimize queries for high read throughput.
- Add more cluserts in the node, and more nodes if needed.

## Data Dictionary

Temperatures dataset fields are:

- date
- average_temperature
- average_temperature_unertainty
- city
- country
- latitude
- longitude

Demographics dataset fields are:

- city
- state
- median_age
- male_population
- female_population
- total_population
- number_of_veterans
- foreign_born
- average_household_size
- state_code
- race
- count

A star schema is used to model this data as only one fact table is needed for the analysis and 3 views for 3 diifrent variables.
