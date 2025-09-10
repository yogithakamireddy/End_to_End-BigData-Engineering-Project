# Databricks notebook source
spark

# COMMAND ----------

pip install azure-storage-file-datalake

# COMMAND ----------

# MAGIC %md
# MAGIC ## connecting databricks to data lake

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.ecommolistdatastorage.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.ecommolistdatastorage.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.ecommolistdatastorage.dfs.core.windows.net", "ea877050-90e0-4ccb-8ecf-5e0ed3882f0c")
spark.conf.set("fs.azure.account.oauth2.client.secret.ecommolistdatastorage.dfs.core.windows.net","hbW8Q~yxafNdpL1xuEygS~PVOxJ5es_89rKJKbVY")
spark.conf.set("fs.azure.account.oauth2.client.endpoint.ecommolistdatastorage.dfs.core.windows.net", "https://login.microsoftonline.com/c895e435-afc9-4357-9d8e-0b9a78b89309/oauth2/token")

# COMMAND ----------

# MAGIC %md
# MAGIC ##loading data from datalake

# COMMAND ----------

base_path = "abfss://olistdata@ecommolistdatastorage.dfs.core.windows.net/bronze/"
customers_path = base_path + "olist_customers_dataset.csv"
geolocation_path = base_path + "olist_geolocation_dataset.csv"
items_path = base_path + "olist_order_items_dataset.csv"
payments_path = base_path + "olist_order_payments_dataset.csv"
reviews_path = base_path + "olist_order_reviews_dataset.csv"
orders_path = base_path + "olist_orders_dataset.csv"
products_path = base_path + "olist_products_dataset.csv"
sellers_path = base_path + "olist_sellers_dataset.csv"

customers_df = spark.read.format("csv").option("header", "true").load(customers_path)
geolocation_df = spark.read.format("csv").option("header", "true").load(geolocation_path)
items_df = spark.read.format("csv").option("header", "true").load(order_items_path)
payments_df = spark.read.format("csv").option("header", "true").load(order_payments_path)
reviews_df = spark.read.format("csv").option("header", "true").load(order_reviews_path)
orders_df = spark.read.format("csv").option("header", "true").load(orders_path)
products_df = spark.read.format("csv").option("header", "true").load(products_path)
sellers_df = spark.read.format("csv").option("header", "true").load(sellers_path)

# COMMAND ----------

display(orders_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##reading data from pymongo

# COMMAND ----------

from pymongo import MongoClient

# COMMAND ----------

# importing module
from pymongo import MongoClient
hostname = "5-x8xl.h.filess.io"
database = "olistDataNoSQL_friendgot"
port = "61004"
username = "olistDataNoSQL_friendgot"
password = "599427d546d0c4e7a57bb4a06f113faf0214efc7"

uri = "mongodb://" + username + ":" + password + "@" + hostname + ":" + port + "/" + database

# Connect with the portnumber and host
client = MongoClient(uri)

# Access database
mydatabase = client[database]
mydatabase

# COMMAND ----------

collection = mydatabase["product_category_translation"]

# COMMAND ----------

import pandas as pd
collection = mydatabase["product_category_translation"]

mongo_data = pd.DataFrame(list(collection.find()))
mongo_data.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Cleaning the data

# COMMAND ----------

from pyspark.sql.functions import datediff,col,to_date,current_date,when

# COMMAND ----------

def clean_dataframe(df,name):
    print(f"Cleaning {name} dataframe")
    return df.dropDuplicates().na.drop('all')

orders_df = clean_dataframe(orders_df,"orders")
display(orders_df)

# COMMAND ----------

#convert Date columns

orders_df = orders_df.withColumn("order_purchase_timestamp",to_date(col("order_purchase_timestamp")))\
    .withColumn("order_approved_at",to_date(col("order_approved_at")))\
    .withColumn("order_delivered_carrier_date",to_date(col("order_delivered_carrier_date")))\
    .withColumn("order_delivered_customer_date",to_date(col("order_delivered_customer_date")))\
    .withColumn("order_estimated_delivery_date",to_date(col("order_estimated_delivery_date")))

# COMMAND ----------

display(orders_df)

# COMMAND ----------

orders_df = orders_df.withColumn("actual_delivery_time", datediff("order_delivered_customer_date","order_purchase_timestamp"))
orders_df = orders_df.withColumn("estimated_delivery_time", datediff("order_estimated_delivery_date","order_purchase_timestamp"))
orders_df = orders_df.withColumn("delay_time", col("actual_delivery_time") - col("estimated_delivery_time"))
orders_df = orders_df.withColumn("delay_time", when(col("delay_time")<0,0).otherwise(col("delay_time")))

# COMMAND ----------

display(orders_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Joining tables

# COMMAND ----------

orders_customers_df = orders_df.join(customers_df,orders_df.customer_id == customers_df.customer_id,"left")

orders_payments_df = orders_customers_df.join(payments_df, orders_customers_df.order_id == payments_df.order_id,"left")

orders_items_df = orders_payments_df.join(items_df,"order_id","left")

orders_items_products_df = orders_items_df.join(products_df, orders_items_df.product_id == products_df.product_id,"left")

order_items_products_sellers_df = orders_items_products_df.join(sellers_df, orders_items_products_df.seller_id == sellers_df.seller_id,"left")

# COMMAND ----------

display(orders_items_df)

# COMMAND ----------

display(order_items_products_sellers_df)

# COMMAND ----------

mongo_data.drop('_id', axis=1, inplace=True)

mongo_spark_df = spark.createDataFrame(mongo_data)
display(mongo_spark_df)

# COMMAND ----------

final_df = order_items_products_sellers_df.join(mongo_spark_df, order_items_products_sellers_df.product_category_name == mongo_spark_df.product_category_name,"left")

# COMMAND ----------

display(final_df)

# COMMAND ----------

def remove_duplicate_columns(df):
    columns = df.columns

    seen_columns = set()
    columns_to_drop = []

    for column in columns:
        if column in seen_columns:
            columns_to_drop.append(column)
        else:
            seen_columns.add(column)
    return df.drop(*columns_to_drop)
    
final_df = remove_duplicate_columns(final_df)
display(final_df)

# COMMAND ----------

final_df.columns

# Loading final data into silver layer

final_df.write.mode("overwrite").parquet("abfss://olistdata@ecommolistdatastorage.dfs.core.windows.net/silver")

# COMMAND ----------

