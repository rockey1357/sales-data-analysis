import os
import mysql.connector
import pandas as pd
import numpy as np

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("DB_PASSWORD", ""),
    database="sales_analysis"
)

query = "SELECT * FROM sales"

df = pd.read_sql(query, connection)

connection.close()

df["sales_amount"] = df["quantity"] * df["price"]

print("\nSALES DATA")
print(df)

print("\nTOTAL SALES")
print(df["sales_amount"].sum())

print("\nTOTAL QUANTITY")
print(df["quantity"].sum())

print("\nAVERAGE SALES")
print(np.mean(df["sales_amount"]))

print("\nSALES BY PRODUCT")
print(df.groupby("product_name")["sales_amount"].sum())

print("\nSALES BY REGION")
print(df.groupby("region")["sales_amount"].sum())