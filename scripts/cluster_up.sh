#!/bin/bash

echo "> Creating docker network 'airflow_network'"
docker network create airflow_network

echo ">> Startup up MSSQL Server"
docker compose -f ./mssql/docker-compose.yml up -d
sleep 5


echo "> Configuring individual services"

echo ">> Setting up mssql for backups"
cmd='bash -c "/config/setup.sh"'
docker exec -it sqlserver $cmd

echo "> Cluster ready for use"