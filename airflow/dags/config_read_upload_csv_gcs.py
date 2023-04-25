import os
from google.cloud import storage
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

print(config['GoogleCloud']['bucket_name'])
print(config['GoogleCloud']['transaction_path'])
print(config['GoogleCloud']['devices_path'])
print(config['GoogleCloud']['stores_path'])
print(config['Credentials']['project_id'])
print(config['Credentials']['keyfile_path'])

# Set the paths to the CSV files
transaction_path = config['GoogleCloud']['transaction_path']
devices_path = config['GoogleCloud']['devices_path']
stores_path = config['GoogleCloud']['stores_path']

# Set the name of the destination bucket in Google Cloud Storage
bucket_name = config['GoogleCloud']['bucket_name']

# Set up the Google Cloud Storage client
client = storage.Client()

# Set the destination bucket
bucket = client.get_bucket(bucket_name)

# Create three folders in the bucket
def create_folders():
    device_folder = bucket.blob("device_info/")
    device_folder.upload_from_string("")

    store_folder = bucket.blob("stores_info/")
    store_folder.upload_from_string("")

    transaction_folder = bucket.blob("transactions/")
    transaction_folder.upload_from_string("")

# Upload the transaction file to the transactions folder
def upload_transaction():
    transaction_blob = bucket.blob("transactions/" + os.path.basename(transaction_path))
    transaction_blob.upload_from_filename(transaction_path)

# Upload the devices file to the device_info folder
def upload_devices():
    devices_blob = bucket.blob("device_info/" + os.path.basename(devices_path))
    devices_blob.upload_from_filename(devices_path)

# Upload the stores file to the stores_info folder
def upload_stores():
    stores_blob = bucket.blob("stores_info/" + os.path.basename(stores_path))
    stores_blob.upload_from_filename(stores_path)

# Define the DAG
dag = DAG(
    'csv_upload_gcs',
    description='Upload CSVs to Google Cloud Storage',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False
)

# Define the tasks
create_folders_task = PythonOperator(
    task_id='create_folders',
    python_callable=create_folders,
    dag=dag,
)

upload_transaction_task = PythonOperator(
    task_id='upload_transaction',
    python_callable=upload_transaction,
    dag=dag,
)

upload_devices_task = PythonOperator(
    task_id='upload_devices',
    python_callable=upload_devices,
    dag=dag,
)

upload_stores_task = PythonOperator(
    task_id='upload_stores',
    python_callable=upload_stores,
    dag=dag,
)

# Define the task dependencies
create_folders_task >> [upload_transaction_task, upload_devices_task, upload_stores_task]
