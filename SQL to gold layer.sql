create view gold.final2
AS
SELECT
    *
FROM
    OPENROWSET(
        BULK 'https://ecommolistdatastorage.dfs.core.windows.net/olistdata/silver/',
        FORMAT = 'PARQUET'
    )AS result2
Where order_status = 'Delivered'
-- CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'yogitha@123';

-- CREATE DATABASE SCOPED CREDENTIAL adminyogitha WITH IDENTITY = 'Managed Identity';
-- select * from sys.database_credentials

CREATE EXTERNAL FILE FORMAT extfileformat WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);

CREATE EXTERNAL DATA SOURCE goldlayer WITH (
    LOCATION = 'https://ecommolistdatastorage.dfs.core.windows.net/olistdata/gold/',
    CREDENTIAL = adminyogitha
);

CREATE EXTERNAL TABLE gold.finaltable WITH (
        LOCATION = 'serving',
        DATA_SOURCE = goldlayer,
        FILE_FORMAT = extfileformat
) AS
SELECT * FROM gold.final2;