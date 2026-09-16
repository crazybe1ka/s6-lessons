import pendulum
import vertica_python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import dag
from airflow.models import Variable
from airflow.hooks.base import BaseHook

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


def load_csv_to_vertica(file_path: str, table_name: str):
    connection = BaseHook.get_connection('WAREHOUSE_CONNECTION')

    conn_info = {
        'host': connection.host,
        'port': connection.port,
        'user': connection.login,
        'password': connection.password,
        'database': connection.schema,
    }

    chunk_size = 10000

    with vertica_python.connect(**conn_info) as conn:
        cursor = conn.cursor()

        if table_name == 'users':
            cursor.execute("""
                TRUNCATE TABLE VT260905539720__STAGING.dialogs;
                TRUNCATE TABLE VT260905539720__STAGING.groups;
                TRUNCATE TABLE VT260905539720__STAGING.users;
            """)
        else:
            cursor.execute(f"""
                TRUNCATE TABLE VT260905539720__STAGING.{table_name};
            """)

        cursor.execute(f"""
            DROP TABLE IF EXISTS VT260905539720__STAGING.{table_name}_rej;
        """)

        with open(file_path, 'r', encoding='utf-8') as file:
            next(file)  # пропускаем заголовок

            while True:
                chunk = []

                for _ in range(chunk_size):
                    line = file.readline()

                    if not line:
                        break

                    chunk.append(line)

                if not chunk:
                    break

                cursor.copy(
                    f"""
                    COPY VT260905539720__STAGING.{table_name}
                    FROM STDIN
                    DELIMITER ','
                    ENCLOSED BY '"'
                    NO ESCAPE
                    REJECTED DATA AS TABLE VT260905539720__STAGING.{table_name}_rej
                    REJECTMAX 100
                    """,
                    ''.join(chunk)
                )

        conn.commit()


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
    load_users_to_vertica = PythonOperator(
        task_id='load_users_to_vertica',
        python_callable=load_csv_to_vertica,
        op_kwargs={
            'file_path': '/data/users.csv',
            'table_name': 'users'
        },
    )
    load_groups_to_vertica = PythonOperator(
        task_id='load_groups_to_vertica',
        python_callable=load_csv_to_vertica,
        op_kwargs={
            'file_path': '/data/groups.csv',
            'table_name': 'groups'
        },
    )
    load_dialogs_to_vertica = PythonOperator(
        task_id='load_dialogs_to_vertica',
        python_callable=load_csv_to_vertica,
        op_kwargs={
            'file_path': '/data/dialogs.csv',
            'table_name': 'dialogs'
        },
    )

    [load_fetch_groups_csv, load_fetch_users_csv, load_fetch_dialogs_csv] \
        >> print_10_lines_of_each \
        >> load_users_to_vertica \
        >> load_groups_to_vertica \
        >> load_dialogs_to_vertica


_ = sprint6_dag_get_data()