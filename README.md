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

## DataIngestion:

### Services Used
- Azure Data Factory(ADF)
- Azure Data Lake Storage (ADLS Gen2)

### Steps Followed

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

**Data Transformation:**
used Azure databricks: Spark powered, integrated with Azure, Handles big data easily, Great for Machine learning
Azure databricks workflow:
read data from ADLS
read data from NoSQL (mongoDB)


**Challenges Faced:**





