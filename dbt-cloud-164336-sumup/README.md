Welcome to the DBT project!

# SumUp Analytics

## Getting Started

* First I have created the raw models where I have done the data quality checks to ensure the correctness of the data. All theses tests have been added in schema.yml file under source folder. Materalized these raw models as views. 
* A **view** doesn’t store any data, like a table does, but it defines the logic that needs to be fetched from the underlying data.
* Creat dimensional models from the respective raw models. The dimensional models creeated are **dim_devices, dim_stores and dim_transactions**.
* I created dimensional table **dim_devices**, assuming that we should have one in our system. Taking the **distinct device_type** from raw_devices and added couple of related dimensions like id(unique identifier of the device_type),device_type_name(These names were picked from the SumUp website.), and launch_date (when a specific device type was first introduced in our system) and etc.. This table is not adding any value to our current analysis.
* **dim_stores**: Created it directly from **raw_stores**, incrementalised the model so that the model will append the newly created stores to the table.
* **Incrementals** are built as table, the first time a model is run, the table is built by transforming all rows of source data. On subsequent runs, dbt transforms only the rows in your source data that you tell dbt to filter in the incremental logic.
* **dim_transactions** Created this model from raw_devices and dim_stores, this is the final model to answer all the questions in the case study. I have materialized is as incremental. I have used pre_hook which drops the previous 6 hours data and reinserts it in the current run.
* **fact_transactions**: This is the additional table I have created, again nothing to do with this case study. To provide the complete dimensional modeling overview I created this table by adding few measures. 
* **freshness**: Adding model freshness to each raw models keeps us aware of free flow of data in the data models. Alert with the warning if a specific model is not updated with the new data in the past hours/days(as mentioned in the freshness check). This needs to be determined by the business use case.
* **Tags**: I have added different tags to these models. These tags come in handy while creating the schedules for these models.
* Add **meta owner**: adding meta owner for every model helps determining the person responsible or person owning the specific model.
* Add **group**: adding group helps the developer community know to which business group the specific model begins to, Can also add lebels to the models.


### Sample commands used in building this project

```
Try running the following commands:
<!-- Builds the entire project, run models, test tests snapshot snapshots and seed seeds. -->
- dbt build 
<!-- Test all the tests defined for the tag source. -->
- dbt test --select tag:source 
<!-- This command will build upstream and the downstream models -->
- dbt build --select +dim_transactions+
<!-- Buiilds all the models which are tagged with payments tag. -->
- dbt build --select tag:payments
```



### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
