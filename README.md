# End_to_End-BigData-Engineering-Project

Pre-Requisites
1. Python and SQL
2. Azure free account($200 free credit)

**Architechure of the project**

<img width="1339" height="736" alt="image" src="https://github.com/user-attachments/assets/73dfeaf7-2ff5-42d7-a6f3-04132de0313b" />

**Dataset:**
Domain: Ecommerce Data
1. Download the data from Kaggle(Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data?select=olist_orders_dataset.csv)
2. Push the files into github repository
3. Created MySQL and MongoDB databases(Hosted them on cloud using Filess.io)
4. Established cloud connections using python connectors
5. Loaded structured data into MySQL and semi structured data into MongoDB

### 1. DataIngestion:

### 1.1 Services Used
- Azure Data Factory(ADF)
- Azure Data Lake Storage (ADLS Gen2)

### 1.2 Steps Followed

1. Configured Azure Data Lake Storage:
   - Created a **Storage Account**  
   - **Enabled Hierarchical Namespace (HNS)** during setup (required for ADLS Gen2)  
   - Created container with folders:  
     - `bronze/` → raw data  
     - `silver/` → transformed/cleaned data  
     - `gold/` → final curated data
       
2. Connected ADF with data sources:
   - HTTP connection -> GitHub(to fetch raw files)
   - MySQL connection -> MySQL cloud database (to fetch data from MySQL cloud server)
     
3. Created a Lookup activity in ADF:
   - Reads the JSON configuration file from GitHub
   - Fetches values like `relative_url` and `file_name`
   [ JSON file Link: https://github.com/yogithakamireddy/End_to_End-BigData-Engineering-Project/blob/main/ForEachInput.json ]
     
4. ForEach Activity (GitHub Data Ingestion)
   - Iterates over the JSON values from Lookup activity  
   - Copy Activity inside ForEach:  
     - Copies each file from GitHub into ADLS – Bronze folder 

5. Copy Activity (MySQL Data Ingestion)
   - After ForEach activity, copies data from MySQL cloud database
   - Loads data into ADLS – Bronze folder using parameterized values
  
  
### JSON Configuration Example
[
	{
	"csv_relative_url":"End_to_End-BigData-Engineering-Project/refs/heads/main/data/olist_customers_dataset.csv",
	"file_name":"olist_customers_dataset.csv"
	},
	{
	"csv_relative_url":"End_to_End-BigData-Engineering-Project/refs/heads/main/data/olist_geolocation_dataset.csv",
	"file_name":"olist_geolocation_dataset.csv"
	}
]

<img width="791" height="523" alt="image" src="https://github.com/user-attachments/assets/4fc143a5-1bb6-497d-bd1f-9950260ec15e" />

### 2. Data Transformation

### 2.1 Services Used
- Azure databricks: Spark powered, integrated with Azure, Handles big data easily, Great for Machine learning
- Azure Data Lake Storage (ADLS)
- MongoDB (Cloud NoSQL Database)
- 
### 2.2 Steps Followed
1. **Connected Databricks to Data Sources**
   - Established a secure connection between **Databricks and ADLS** using service principal credentials
   - Connected Databricks to **MongoDB (NoSQL)** for additional datasets

2. **Loaded Data into PySpark DataFrames**
   - Fetched raw data from **Bronze layer (ADLS)**
   - Imported NoSQL data from **MongoDB**
   - Converted both sources into PySpark DataFrames for processing

3. **Applied Data Cleaning & Transformations**
   - Removed duplicates and null values
   - Standardized schema and column names
   - Applied necessary business rules

4. **Joined Relational + NoSQL Data**
   - Performed joins between **Bronze layer data (CSV/MySQL sources)** and **MongoDB collections**
   - Built a unified schema for downstream analysis

5. **Wrote Transformed Data to Silver Layer**
   - Stored the cleaned and enriched data into **ADLS Silver container**
   - Ensured partitioning and optimized storage formats (e.g., Parquet) for performance

### 3. Data Loading / Serving

#### 3.1 Services Used
- Azure Synapse Analytics (Serverless SQL Pool)
- Azure Data Lake Storage (ADLS)

#### 3.2 Steps Followed
1. **Established Synapse–ADLS Connection**
   - Configured Synapse Analytics to connect with **ADLS Silver layer**
   - Granted necessary permissions (Storage Blob Data Contributor role via Microsoft Entra ID)

2. **Queried Data from Silver Layer**
   - Used **serverless SQL pool** in Synapse Analytics
   - Executed SQL scripts to query Parquet files from the Silver container
   - Created **views** for simplified querying

3. **Created External Tables in Gold Layer**
   - Defined external tables on top of ADLS data
   - Transformed data into curated **Gold layer**  
   - Stored in **Parquet format** (optimized for analytics)

4. **Prepared Data for Analytics**
   - Final curated Gold layer tables made available for:
     - Power BI dashboards
     - Advanced analytics queries
    
**Challenges Faced:**

#### 1. CSV Ingestion Failure (Extra Commas)
**Error:**
	ErrorCode=DelimitedTextMoreColumnsThanDefined,'Type=Microsoft.DataTransfer.Common.Shared.HybridDeliveryException,
	Message=Error found when processing 'olist_order_reviews_dataset.csv' with row number 1587: found more columns 
	than expected column count 7.
**Cause:** Extra commas inside text fields
**✅ Solution:** In ADF DelimitedText dataset, configured:
	Column delimiter → ,
	Row delimiter → \n
	Quote character → "
	Escape character → \
	(Resolved with help from ChatGPT)

#### 2. Databricks Compute Not Available in Region
Issue: Selected compute type was unavailable in chosen region
✅ Solution: Used Databricks AI Playground to identify a supported compute SKU for the subscription and region

#### 3. Synapse Access to ADLS Silver Layer
**Error:**
Content of directory on path 'https://ecommolistdatastorage.dfs.core.windows.net/olistdata/silver/' cannot be listed.
**Cause:** Insufficient permissions
**✅ Solution:**
	- Created security group in Microsoft Entra ID
	- Added self as member
	- Granted Storage Blob Data Contributor role
	(Resolved with help from Stack Overflow & ChatGPT)

### Results and key outcomes:
1. Successfully implemented end-to-end big data pipeline in Azure
2. Achieved structured data processing with Medallion Architecture
3. Enabled real-time querying through Synapse
4. Built scalable foundation for Power BI dashboards
