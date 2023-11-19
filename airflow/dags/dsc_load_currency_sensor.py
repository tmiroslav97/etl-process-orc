from datetime import datetime, timedelta
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

import logging
logger = logging.getLogger(__name__)

def _success_criteria(record):
    return record

#def _failure_criteria(record):
#    return True if not record else False

@dag(dag_id="dsc_load_currency_sensor",
    description="DAG fow loading currencies into dw zone with sql sensor",
    start_date=datetime(2023,11,1),
    schedule_interval="@once")
def dsc_load_currency_sensor():
    """
    ### Loading currencies from OLTP database

    This DAG will load all currencies inside DW currency dimension table
    """

    @task
    def get_currencies_count() -> int:
        """
            #### Get currency count
    
            Task will count entries in currency dw_schema
        """
        postgres_hook = PostgresHook(postgres_conn_id='POSTGRES_DW_CONNECTION')

        logger.info("Fetching count from dw_schema.dim_currency")
        record = postgres_hook.get_first("select count(*) from dw_schema.dim_currency")
        num_of_records = record[0]
        if num_of_records>0:
            logger.info(f'Number of records is {num_of_records}')
        else:
            raise Exception("No records found; make sure to perform initial load into dimension table")
        return num_of_records
    
    doc_md_sql_sensor = """
        #### Wait for new records task

        Sensor task is used to check if new rows inserted in currency table in OLTP database
    """

    wait_for_new_currency_records= SqlSensor(
        task_id="wait_for_new_currency_records",
        conn_id="SQL_SERVER_CONNECTION",
        sql="sql/check_currency_table_updates.sql",
        success=_success_criteria,
        #failure=_failure_criteria,
        fail_on_empty=True,
        poke_interval=30,
        mode="reschedule",
        doc_md=doc_md_sql_sensor
    )

    @task
    def load_new_rows_into_dim_table():
        postgres_hook = PostgresHook(postgres_conn_id='POSTGRES_DW_CONNECTION')

        logger.info("Fetching rows from currency dim table")
        currency_codes = postgres_hook.get_pandas_df("select currency_code from dw_schema.dim_currency")

        mssql_hook=MsSqlHook(mssql_conn_id='SQL_SERVER_CONNECTION')
        rows_df = mssql_hook.get_pandas_df(
            "select CurrencyCode as currency_code, name as currency_name from sales.currency " +
            "where CurrencyCode not in ({})".format(', '.join(["'{}'".format(value) for value in currency_codes['currency_code']]))
        );

        postgres_hook= PostgresHook(postgres_conn_id='POSTGRES_DW_CONNECTION')
        rows_df.to_sql("dim_currency", postgres_hook.get_sqlalchemy_engine(), schema='dw_schema', if_exists='append', index=False)

    doc_md_delete_xcoms = """
        #### Delete XComs Task
        
        Task used to clean up XComs after Dag run
    """

    delete_xcoms = PostgresOperator(
        task_id="delete-xcom-task",
        postgres_conn_id="AIRFLOW_DB_CONNECTION",
        sql="delete from xcom where dag_id='dsc_load_currency_sensor'",
        doc_md=doc_md_delete_xcoms
    )

    doc_md_trigger_next_run = """
        #### Trigger next run

        Task used to trigger next run
    """
    trigger_next_run = TriggerDagRunOperator(
        task_id="trigger_next_run",
        trigger_dag_id='dsc_load_currency_sensor',
        doc_md=doc_md_trigger_next_run
    )

    get_currencies_count() >> wait_for_new_currency_records >> load_new_rows_into_dim_table() >> delete_xcoms >> trigger_next_run

dsc_load_currency_sensor()