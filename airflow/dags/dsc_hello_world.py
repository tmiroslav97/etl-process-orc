from datetime import datetime, timedelta
from airflow.decorators import task, dag

import logging
logger = logging.getLogger(__name__)


@dag(dag_id="dsc_hello_world",
    description="DAG with hello world example",
    start_date=datetime(2023,11,1),
    schedule_interval="@monthly",
    max_active_runs=1)
def dsc_hello_world():
    """
    ### Hello world from DSC

    This DAG can be used for practice and here you can write docs about DAG.
    """

    @task
    def hello_world():
        """
        #### Hello world task

        Task docs are written here
        """

        print("Hello world!")
    
    @task
    def from_dsc():
        """
        #### From DSC task

        This task will print complete message
        """
        print("Hello world from DSC Europe 2023!")

    [hello_world(), from_dsc()]

dsc_hello_world()