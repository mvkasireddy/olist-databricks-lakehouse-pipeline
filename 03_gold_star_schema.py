# Databricks notebook source
# MAGIC %sql
# MAGIC -- 1. Gold Dimension: Customers
# MAGIC CREATE OR REPLACE TABLE workspace.default.gold_dim_customers AS
# MAGIC SELECT DISTINCT
# MAGIC     customer_id,
# MAGIC     customer_unique_id,
# MAGIC     customer_city,
# MAGIC     customer_state
# MAGIC FROM workspace.default.silver_customers;
# MAGIC
# MAGIC -- 2. Gold Dimension: Products (with English category names!)
# MAGIC CREATE OR REPLACE TABLE workspace.default.gold_dim_products AS
# MAGIC SELECT DISTINCT
# MAGIC     product_id,
# MAGIC     product_category_english AS category_name,
# MAGIC     product_weight_g,
# MAGIC     product_length_cm,
# MAGIC     product_height_cm,
# MAGIC     product_width_cm
# MAGIC FROM workspace.default.silver_products;
# MAGIC
# MAGIC -- 3. Gold Fact Table: Sales
# MAGIC CREATE OR REPLACE TABLE workspace.default.gold_fact_sales AS
# MAGIC WITH primary_payment AS (
# MAGIC     SELECT 
# MAGIC         order_id,
# MAGIC         FIRST(payment_type) AS payment_type,
# MAGIC         SUM(payment_value) AS total_payment_value
# MAGIC     FROM workspace.default.silver_payments
# MAGIC     GROUP BY order_id
# MAGIC )
# MAGIC SELECT 
# MAGIC     oi.order_id,
# MAGIC     oi.order_item_id,
# MAGIC     o.customer_id,
# MAGIC     oi.product_id,
# MAGIC     oi.seller_id,
# MAGIC     o.order_status,
# MAGIC     o.order_purchase_timestamp,
# MAGIC     DATE(o.order_purchase_timestamp) AS order_date,
# MAGIC     oi.price,
# MAGIC     oi.freight_value,
# MAGIC     (oi.price + oi.freight_value) AS total_item_value,
# MAGIC     COALESCE(p.payment_type, 'unknown') AS payment_type
# MAGIC FROM workspace.default.silver_order_items oi
# MAGIC JOIN workspace.default.silver_orders o 
# MAGIC     ON oi.order_id = o.order_id
# MAGIC LEFT JOIN primary_payment p 
# MAGIC     ON oi.order_id = p.order_id;

# COMMAND ----------

