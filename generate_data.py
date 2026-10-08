"""
Synthetic e-commerce sales dataset generator.
Creates data/ecommerce_sales.csv with realistic Indian e-commerce orders.
Seeded for reproducibility.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

N = 2500

# --- Catalog: category -> list of (product, base_price_inr) ---
CATALOG = {
    "Electronics": [
        ("Smartphone", 15999), ("Laptop", 52990), ("Headphones", 2499),
        ("Smartwatch", 4999), ("Tablet", 18999),
    ],
    "Fashion": [
        ("T-Shirt", 599), ("Jeans", 1499), ("Sneakers", 2299),
        ("Jacket", 2799), ("Dress", 1299),
    ],
    "Home & Kitchen": [
        ("Cookware Set", 3499), ("Mixer Grinder", 4299), ("Bedsheet Set", 1199),
        ("Air Fryer", 7999), ("Table Lamp", 899),
    ],
    "Beauty": [
        ("Skincare Kit", 1499), ("Perfume", 1899), ("Hair Dryer", 1799),
        ("Makeup Set", 999),
    ],
    "Sports": [
        ("Cricket Bat", 2499), ("Yoga Mat", 799), ("Dumbbell Set", 1999),
        ("Football", 1099), ("Badminton Racket", 1399),
    ],
}

CITIES = {
    "Delhi": "North", "Jaipur": "North", "Lucknow": "North",
    "Mumbai": "West", "Pune": "West", "Ahmedberg": "West",
    "Bengaluru": "South", "Hyderabad": "South", "Chennai": "South",
    "Kolkata": "East", "Patna": "East", "Guwahati": "East",
}
# fix typo city name
CITIES["Ahmedabad"] = CITIES.pop("Ahmedberg")

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking", "Wallet"]
PAYMENT_PROBS = [0.42, 0.20, 0.12, 0.14, 0.07, 0.05]

STATUSES = ["Delivered", "Shipped", "Cancelled", "Returned"]
STATUS_PROBS = [0.86, 0.06, 0.05, 0.03]

categories = list(CATALOG.keys())
cat_probs = [0.30, 0.28, 0.18, 0.14, 0.10]

rows = []
start = np.datetime64("2025-01-01")
for i in range(N):
    # Seasonal tilt: festive spike Oct-Nov (Diwali), sale spike Jul
    month = int(rng.integers(1, 13))
    weights = np.ones(12)
    weights[9] = 1.8   # Oct
    weights[10] = 1.6  # Nov
    weights[6] = 1.4   # Jul sale
    weights = weights / weights.sum()
    month = int(rng.choice(np.arange(1, 13), p=weights))
    day = int(rng.integers(1, 29))
    date = f"2025-{month:02d}-{day:02d}"

    cat = str(rng.choice(categories, p=cat_probs))
    product, base_price = CATALOG[cat][int(rng.integers(0, len(CATALOG[cat])))]
    qty = int(rng.choice([1, 1, 1, 2, 2, 3, 4], p=[0.45, 0.2, 0.1, 0.12, 0.08, 0.03, 0.02]))
    unit_price = round(base_price * float(rng.uniform(0.92, 1.08)), 2)
    discount = float(rng.choice([0, 5, 10, 15, 20, 25, 30, 40],
                                p=[0.25, 0.15, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02]))
    city = str(rng.choice(list(CITIES.keys())))
    payment = str(rng.choice(PAYMENT_METHODS, p=PAYMENT_PROBS))
    status = str(rng.choice(STATUSES, p=STATUS_PROBS))
    revenue = round(qty * unit_price * (1 - discount / 100), 2)

    rows.append({
        "OrderID": f"ORD-{100001 + i}",
        "OrderDate": date,
        "CustomerID": f"CUST-{int(rng.integers(1, 1201)):05d}",
        "CustomerAge": int(rng.integers(18, 66)),
        "CustomerGender": str(rng.choice(["Male", "Female"], p=[0.52, 0.48])),
        "City": city,
        "Region": CITIES[city],
        "Category": cat,
        "ProductName": product,
        "Quantity": qty,
        "UnitPrice": unit_price,
        "DiscountPct": discount,
        "PaymentMethod": payment,
        "OrderStatus": status,
        "Revenue": revenue,
    })

df = pd.DataFrame(rows)

# Inject realistic data-quality issues for the cleaning demo
dup_idx = rng.choice(df.index, size=12, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)
for col in ["CustomerAge", "PaymentMethod", "DiscountPct"]:
    miss_idx = rng.choice(df.index, size=15, replace=False)
    df.loc[miss_idx, col] = np.nan

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/ecommerce_sales.csv", index=False)
print(f"Saved data/ecommerce_sales.csv with {len(df)} rows x {df.shape[1]} columns")
print(df.head(3).to_string())
