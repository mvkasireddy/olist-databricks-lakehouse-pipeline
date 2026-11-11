# Databricks notebook source
base_path = "/Volumes/workspace/default/olist_raw/"

tables = {
    "bronze_orders": "olist_orders_dataset.csv",
    "bronze_order_items": "olist_order_items_dataset.csv",
    "bronze_customers": "olist_customers_dataset.csv",
    "bronze_payments": "olist_order_payments_dataset.csv",
    "bronze_products": "olist_products_dataset.csv",
    "bronze_sellers": "olist_sellers_dataset.csv",
    "bronze_reviews": "olist_order_reviews_dataset.csv",
    "bronze_geolocation": "olist_geolocation_dataset.csv",
    "bronze_category_translation": "product_category_name_translation.csv"
}

for table_name, file_name in tables.items():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(base_path + file_name)
    )
    df.write.format("delta").mode("overwrite").saveAsTable(f"workspace.default.{table_name}")
    print(f"Loaded {table_name}: {df.count()} rows")

# COMMAND ----------

