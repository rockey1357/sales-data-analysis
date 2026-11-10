import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
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

plt.rcParams["font.family"] = "Arial"


# =====================================================
# 1. MONTHLY SALES - LINE GRAPH
# =====================================================

df["sale_date"] = pd.to_datetime(df["sale_date"])

monthly_sales = df.groupby(
    df["sale_date"].dt.strftime("%b")
)["sales_amount"].sum()

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

monthly_sales = monthly_sales.reindex(
    [x for x in month_order if x in monthly_sales.index]
)

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=3,
    markersize=8
)

plt.fill_between(
    range(len(monthly_sales)),
    monthly_sales.values,
    alpha=0.15
)

plt.title(
    "Monthly Sales Performance",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Sales Amount")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.25
)

plt.tight_layout()

plt.savefig(
    "static/monthly_sales.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 2. PRODUCT SALES - MODERN BAR GRAPH
# =====================================================

product_sales = df.groupby(
    "product_name"
)["sales_amount"].sum().sort_values(ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(
    product_sales.index,
    product_sales.values,
    height=0.6
)

plt.title(
    "Sales by Product",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Sales Amount")

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

for bar in bars:

    width = bar.get_width()

    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f" ₹{width:,.0f}",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    "static/product_sales.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 3. CATEGORY SALES - DONUT CHART
# =====================================================

category_sales = df.groupby(
    "category"
)["sales_amount"].sum()

plt.figure(figsize=(7, 7))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={
        "width": 0.42,
        "edgecolor": "white"
    },
    textprops={
        "fontsize": 11
    }
)

plt.title(
    "Sales by Category",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "static/category_sales.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 4. REGION SALES - RANKED BAR GRAPH
# =====================================================

region_sales = df.groupby(
    "region"
)["sales_amount"].sum().sort_values(ascending=True)

plt.figure(figsize=(9, 5))

bars = plt.barh(
    region_sales.index,
    region_sales.values,
    height=0.55
)

plt.title(
    "Regional Sales Performance",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Sales Amount")

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

for bar in bars:

    width = bar.get_width()

    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f" ₹{width:,.0f}",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    "static/region_sales.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()


print("New modern charts created successfully!")