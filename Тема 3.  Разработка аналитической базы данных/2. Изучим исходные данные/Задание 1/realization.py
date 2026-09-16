import os
import boto3

os.makedirs('data', exist_ok=True)

aws_access_key_id = "__"
aws_secret_access_key = "__"

session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
s3_client.download_file(
    Bucket='sprint6',
    Key='groups.csv',
    Filename='data/groups.csv'
)