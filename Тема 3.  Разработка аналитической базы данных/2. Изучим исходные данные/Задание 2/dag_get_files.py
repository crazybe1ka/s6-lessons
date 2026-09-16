import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import dag
from airflow.models import Variable

import boto3

aws_access_key_id = Variable.get('aws_access_key_id')
aws_secret_access_key = Variable.get('aws_secret_access_key')


def fetch_s3_file(bucket: str, key: str):
    # сюда поместить код из скрипта для скачивания файла
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    s3_client.download_file(
        Bucket=bucket,
        Key=key,
        Filename=f'/data/{key}'
    )

# эту команду надо будет поправить, чтобы она выводила
# первые десять строк каждого файла
bash_command_tmpl = """
{% for file in params.files %}
echo "===== {{ file }} ====="
head -n 10 "{{ file }}"
{% endfor %}
"""


@dag(schedule_interval=None, start_date=pendulum.parse('2022-07-13'))
def sprint6_dag_get_data():
    bucket_files = [
        'groups.csv',
        'users.csv',
        'dialogs.csv'
        ]
    load_fetch_groups_csv = PythonOperator(
        task_id='load_fetch_groups_csv',
        python_callable=fetch_s3_file,
        op_kwargs={'bucket': 'sprint6', 'key': 'groups.csv'},
    )
    load_fetch_users_csv = PythonOperator(
            task_id='load_fetch_users_csv',
            python_callable=fetch_s3_file,
            op_kwargs={'bucket': 'sprint6', 'key': 'users.csv'},
        )
    load_fetch_dialogs_csv = PythonOperator(
            task_id='load_fetch_dialogs_csv',
            python_callable=fetch_s3_file,
            op_kwargs={'bucket': 'sprint6', 'key': 'dialogs.csv'},
        )
    print_10_lines_of_each = BashOperator(
        task_id='print_10_lines_of_each',
        bash_command=bash_command_tmpl,
        params={'files': [f'/data/{f}' for f in bucket_files]}
    )

    [load_fetch_groups_csv, load_fetch_users_csv, load_fetch_dialogs_csv] >> print_10_lines_of_each


_ = sprint6_dag_get_data()