"""
Pandas Case Study: Exploratory Data Analysis (EDA)
===================================================

End-to-end EDA on a realistic dataset using all pandas techniques learned.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import seaborn as sns  # noqa: F401  (optional; unused in this script)

    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("[skip] seaborn not installed — pip install seaborn")

np.random.seed(42)

# =============================================================================
# 1. GENERATE SYNTHETIC E-COMMERCE DATA
# =============================================================================

print("=" * 60)
print("1. DATA GENERATION")
print("=" * 60)

n_customers = 5000
n_orders = 50000
n_products = 200

# Customers
customers = pd.DataFrame(
    {
        "customer_id": range(1, n_customers + 1),
        "signup_date": pd.date_range("2020-01-01", periods=n_customers, freq="h"),
        "age": np.random.randint(18, 75, n_customers),
        "gender": np.random.choice(["M", "F", "Other"], n_customers, p=[0.48, 0.48, 0.04]),
        "country": np.random.choice(
            ["US", "UK", "CA", "AU", "DE", "FR", "JP"],
            n_customers,
            p=[0.35, 0.15, 0.10, 0.08, 0.12, 0.10, 0.10],
        ),
        "city": [f"City_{np.random.randint(1, 100)}" for _ in range(n_customers)],
        "is_premium": np.random.choice([True, False], n_customers, p=[0.2, 0.8]),
        "acquisition_channel": np.random.choice(
            ["Organic", "Paid", "Referral", "Social", "Email"],
            n_customers,
            p=[0.4, 0.3, 0.15, 0.1, 0.05],
        ),
    }
)

# Products
products = pd.DataFrame(
    {
        "product_id": range(1, n_products + 1),
        "category": np.random.choice(
            ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"], n_products
        ),
        "brand": [f"Brand_{np.random.randint(1, 30)}" for _ in range(n_products)],
        "base_price": np.random.lognormal(3, 1, n_products).round(2),
        "cost": np.random.lognormal(2.5, 0.8, n_products).round(2),
        "weight_kg": np.random.exponential(2, n_products).round(2),
        "is_active": np.random.choice([True, False], n_products, p=[0.85, 0.15]),
    }
)

# Orders
order_dates = pd.date_range("2022-01-01", "2023-12-31", freq="h")
orders = pd.DataFrame(
    {
        "order_id": range(1, n_orders + 1),
        "customer_id": np.random.randint(1, n_customers + 1, n_orders),
        "product_id": np.random.randint(1, n_products + 1, n_orders),
        "order_date": np.random.choice(order_dates, n_orders),
        "quantity": np.random.choice([1, 2, 3, 4, 5], n_orders, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
        "discount_pct": np.random.choice(
            [0, 0.05, 0.1, 0.15, 0.2], n_orders, p=[0.5, 0.2, 0.15, 0.1, 0.05]
        ),
        "shipping_cost": np.random.exponential(8, n_orders).round(2),
        "payment_method": np.random.choice(
            ["Credit Card", "PayPal", "Apple Pay", "Bank Transfer"],
            n_orders,
            p=[0.5, 0.25, 0.15, 0.1],
        ),
        "status": np.random.choice(
            ["Delivered", "Shipped", "Processing", "Cancelled", "Returned"],
            n_orders,
            p=[0.7, 0.15, 0.05, 0.05, 0.05],
        ),
    }
)

# Merge to get prices (include 'cost' — it is used below for profit)
orders = orders.merge(
    products[["product_id", "base_price", "cost", "category", "brand"]], on="product_id", how="left"
)
orders["revenue"] = orders["quantity"] * orders["base_price"] * (1 - orders["discount_pct"])
orders["profit"] = (
    orders["revenue"] - (orders["quantity"] * orders["cost"]) - orders["shipping_cost"]
)

print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
print()

# =============================================================================
# 2. DATA QUALITY ASSESSMENT
# =============================================================================

print("=" * 60)
print("2. DATA QUALITY ASSESSMENT")
print("=" * 60)


def assess_quality(df, name):
    print(f"\n--- {name} ---")
    print(f"Shape: {df.shape}")
    print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"Dtypes:\n{df.dtypes.value_counts()}")
    print(f"Missing:\n{df.isna().sum()[df.isna().sum() > 0]}")
    print(f"Duplicates: {df.duplicated().sum()}")

    # Numeric summary
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        print(f"Numeric summary:\n{df[num_cols].describe().round(2)}")

    # Categorical summary
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols[:3]:
        print(f"{col} unique: {df[col].nunique()}, top: {df[col].value_counts().head(3).to_dict()}")


assess_quality(customers, "Customers")
assess_quality(products, "Products")
assess_quality(orders, "Orders")

# =============================================================================
# 3. FEATURE ENGINEERING
# =============================================================================

print("=" * 60)
print("3. FEATURE ENGINEERING")
print("=" * 60)

# Customer features
customer_features = (
    orders.groupby("customer_id")
    .agg(
        total_orders=("order_id", "count"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_order_value=("revenue", "mean"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max"),
        unique_products=("product_id", "nunique"),
        unique_categories=("category", "nunique"),
        avg_discount=("discount_pct", "mean"),
        return_rate=("status", lambda x: (x == "Returned").mean()),
    )
    .reset_index()
)

customer_features["customer_lifetime_days"] = (
    customer_features["last_order"] - customer_features["first_order"]
).dt.days
customer_features["purchase_frequency"] = customer_features["total_orders"] / customer_features[
    "customer_lifetime_days"
].replace(0, 1)
customer_features["is_repeat"] = customer_features["total_orders"] > 1

# RFM Analysis
rfm = customer_features.copy()
rfm["Recency"] = (orders["order_date"].max() - rfm["last_order"]).dt.days
rfm["Frequency"] = rfm["total_orders"]
rfm["Monetary"] = rfm["total_revenue"]

# RFM Scoring (quintiles)
for col in ["Recency", "Frequency", "Monetary"]:
    if col == "Recency":
        rfm[f"{col}_Score"] = pd.qcut(rfm[col], 5, labels=[5, 4, 3, 2, 1], duplicates="drop")
    else:
        rfm[f"{col}_Score"] = pd.qcut(rfm[col], 5, labels=[1, 2, 3, 4, 5], duplicates="drop")

rfm["RFM_Score"] = (
    rfm[["Recency_Score", "Frequency_Score", "Monetary_Score"]].astype(str).agg("".join, axis=1)
)


# Segment customers
def segment_customer(row):
    if row["RFM_Score"].startswith("55"):
        return "Champions"
    elif row["RFM_Score"].startswith("5"):
        return "Loyal"
    elif row["RFM_Score"].startswith("4"):
        return "Potential"
    elif row["RFM_Score"].startswith("3"):
        return "At Risk"
    else:
        return "Lost"


rfm["Segment"] = rfm.apply(segment_customer, axis=1)

print("RFM Segments:")
print(rfm["Segment"].value_counts())
print()

# Product features
product_features = (
    orders.groupby("product_id")
    .agg(
        total_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_orders=("order_id", "count"),
        avg_discount=("discount_pct", "mean"),
        return_rate=("status", lambda x: (x == "Returned").mean()),
    )
    .reset_index()
)

product_features = product_features.merge(
    products[["product_id", "base_price", "cost", "category", "brand"]], on="product_id"
)
product_features["margin"] = (
    product_features["base_price"] - product_features["cost"]
) / product_features["base_price"]

# =============================================================================
# 4. EXPLORATORY ANALYSIS
# =============================================================================

print("=" * 60)
print("4. EXPLORATORY ANALYSIS")
print("=" * 60)

# Time series analysis
orders_ts = orders.set_index("order_date").sort_index()

# Monthly revenue
monthly_rev = orders_ts["revenue"].resample("ME").sum()
monthly_orders = orders_ts["order_id"].resample("ME").count()

print("Monthly Revenue Trend:")
print(monthly_rev.tail(12).to_string())
print()

# Year-over-year
monthly_rev_df = monthly_rev.reset_index()
monthly_rev_df["year"] = monthly_rev_df["order_date"].dt.year
monthly_rev_df["month"] = monthly_rev_df["order_date"].dt.month

yoy = monthly_rev_df.pivot_table(values="revenue", index="month", columns="year", aggfunc="sum")
print("Year-over-Year Monthly Revenue:")
print(yoy.round(0).to_string())
print()

# Category analysis
cat_revenue = orders.groupby("category")["revenue"].sum().sort_values(ascending=False)
cat_margin = (
    orders.groupby("category")["profit"].sum() / orders.groupby("category")["revenue"].sum()
)
print("Revenue by Category:")
print(cat_revenue.to_string())
print()
print("Margin by Category:")
print(cat_margin.round(3).to_string())
print()

# Customer cohort analysis
cohort_data = orders.merge(customers[["customer_id", "signup_date"]], on="customer_id")
cohort_data["cohort"] = cohort_data["signup_date"].dt.to_period("M")
cohort_data["order_month"] = cohort_data["order_date"].dt.to_period("M")
cohort_data["period"] = (cohort_data["order_month"] - cohort_data["cohort"]).apply(lambda x: x.n)

cohort_matrix = (
    cohort_data.groupby(["cohort", "period"])["customer_id"].nunique().unstack(fill_value=0)
)
cohort_sizes = cohort_matrix.iloc[:, 0]
retention = cohort_matrix.div(cohort_sizes, axis=0)

print("Cohort Retention (first 6 months):")
print(retention.iloc[:, :6].round(3).to_string())
print()

# =============================================================================
# 5. STATISTICAL ANALYSIS
# =============================================================================

print("=" * 60)
print("5. STATISTICAL ANALYSIS")
print("=" * 60)

from scipy import stats

# A/B test simulation: Premium vs Regular customers
premium_revenue = orders.merge(customers[["customer_id", "is_premium"]], on="customer_id")
premium_rev = premium_revenue[premium_revenue["is_premium"]]["revenue"]
regular_rev = premium_revenue[~premium_revenue["is_premium"]]["revenue"]

t_stat, p_val = stats.ttest_ind(premium_rev, regular_rev, equal_var=False)
print(f"Premium vs Regular Revenue t-test:")
print(f"  t-statistic: {t_stat:.4f}, p-value: {p_val:.6f}")
print(f"  Premium mean: ${premium_rev.mean():.2f}, Regular mean: ${regular_rev.mean():.2f}")
print()

# Correlation analysis
numeric_orders = orders.select_dtypes(include=[np.number])
corr_matrix = numeric_orders.corr()
print("Top correlations with revenue:")
print(corr_matrix["revenue"].sort_values(ascending=False).head(10))
print()

# Anomaly detection (isolation forest concept with IQR)
Q1 = orders["revenue"].quantile(0.25)
Q3 = orders["revenue"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = orders[(orders["revenue"] < lower) | (orders["revenue"] > upper)]
print(
    f"Revenue outliers (IQR method): {len(outliers)} orders ({len(outliers) / len(orders) * 100:.1f}%)"
)
print()

# =============================================================================
# 6. PREDICTIVE FEATURES FOR ML
# =============================================================================

print("=" * 60)
print("6. ML FEATURE PREPARATION")
print("=" * 60)

# Target: Will customer order in next 30 days?
cutoff_date = orders["order_date"].max() - pd.Timedelta(days=30)
recent_customers = orders[orders["order_date"] > cutoff_date]["customer_id"].unique()

ml_features = customer_features.copy()
ml_features["will_order_30d"] = ml_features["customer_id"].isin(recent_customers).astype(int)

# Select features
feature_cols = [
    "total_orders",
    "total_revenue",
    "avg_order_value",
    "customer_lifetime_days",
    "purchase_frequency",
    "unique_products",
    "unique_categories",
    "avg_discount",
    "return_rate",
    "is_repeat",
]

X = ml_features[feature_cols].fillna(0)
y = ml_features["will_order_30d"]

print(f"Feature matrix: {X.shape}")
print(f"Target distribution:\n{y.value_counts(normalize=True)}")
print()

# Feature importance preview (correlation with target)
feature_corr = X.copy()
feature_corr["target"] = y
correlations = feature_corr.corr()["target"].drop("target").sort_values(key=abs, ascending=False)
print("Feature correlations with target:")
print(correlations.round(4))
print()

# =============================================================================
# 7. SUMMARY REPORT
# =============================================================================

print("=" * 60)
print("7. EDA SUMMARY")
print("=" * 60)

summary = f"""
E-COMMERCE EDA SUMMARY
======================

DATA OVERVIEW:
- {len(customers):,} customers across {customers["country"].nunique()} countries
- {len(products):,} products in {products["category"].nunique()} categories
- {len(orders):,} orders from {orders["order_date"].min().date()} to {orders["order_date"].max().date()}
- Total Revenue: ${orders["revenue"].sum():,.2f}
- Total Profit: ${orders["profit"].sum():,.2f}
- Overall Margin: {orders["profit"].sum() / orders["revenue"].sum():.1%}

KEY INSIGHTS:
1. Top Category: {cat_revenue.index[0]} (${cat_revenue.iloc[0]:,.0f} revenue)
2. Best Margin: {cat_margin.idxmax()} ({cat_margin.max():.1%})
3. Premium customers: {customers["is_premium"].sum():,} ({customers["is_premium"].mean():.1%})
4. Repeat rate: {customer_features["is_repeat"].mean():.1%}
5. RFM Champions: {rfm["Segment"].value_counts().get("Champions", 0):,} customers

RFM SEGMENTS:
{rfm["Segment"].value_counts().to_string()}

ML READINESS:
- Features: {len(feature_cols)}
- Samples: {len(X):,}
- Target rate: {y.mean():.1%}
- Top predictive feature: {correlations.index[0]} ({correlations.iloc[0]:.4f})

NEXT STEPS:
1. Build churn prediction model using RFM features
2. Optimize pricing by category based on margin analysis
3. Target 'At Risk' segment with retention campaigns
4. A/B test premium vs regular customer experience
"""
print(summary)

print("\n" + "=" * 60)
print("END OF EDA CASE STUDY")
print("=" * 60)
