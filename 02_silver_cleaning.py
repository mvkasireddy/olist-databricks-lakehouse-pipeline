# Databricks notebook source
from pyspark.sql import functions as F

# 1. Clean Orders
df_orders = (
    spark.table("workspace.default.bronze_orders")
    .dropDuplicates(["order_id"])
    .withColumn("order_purchase_timestamp", F.to_timestamp("order_purchase_timestamp"))
    .withColumn("order_delivered_customer_date", F.to_timestamp("order_delivered_customer_date"))
    .withColumn("order_estimated_delivery_date", F.to_timestamp("order_estimated_delivery_date"))
)
df_orders.write.format("delta").mode("overwrite").saveAsTable("workspace.default.silver_orders")

# 2. Clean Order Items
df_items = (
    spark.table("workspace.default.bronze_order_items")
    .dropDuplicates(["order_id", "order_item_id"])
    .withColumn("price", F.col("price").cast("double"))
    .withColumn("freight_value", F.col("freight_value").cast("double"))
)
df_items.write.format("delta").mode("overwrite").saveAsTable("workspace.default.silver_order_items")

# 3. Clean Customers
df_customers = (
    spark.table("workspace.default.bronze_customers")
    .dropDuplicates(["customer_id"])
    .withColumn("customer_city", F.initcap(F.trim("customer_city")))
    .withColumn("customer_state", F.upper(F.trim("customer_state")))
)
df_customers.write.format("delta").mode("overwrite").saveAsTable("workspace.default.silver_customers")

# 4. Clean Products & Join English Category Names
df_products = spark.table("workspace.default.bronze_products").dropDuplicates(["product_id"])
df_trans = spark.table("workspace.default.bronze_category_translation")

df_products_clean = (
    df_products.join(df_trans, on="product_category_name", how="left")
    .withColumn(
        "product_category_english",
        F.coalesce(F.col("product_category_name_english"), F.col("product_category_name"), F.lit("unknown"))
    )
    .drop("product_category_name_english")
)
df_products_clean.write.format("delta").mode("overwrite").saveAsTable("workspace.default.silver_products")

# 5. Clean Payments
df_payments = (
    spark.table("workspace.default.bronze_payments")
    .withColumn("payment_value", F.col("payment_value").cast("double"))
)
df_payments.write.format("delta").mode("overwrite").saveAsTable("workspace.default.silver_payments")

print("All Silver Delta tables created successfully!")

# COMMAND ----------

