#!/bin/bash

echo "> Shutting down cluster"

read -p "> Delete volumes? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ">> Shutting down MSSQL cluster"
    docker compose -f ./mssql/docker-compose.yml down -v
    echo ">> Shutting down Airflow"
    docker compose -f ./airflow/docker-compose.yml down -v
else
    echo ">> Shutting down MSSQL cluster"
    docker compose -f ./mssql/docker-compose.yml down
    echo ">> Shutting down Airflow"
    docker compose -f ./airflow/docker-compose.yml down
fi

echo "> Deleting 'airflow_network' network"
docker network rm airflow_network

echo "> Cluster down"