# Case Study

Create End-to-End ELT Pipeline from Data Source to Data Warehouse using Python, SQL, and DBT.

## Description

I had been provided with three csv files, the goal of this project is to create an end to end ELT pipeline from a data source to data warehouse using Python, SQL and DBT and data models to answer the following questions. 
* Top 10 stores per transacted amount
* Top 10 products sold
* Average transacted amount per store typology and country
* Percentage of transactions per device type
* Average time for a store to perform its 5 first transactions

### Deliverables: 
Please share the source code, data model design, SQLs to answer the above questions via public git repository including a readme file explaining your assumptions, design and solution implementation details.

## Getting Started

### Data Sources
The project uses three CSV files as the data sources:
* **Stores.csv**: Contains information about the stores, such as the store ID, name, location and Typology.
* **Devices.csv**: Contains information about the devices used for transactions, such as the device ID, device type, and store id the device is associated with.
* **Transactions.csv**: Contains information about the sales transactions, such as the transaction ID, date teh transaction happened at, device ID, product name, product category, transaction amount, and card details of the card being used in the transaction.

## Assumptions

* Assuing happened_at timestamp is the time when the transaction happened.
* There are two entries with this card number **4.91783E+15** assuming it as the invalid ingestion. To overcome such issues add accepted_values test on the **card_number** column

### Project Breakdown : 
I have devided the project into multiple steps. I am using **Google Cloud Platform Service**(GCP) to handle this project, **BigQuery**(BQ) is the data warehouse in this project.

1. Load the data from my local system to Google Cloud Storage(GCS) using Python.
  * Here i have written python script to load data from my laptop to the GCS bucket(Bucket is defined in congig.ini file) , the source of the data can be changed to anything in the config/config.ini file. **upload_csv_gcs.py** is the python file with hardcoaded source and destination bucket. **config_read_upload_csv_gcs.py** contains the same script but it will read the credentials and paths from config.ini file.
  * First I have created three folders called as device_info, stores_info and transactions to store device.csv, store.csv and transactions.csv under respective folders. 
  * In development environment we might be consuming this source data from any message queue like **Kafka**, **SQS** or extracting from some **third party API's**. Let's say we are extracting the transaction data every 2 hours from kafka queue. I will create subfolders under these main(device_info, stores_info and transactions) folders for respective date and within these subfolders I will again create folders called hourly_folders for every extraction(2 hours) i.e. i will be having 12 folders within every date folder and store my csv's or json files under this hourly folders.
  Screenshots attached for reference.
  
  ![Screenshot 2023-04-25 at 01 37 07](https://user-images.githubusercontent.com/36684754/234170747-8a55c6b7-e9df-4842-9ef5-3aced0dab51d.png)
  
2. Automating the pipeline using Airflow.
  * I am using airflow to orchestrate the above script. I have created created four tasks within the **DAG** one to create folders in the bucket, and rest three tasks to upload the csv's into the respective folders. First the folders are created and then the remaining three tasks run in parallel to upload the csv's. 
  * These tasks can be scheduled at different time intervals depending on the business requirements.
  
  The below screenshot shows the **success** of the DAG run.
  
  ![WhatsApp Image 2023-04-23 at 4 43 11 PM](https://user-images.githubusercontent.com/36684754/234170884-f9c11a80-5562-48aa-b155-0427c4e9544b.jpeg)
  
3. Create tables in BigQuery using the files in GCS.
  * I have done it directly on BQ colsole.
4. Connect BigQuery to Data Build Tool(DBT).
  * I used the trial version of DBT cloud and created the project from scratch.
5. Create the raw models(raw_transactions, raw_devices, raw_stores) where column type casting, deduplication and data quality testing is done.
  * I am using Kimball's approach of dimensional modelling in creating this data warehouse.
  * Dimensional modeling is one of many data modeling techniques used to organize and present data for analytics.
  * The goal of dimensional modeling is to take raw data and transform it into Fact and Dimension tables that represent the business.
  * Why am i using this approach? Couple of main benefits are ** Simpler data model for analytics, Dimensions can be easily reused and Faster data retrieval**
  
  <img width="833" alt="Screenshot 2023-04-25 at 12 57 36" src="https://user-images.githubusercontent.com/36684754/234257159-a588f14e-21a5-4afa-ac9d-bba2c8e7756a.png">
  
  ![Screenshot 2023-04-25 at 02 20 13](https://user-images.githubusercontent.com/36684754/234171024-d9e39c3d-780d-4615-8dc5-ee2d2b1b4a36.png)
  
  * I have added **source freshness checks** and all the necessary tests in the **schema.yml** file under sources folder.
  The below screenshot show the test results.
   
   ![WhatsApp Image 2023-04-25 at 2 28 14 AM](https://user-images.githubusercontent.com/36684754/234171234-7782815b-7019-4243-a752-cd22a0eca832.jpeg)
  
6. Create the respective dimensional and the fact models to answer the business questions.
  * To answer all the five questions defined in the case study I have created the **dim_transaction** table by joining **raw_transactions** with **raw_devices** and **dim_stores** I have presented the results of these questions in two wasy.
    * **SQL queries** queried on a dim_transaction table. I have pasted these queries in pdf and attached the same for your reference.
    * I have used **Looker Studio** and created the Looks. I have attached the pdf of the same for reference.
    
  ![WhatsApp Image 2023-04-25 at 2 12 26 AM](https://user-images.githubusercontent.com/36684754/234171416-f3ed9d4b-1ce9-48e4-a5de-c88e3cf2bf4c.jpeg)


## Project Setup
The following are the steps to set up and run the project:
1. Clone the repository: Clone the repository to your local machine using the following command: 
```
git clone https://github.com/sidgk/sumup.git
```
2. Set up a Google Cloud Storage bucket and upload the sample data files (stores.csv, devices.csv, transactions.csv) to a subdirectory.
3. Configure the **config.ini** file in the config directory with your source paths, GCS bucket name and project ID.
4. Install dependencies: Install the required dependencies using the following command: 

  ```
  pip install -r requirements.txt
  ```
  
  * Please note that you need to have pip installed in your system to install these packages. Also, make sure to run this command in a virtual environment to avoid any conflicts with other packages that you may have installed on your system.
5. Create the tables in BigQuery.
6. Configure Airflow: Configure Airflow by setting up the connections and variables.
7. Start the Airflow web server and scheduler:
  ``` 
  airflow webserver --port 8080
  airflow scheduler
 ```
8. Run the DAG: Run the Airflow DAG to start the ELT pipeline. Open the **http://localhost:8080/** in the web browser to check the DAG runs on Airflow UI.
9. All the DBT models and model run steps are defined in **dbt-cloud-164336-sumup** folder. 

## Conclusion
This project demonstrates an end-to-end ELT pipeline for online-payment-tribe data using Python, SQL, and DBT. The pipeline extracts data from CSV files, loads it into Google Cloud Storage, and transforms it into a data model in BigQuery using DBT. The pipeline is then used to answer several business questions related to sales data, and the results can be visualized in a BI dashboard.

## Authors

Siddu G Kattimani

@siddugkattimani@gmail.com

