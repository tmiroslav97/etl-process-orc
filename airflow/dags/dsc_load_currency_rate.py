from datetime import datetime, timedelta
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.param import Param
from airflow.models import Variable
from airflow.operators.python import get_current_context

import logging
logger = logging.getLogger(__name__)

@dag(dag_id="dsc_load_currency_rate",
    description="DAG fow loading currency rates into dw zone",
    start_date=datetime(2023,11,1),
    schedule_interval="@once",
    params={
        "currencies": Param(["USD", "EUR"], type=["null", "array"])
    })
def dsc_load_currency_rate():
    """
    ### Loading currencies from OLTP database

    This DAG will load all currency reates inside DW currency rate fact table
    
    Params:
    * currencies (array): list of currencies for which currency rate should be loaded, if it is empty then all currency rates will be loaded
    """

    @task
    def load_currency_rates():
        context = get_current_context()
        currencies = context["params"]["currencies"]
        # print([curr for curr in currencies])

        mssql_hook=MsSqlHook(mssql_conn_id='SQL_SERVER_CONNECTION')
        if not currencies:
            rows_df = mssql_hook.get_pandas_df(
                "select CurrencyRateDate as date_rate, ToCurrencyCode as currency_code, AverageRate avg_rate, EndOfDayRate end_of_day_rate from sales.currencyrate"
            );
        else:
            rows_df = mssql_hook.get_pandas_df(
                "select CurrencyRateDate as date_rate, ToCurrencyCode as currency_code, AverageRate avg_rate, EndOfDayRate end_of_day_rate from sales.currencyrate " +
                "where ToCurrencyCode in ({})".format(', '.join(["'{}'".format(value) for value in currencies]))
            );

        postgres_hook= PostgresHook(postgres_conn_id='POSTGRES_DW_CONNECTION')
        fk_df  = postgres_hook.get_pandas_df(
            "select id, currency_code from dw_schema.dim_currency " +
            "where currency_code in ({})".format(', '.join(["'{}'".format(value) for value in rows_df['currency_code'].unique()]))
        );

        if fk_df.empty:
            raise Exception("No records found; make sure to perform initial load into currency dimension table")
        else:
            logger.info(fk_df)
        
        rows_df['currency_id']=rows_df['currency_code'].apply(lambda x: fk_df[fk_df['currency_code']==x]['id'].values[0])
        #print(rows_df)
        rows_df = rows_df.drop(columns=['currency_code'])
        chunk_size = int(Variable.get("SQL_CHUNK_SIZE", default_var=10))
        rows_df.to_sql("fact_currency_rate", postgres_hook.get_sqlalchemy_engine(), schema='dw_schema', if_exists='append', index=False, chunksize=chunk_size)
        

    load_currency_rates()

dsc_load_currency_rate()