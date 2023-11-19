# Introduction to Orchestration ETL Processes With Apache Airflow

This repository contains all files from tutorial that I held at Data Science Conference Europe 2023.
Main focus of this tutorial is to get familiar with Apache Airflow concepts on first place and to demonstrate its usage for creation and orchestration of ETL processess. 

## Prerequisites

In order to run project Docker has to be installed.

To be able to run examples they should be downloaded from:
https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms

Two backups should be downloaded:
* AdventureWorks2017.bak
* AdventureWorksDW2017.bak

After download they should be put inside mssql/backups directory.

## Running

Examples/cluster can be run by simply executing script cluster_up.sh from root of project with
`./scripts/cluster_up.sh`

## Additional commands

- All bash scripts inside project should have appropriate permissions if working on Linux/Max machine
```find . -type -iname "*.sh" -exec chmod +x {} \;```
- If having issues with line endings (CLRF vs LF)
```find . -type -iname "*.sh" -exec sed -i -e 's/\r$//' {} \;```


