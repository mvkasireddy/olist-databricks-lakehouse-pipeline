

# End-to-End E-Commerce Data Lakehouse Pipeline

**A Cloud Data Engineering & Business Intelligence Project using Databricks, PySpark, Delta Lake, Spark SQL and Power BI.**

![Project](https://img.shields.io/badge/Project-Data%20Engineering-blue)
![Platform](https://img.shields.io/badge/Platform-Databricks-orange)
![Processing](https://img.shields.io/badge/Processing-PySpark-green)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-purple)
![BI](https://img.shields.io/badge/BI-Power%20BI-yellow)

## Project Overview

This project implements an end-to-end E-Commerce Data Lakehouse Pipeline using the Brazilian E-Commerce Public Dataset by Olist.

The objective is to transform raw transactional data into structured, clean and analytics-ready datasets using Databricks and Apache Spark.

The pipeline follows the **Medallion Architecture (Bronze → Silver → Gold)** to perform data ingestion, data cleaning, standardization, transformation and dimensional modeling. The final Gold-layer datasets are used in Power BI to build interactive dashboards for analyzing sales performance, revenue, customer behavior and business operations.

## Business Problem

E-commerce platforms generate data across multiple operational systems, including orders, customers, products, payments, sellers and reviews.

Analyzing these datasets independently can lead to inconsistent data, duplicate records, complex joins and inaccurate business reporting.

This project addresses these challenges by:
- Consolidating multiple transactional datasets.
- Cleaning and standardizing inconsistent data.
- Transforming raw data into structured analytical tables.
- Building a Star Schema for efficient reporting.
- Presenting business metrics through Power BI dashboards.

## Technology Stack

| Category | Technologies |
|---|---|
| Cloud Data Platform | Databricks |
| Data Processing | Apache Spark, PySpark |
| Programming | Python |
| Data Storage | Delta Lake |
| Data Transformation | Spark SQL, SQL |
| Architecture | Medallion Architecture |
| Data Modeling | Star Schema |
| Data Visualization | Power BI Desktop |
| Analytics | DAX |
| Source Control | GitHub |

## Dataset Information

**Dataset:** Brazilian E-Commerce Public Dataset by Olist

**Source:** [Download Dataset – Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains approximately 100,000 orders placed between 2016 and 2018 across Brazilian marketplaces.

The project processes nine CSV datasets:

| Dataset | Description |
|---|---|
| Orders | Order details and delivery timestamps |
| Order Items | Product prices, freight and seller information |
| Customers | Customer identifiers and locations |
| Payments | Payment methods and transaction values |
| Products | Product details and categories |
| Sellers | Seller information and locations |
| Reviews | Customer ratings and review details |
| Geolocation | ZIP code and geographical coordinates |
| Category Translation | Portuguese-to-English product categories |

The raw dataset files are not included in this repository due to file-size limitations. Download them from the source above.

## System Architecture

The project uses a three-layer Medallion Architecture.

```text
             OLIST E-COMMERCE DATASET
                  9 CSV FILES
                       |
                       v
              DATABRICKS VOLUME
                       |
                       v
          +-------------------------+
          |      BRONZE LAYER       |
          |                         |
          | Raw CSV Ingestion       |
          | Delta Table Storage     |
          +-------------------------+
                       |
                       v
          +-------------------------+
          |      SILVER LAYER       |
          |                         |
          | Data Cleaning           |
          | Deduplication           |
          | Type Conversion         |
          | Standardization         |
          | Category Enrichment     |
          +-------------------------+
                       |
                       v
          +-------------------------+
          |       GOLD LAYER        |
          |                         |
          | Fact Table              |
          | Customer Dimension      |
          | Product Dimension       |
          | Star Schema              |
          +-------------------------+
                       |
                       v
             DATABRICKS SQL WAREHOUSE
                       |
                       v
          +-------------------------+
          |       POWER BI          |
          |                         |
          | DAX Measures            |
          | KPI Cards               |
          | Sales Analytics         |
          | Business Dashboards     |
          +-------------------------+
```

## Data Pipeline Implementation

### 1. Bronze Layer – Raw Data Ingestion

**Notebook:** `01_bronze_ingestion.py`

The Bronze layer ingests all nine Olist CSV datasets into Databricks and stores them as Delta tables.

Implementation:
- Reads CSV files using PySpark.
- Uses header-based column identification.
- Applies schema inference.
- Writes the datasets into Delta Lake.
- Stores the raw tables in the Databricks workspace.

**Output:** Nine Bronze Delta tables.

### 2. Silver Layer – Data Cleaning and Transformation

**Notebook:** `02_silver_cleaning.py`

The Silver layer transforms raw data into standardized datasets suitable for analytical processing.

Transformations implemented:

- Removes duplicate records using relevant identifiers.
- Converts order timestamps into proper timestamp formats.
- Converts price, freight and payment values into numeric data types.
- Standardizes customer city and state values.
- Enriches product data using the English category translation dataset.
- Creates cleaned Delta tables.

**Output:** Five cleaned Silver Delta tables.

### 3. Gold Layer – Dimensional Modeling

**Notebook:** `03_gold_star_schema.py`

The Gold layer converts cleaned transactional data into a Star Schema for business intelligence.

Three analytical tables are created:

**Fact Table**

`gold_fact_sales`

Contains:
- Order ID
- Order item ID
- Customer ID
- Product ID
- Seller ID
- Order status
- Purchase timestamp
- Order date
- Product price
- Freight value
- Total item value
- Payment type

Grain: One record per order line item.

**Dimension Tables**

`gold_dim_customers`

Contains customer identifiers, customer city and state information.

`gold_dim_products`

Contains product identifiers, English product categories and physical product attributes.

**Data Modeling Consideration**

Payment records can contain multiple entries for one order. The Gold transformation groups payment records by order ID before joining them with order items to avoid multiplying fact-table rows.

## Power BI Dashboard

The Gold-layer tables are used to develop an interactive Power BI dashboard.

**Dashboard capabilities:**

- Total product revenue analysis.
- Total fulfilled order analysis.
- Average Order Value (AOV).
- Total items sold.
- Payment method distribution.
- Monthly sales and revenue trends.
- Product category performance.
- Regional customer analysis.

### DAX Measures

```dax
Gold Revenue =
SUM(gold_fact_sales[price])

Gold Orders =
DISTINCTCOUNT(gold_fact_sales[order_id])

Gold AOV =
DIVIDE([Gold Revenue], [Gold Orders], 0)

Gold Items Sold =
COUNT(gold_fact_sales[order_item_id])
```

Note: Gold Revenue represents product price revenue and excludes freight charges.

### Dashboard File

The Power BI dashboard file is available in this repository:

`ecommerece visuals.pbix`

Open it using Power BI Desktop to explore the report.

## Repository Structure

```text
olist-databricks-lakehouse-pipeline/
│
├── 01_bronze_ingestion.py
│
├── 02_silver_cleaning.py
│
├── 03_gold_star_schema.py
│
├── ecommerece visuals.pbix
│
├── olist_customers_dataset.csv
│
├── Screenshot (17).png
├── Screenshot (18).png
├── Screenshot (19).png
├── Screenshot (20).png
├── Screenshot (21).png
├── Screenshot (22).png
├── Screenshot (23).png
├── Screenshot (24).png
├── Screenshot (25).png
│
└── README.md
```

## How to Run the Project

### Prerequisites

- Databricks workspace with Unity Catalog access.
- Databricks notebooks and Spark environment.
- Olist Brazilian E-Commerce dataset.
- Power BI Desktop.

### Step 1: Download the Dataset

Download the Olist dataset from Kaggle and extract all nine CSV files.

### Step 2: Upload Data to Databricks

Create a Unity Catalog Volume and upload the CSV files to:

```text
/Volumes/workspace/default/olist_raw/
```

### Step 3: Execute Bronze Ingestion

Import and execute:

```text
01_bronze_ingestion.py
```

This creates nine Bronze Delta tables.

### Step 4: Execute Silver Transformation

Execute:

```text
02_silver_cleaning.py
```

This creates five cleaned Silver Delta tables.

### Step 5: Execute Gold Modeling

Execute:

```text
03_gold_star_schema.py
```

This creates the sales fact table and two dimension tables.

### Step 6: Build Power BI Dashboard

Connect Power BI Desktop to the Databricks Gold tables, configure the relationships, create DAX measures and develop interactive visualizations.

**Execution order:** Bronze → Silver → Gold → Power BI.

The current notebook implementation uses overwrite-based table creation. Run the notebooks in the specified order when rebuilding the pipeline.

## Key Engineering Concepts Demonstrated

- End-to-End Data Engineering
- Cloud Data Lakehouse Architecture
- Medallion Architecture
- Distributed Data Processing using PySpark
- Delta Lake Table Management
- Data Cleaning and Deduplication
- Data Type Standardization
- SQL Joins and Aggregations
- Fact and Dimension Modeling
- Star Schema Design
- Business Intelligence
- DAX-Based KPI Development
- Power BI Dashboard Development

## Future Enhancements

Potential improvements for a production-oriented implementation:

- Incremental data ingestion using Databricks Auto Loader.
- Automated scheduling and orchestration using Databricks Workflows.
- Advanced data quality validation and monitoring.
- Data lineage and pipeline execution monitoring.
- Delta Lake optimization and partitioning.
- Additional analytical fact and dimension tables.

These are proposed enhancements and are not claimed as implemented features.

## Project Outcome

Developed an end-to-end E-Commerce Data Lakehouse Pipeline that transforms multiple raw transactional datasets into structured analytical data using Databricks, PySpark, Delta Lake and SQL.

Implemented Bronze, Silver and Gold processing layers, created a dimensional Star Schema, and developed a Power BI dashboard to support sales, revenue and operational analysis.

## Author

**Venkata Kasi Reddy Mandadi**

GitHub: [mvkasireddy](https://github.com/mvkasireddy)

LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/mandadi-venkata-kasi-67a4643a8/)



*This project was developed as a practical Data Engineering and Business Intelligence portfolio project using the public Olist e-commerce dataset.*


