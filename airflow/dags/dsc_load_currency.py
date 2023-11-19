from datetime import datetime, timedelta
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

import logging
logger = logging.getLogger(__name__)

@dag(dag_id="dsc_load_currency",
    description="DAG fow loading currencies into dw zone",
    start_date=datetime(2023,11,1),
    schedule_interval="@once")
def dsc_load_currency():
    """
    ### Loading currencies from OLTP database

    This DAG will load all currencies inside DW currency dimension table
    """

    @task
    def load_currencies():
        mssql_hook=MsSqlHook(mssql_conn_id='SQL_SERVER_CONNECTION')
        rows_df = mssql_hook.get_pandas_df(
            "select CurrencyCode as currency_code, name as currency_name  from sales.currency"
        );
        logger.info(f'Number of rows: {len(rows_df)}')
        print(rows_df.columns)
        postgres_hook= PostgresHook(postgres_conn_id='POSTGRES_DW_CONNECTION')
        rows_df.to_sql("dim_currency", postgres_hook.get_sqlalchemy_engine(), schema='dw_schema', if_exists='append', index=False)

    load_currencies()

dsc_load_currency()