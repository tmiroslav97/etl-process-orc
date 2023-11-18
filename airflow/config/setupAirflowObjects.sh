#!/bin/bash

# Set up connections
echo ">>> Setting up Airflow connections"
airflow connections add 'SQL_SERVER_CONNECTION' \
    --conn-json '{
        "conn_type": "mssql",
        "login": "sa",
        "password": "dscPass23!",
        "host": "mssqldb",
        "port": 1433,
        "schema": "AdventureWorks2017"
    }'

airflow connections add 'AIRFLOW_DB_CONNECTION' \
    --conn-json '{
        "conn_type": "postgres",
        "login": "airflow",
        "password": "airflow",
        "host": "postgres",
        "port": 5432,
        "schema": "airflow"
    }'