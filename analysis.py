"""
E-commerce sales analysis: cleaning, KPIs, and visualisations.
Run: python3 src/analysis.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 10

# ---------------- 1. Load & clean ----------------
df = pd.read_csv("data/ecommerce_sales.csv")
print(f"Raw shape: {df.shape}")

df = df.drop_duplicates()
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())
df["PaymentMethod"] = df["PaymentMethod"].fillna(df["PaymentMethod"].mode()[0])
df["DiscountPct"] = df["DiscountPct"].fillna(0)
print(f"Clean shape: {df.shape} | nulls remaining: {int(df.isna().sum().sum())}")

delivered = df[df["OrderStatus"] == "Delivered"].copy()

# ---------------- 2. KPIs ----------------
total_revenue = delivered["Revenue"].sum()
total_orders = len(delivered)
aov = delivered["Revenue"].mean()
customers = delivered["CustomerID"].nunique()
return_rate = (df["OrderStatus"] == "Returned").mean() * 100
cancel_rate = (df["OrderStatus"] == "Cancelled").mean() * 100
print(f"\nTotal revenue (delivered): Rs.{total_revenue:,.0f}")
print(f"Delivered orders: {total_orders} | Unique customers: {customers}")
print(f"Avg order value: Rs.{aov:,.0f}")
print(f"Return rate: {return_rate:.1f}% | Cancel rate: {cancel_rate:.1f}%")

# ---------------- 3. Charts ----------------
# 3a. Monthly revenue trend
monthly = delivered.set_index("OrderDate").resample("M")["Revenue"].sum()
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.bar(monthly.index.strftime("%b"), monthly.values, color="#4C78A8", alpha=0.85)
ax.set_title("Monthly Revenue Trend (2025)", fontweight="bold")
ax.set_ylabel("Revenue (Rs.)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e5:.0f}L"))
for i, v in enumerate(monthly.values):
    ax.text(i, v, f"{v/1e5:.1f}L", ha="center", va="bottom", fontsize=8)
plt.tight_layout(); plt.savefig("visuals/monthly_revenue.png"); plt.close()

# 3b. Revenue by category
cat_rev = delivered.groupby("Category")["Revenue"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(cat_rev.index, cat_rev.values, color="#72B66A")
ax.set_title("Revenue by Product Category", fontweight="bold")
ax.set_xlabel("Revenue (Rs.)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e5:.0f}L"))
plt.tight_layout(); plt.savefig("visuals/category_revenue.png"); plt.close()
print("\nRevenue by category:\n", delivered.groupby("Category")["Revenue"].sum().sort_values(ascending=False).round(0))

# 3c. Revenue by region
reg = delivered.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(reg.index, reg.values, color="#F58518")
ax.set_title("Revenue by Region", fontweight="bold")
ax.set_ylabel("Revenue (Rs.)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e5:.0f}L"))
plt.tight_layout(); plt.savefig("visuals/region_revenue.png"); plt.close()

# 3d. Payment method share (donut)
pay = delivered["PaymentMethod"].value_counts()
fig, ax = plt.subplots(figsize=(6.5, 4.5))
wedges, texts, autotexts = ax.pie(pay.values, labels=pay.index, autopct="%1.0f%%",
                                  startangle=90, pctdistance=0.8,
                                  wedgeprops=dict(width=0.4, edgecolor="white"))
ax.set_title("Orders by Payment Method", fontweight="bold")
plt.tight_layout(); plt.savefig("visuals/payment_method.png"); plt.close()

# 3e. Discount impact: revenue & orders by discount bucket
delivered["DiscountBucket"] = pd.cut(delivered["DiscountPct"], bins=[-1, 0, 10, 20, 100],
                                     labels=["No discount", "1-10%", "11-20%", "20%+"])
disc = delivered.groupby("DiscountBucket", observed=True).agg(orders=("Revenue", "size"),
                                                              revenue=("Revenue", "sum"))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(disc.index.astype(str), disc["revenue"].values, color="#B279A2")
ax.set_title("Revenue by Discount Bucket", fontweight="bold")
ax.set_ylabel("Revenue (Rs.)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e5:.0f}L"))
plt.tight_layout(); plt.savefig("visuals/discount_impact.png"); plt.close()
print("\nDiscount bucket summary:\n", disc.round(0))

# 3f. Top 10 products by revenue
top_prod = delivered.groupby("ProductName")["Revenue"].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(top_prod.index[::-1], top_prod.values[::-1], color="#54A24B")
ax.set_title("Top 10 Products by Revenue", fontweight="bold")
ax.set_xlabel("Revenue (Rs.)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e3:.0f}K"))
plt.tight_layout(); plt.savefig("visuals/top_products.png"); plt.close()

# 3g. Repeat customers
orders_per_cust = delivered["CustomerID"].value_counts()
repeat_pct = (orders_per_cust > 1).mean() * 100
print(f"\nRepeat-customer rate: {repeat_pct:.1f}%")
print(f"Top product: {top_prod.index[0]} (Rs.{top_prod.iloc[0]:,.0f})")
print("\nSaved 7 charts to visuals/")
