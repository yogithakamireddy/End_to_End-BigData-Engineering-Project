# End_to_End-BigData-Engineering-Project
Ecommerce Data [very good type of data for analyzing]
Pre-Requisites
1. Python and SQL
2. Azure free account($200 free credit)

Architechure of the project

<img width="1339" height="736" alt="image" src="https://github.com/user-attachments/assets/73dfeaf7-2ff5-42d7-a6f3-04132de0313b" />


Dataset from kaggle 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data?select=olist_orders_dataset.csv

Dataset from kaggle is downloaded and loaded into Github(data in HTTP)

created/Hosted one MySQL and one NoSQL(Mongo DB) databases in filess.io webserver

loading data to the MySQL Database USING python pandas code(data in SQL table)

Now load data into Azure data lake from github(http) and SQL table (http)

**Data Ingestion:**
used Azure Data Factory(ADF) with HTTP and a SQL server
Parametriozation
For each activity
Lookup
**Data Transformation:**
used Azure databricks: Spark powered, integrated with Azure, Handles big data easily, Great for Machine learning
Azure databricks workflow:
read data from ADLS
read data from NoSQL (mongoDB)






