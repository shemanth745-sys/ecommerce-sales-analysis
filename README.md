# E-commerce Sales Analysis

End-to-end exploratory data analysis of an Indian e-commerce business: from raw, messy order data to cleaned KPIs, visual insights, and business recommendations.

## Business questions answered

1. What is our total revenue, order volume, and average order value?
2. Which months drive the most sales?
3. Which product categories and products bring in the most revenue?
4. Which regions perform best?
5. How do customers prefer to pay?
6. Do deeper discounts actually drive more revenue?
7. How loyal are our customers?

## Tech stack

- **Python 3.12**, **pandas**, **NumPy** — data cleaning & analysis
- **Matplotlib**, **Seaborn** — visualisations
- **Jupyter Notebook** — interactive analysis

## Project structure

```
ecommerce-sales-analysis/
├── data/
│   └── ecommerce_sales.csv      # 2,512 synthetic orders (Jan–Dec 2025)
├── notebooks/
│   └── sales_analysis.ipynb     # step-by-step analysis with narrative
├── src/
│   ├── generate_data.py         # reproducible dataset generator (seed 42)
│   └── analysis.py              # cleaning + KPIs + all charts
├── visuals/
│   ├── monthly_revenue.png
│   ├── category_revenue.png
│   ├── region_revenue.png
│   ├── payment_method.png
│   ├── discount_impact.png
│   └── top_products.png
├── requirements.txt
└── README.md
```

## Dataset

`data/ecommerce_sales.csv` — 2,512 orders across 15 columns: `OrderID`, `OrderDate`, `CustomerID`, `CustomerAge`, `CustomerGender`, `City`, `Region`, `Category`, `ProductName`, `Quantity`, `UnitPrice`, `DiscountPct`, `PaymentMethod`, `OrderStatus`, `Revenue`.

5 categories (Electronics, Fashion, Home & Kitchen, Beauty, Sports), 4 regions, 6 payment methods. The raw data intentionally contains **duplicates and missing values** so the cleaning steps are real.

## How to run

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) regenerate the dataset
python3 src/generate_data.py

# 4. Run the full analysis
python3 src/analysis.py

# 5. Or explore interactively
jupyter notebook notebooks/sales_analysis.ipynb
```

## Key findings

| Metric | Value |
|---|---|
| Total delivered revenue | **₹1.78 Cr** |
| Delivered orders | 2,136 |
| Unique customers | 1,003 |
| Average order value | **₹8,336** |
| Return rate | 3.4% |
| Cancellation rate | 5.0% |
| Repeat-customer rate | **62%** |

**Monthly trend** — October (₹23.1L) and November (₹22.6L) are the festive peak; July (₹20.4L) spikes on sale season.

![Monthly revenue](visuals/monthly_revenue.png)

**Category mix** — Electronics brings in ₹1.39 Cr, roughly **78% of all revenue**. The business is heavily concentrated in one category.

![Revenue by category](visuals/category_revenue.png)

**Top product** — Laptop alone contributes ₹77.9L, the single biggest revenue driver.

![Top products](visuals/top_products.png)

**Payments** — UPI dominates order volume; the checkout experience must stay UPI-first.

![Payment methods](visuals/payment_method.png)

**Discounts** — Revenue concentrates in the 0–20% discount buckets. Discounts above 20% add only ~₹19L of ₹178L total: deep discounting is mostly margin given away.

![Discount impact](visuals/discount_impact.png)

**Regions**

![Revenue by region](visuals/region_revenue.png)

## Recommendations

1. **Protect the festive peak** — stock Electronics inventory heavily for Oct–Nov; it drives ~25% of annual revenue.
2. **Cap deep discounts** — discounts above 20% barely move revenue; reinvest that margin into the 10–20% band.
3. **Keep checkout UPI-first** — the dominant payment mode must be the fastest, most reliable path.
4. **Diversify the mix** — with 78% of revenue from Electronics, Fashion and Home & Kitchen are the growth levers.
5. **Cut the 5% cancellation rate** — confirm high-value orders faster to recover lost revenue.

## Talking points for interviews

- *"Walk me through the project"* → raw CSV → deduplication → missing-value strategy (median/mode/0 by column semantics) → KPI layer → six targeted visualisations → five business recommendations.
- *"How did you handle missing data?"* → checked the mechanism per column: `CustomerAge` → median (numeric, symmetric), `PaymentMethod` → mode (categorical), `DiscountPct` → 0 (business logic: no discount recorded = no discount given).
- *"What would you do with real data?"* → validate against source systems, add cohort/retention analysis, build a forecast model for festive inventory, and automate the report on a schedule.

## Future improvements

- RFM customer segmentation and churn prediction
- Time-series forecasting for festive-season inventory planning
- Interactive dashboard (Streamlit / Power BI)
- A/B test analysis of discount strategies
