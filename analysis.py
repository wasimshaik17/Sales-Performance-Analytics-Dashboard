import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================
# LOAD DATASET
# ==========================

df = pd.read_csv(
    "data/Sample - Superstore.csv",
    encoding="latin1"
)

print("\nDATASET LOADED SUCCESSFULLY")
print("=" * 50)

# ==========================
# BASIC INFORMATION
# ==========================

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================
# DATA CLEANING
# ==========================

before_rows = df.shape[0]

df.drop_duplicates(inplace=True)

after_rows = df.shape[0]

print("\nDuplicate Rows Removed:", before_rows - after_rows)

# ==========================
# SALES AND PROFIT ANALYSIS
# ==========================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

print("\nSALES SUMMARY")
print("=" * 50)

print(f"Total Sales      : ${total_sales:,.2f}")
print(f"Total Profit     : ${total_profit:,.2f}")
print(f"Total Orders     : {total_orders}")

# ==========================
# REGION ANALYSIS
# ==========================

print("\nREGION WISE SALES")
print("=" * 50)

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)

# ==========================
# TOP CUSTOMERS
# ==========================

print("\nTOP 10 CUSTOMERS")
print("=" * 50)

top_customers = (
    df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_customers)

# ==========================
# TOP PRODUCTS
# ==========================

print("\nTOP 10 PRODUCTS")
print("=" * 50)

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

# ==========================
# CATEGORY ANALYSIS
# ==========================

print("\nCATEGORY SALES")
print("=" * 50)

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)

# ==========================
# MONTHLY SALES TREND
# ==========================

df["Order Date"] = pd.to_datetime(df["Order Date"])

df["Month"] = df["Order Date"].dt.month

monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
)

print("\nMONTHLY SALES")
print("=" * 50)
print(monthly_sales)

# ==========================
# CREATE OUTPUT FOLDER
# ==========================

if not os.path.exists("images"):
    os.makedirs("images")

# ==========================
# CHART 1
# MONTHLY SALES TREND
# ==========================

plt.figure(figsize=(10, 5))

monthly_sales.plot(
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.grid(True)

plt.savefig(
    "images/monthly_sales_trend.png"
)

plt.close()

# ==========================
# CHART 2
# REGION SALES
# ==========================

plt.figure(figsize=(8, 5))

region_sales.plot(
    kind="bar"
)

plt.title("Region Wise Sales")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "images/region_sales.png"
)

plt.close()

# ==========================
# CHART 3
# CATEGORY SALES
# ==========================

plt.figure(figsize=(8, 5))

category_sales.plot(
    kind="bar"
)

plt.title("Category Sales")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "images/category_sales.png"
)

plt.close()

# ==========================
# CHART 4
# TOP PRODUCTS
# ==========================

plt.figure(figsize=(12, 6))

top_products.plot(
    kind="bar"
)

plt.title("Top 10 Products")
plt.xlabel("Product")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "images/top_products.png"
)

plt.close()

# ==========================
# REPORT GENERATION
# ==========================

if not os.path.exists("reports"):
    os.makedirs("reports")

with open(
    "reports/sales_report.txt",
    "w"
) as file:

    file.write("SALES PERFORMANCE REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total Sales : ${total_sales:,.2f}\n")
    file.write(f"Total Profit : ${total_profit:,.2f}\n")
    file.write(f"Total Orders : {total_orders}\n\n")

    file.write("TOP REGION:\n")
    file.write(str(region_sales.head(1)))
    file.write("\n\n")

    file.write("TOP CUSTOMER:\n")
    file.write(str(top_customers.head(1)))
    file.write("\n\n")

    file.write("TOP PRODUCT:\n")
    file.write(str(top_products.head(1)))

print("\nREPORT GENERATED SUCCESSFULLY")
print("Saved in reports/sales_report.txt")

print("\nCHARTS SAVED SUCCESSFULLY")
print("Check images folder")

print("\nPROJECT COMPLETED SUCCESSFULLY")

print("\nADVANCED BUSINESS INSIGHTS")
print("=" * 50)

# Top Profit Making Products
profit_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 Profit Making Products:")
print(profit_products)

# Top Loss Making Products
loss_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
    .head(5)
)

print("\nTop 5 Loss Making Products:")
print(loss_products)

# Segment Analysis
segment_sales = (
    df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSegment Wise Sales:")
print(segment_sales)

# Ship Mode Analysis
ship_sales = (
    df.groupby("Ship Mode")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nShip Mode Analysis:")
print(ship_sales)

# Yearly Sales Analysis
df["Year"] = df["Order Date"].dt.year

yearly_sales = (
    df.groupby("Year")["Sales"]
    .sum()
)

print("\nYearly Sales:")
print(yearly_sales)

# Save Yearly Sales Chart
plt.figure(figsize=(10,5))
yearly_sales.plot(marker="o")
plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Sales")
plt.grid(True)
plt.savefig("images/yearly_sales_trend.png")
plt.close()

print("\nAdvanced analytics completed successfully")