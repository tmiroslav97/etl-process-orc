#!/bin/bash

echo "> Creating docker network 'airflow_network'"
docker network create airflow_network

echo ">> Starting up MSSQL Server"
docker compose -f ./mssql/docker-compose.yml up -d
sleep 5

echo "> Starting up Airflow"
docker compose -f ./airflow/docker-compose.yml up -d
sleep 5

echo "> Starting up Postgres 'dw_database'"
docker compose -f ./postgres/docker-compose.yml up -d

echo "> Services started, going to sleep for 25 seconds"
sleep 25

echo "> Configuring individual services"

echo ">> Setting up mssql for backups"
cmd='bash -c "/config/setup.sh"'
docker exec -it sqlserver $cmd

echo ">> Setting up Airflow objects"
cmd='bash -c "/opt/airflow/config/setupAirflowObjects.sh"'
docker exec -it airflow-airflow-webserver-1 $cmd

echo ">> Settup up Postgres 'dw_database'"
cmd='bash -c /config/setup.sh'
docker exec -it postgresdb $cmd

echo "> Cluster ready for use"