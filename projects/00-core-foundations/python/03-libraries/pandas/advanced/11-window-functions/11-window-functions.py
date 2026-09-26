"""
Pandas Window Functions: rolling, expanding, ewm
=================================================

Time series analysis with moving windows, expanding windows, and exponential weighting.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# Create time series data
dates = pd.date_range("2023-01-01", periods=365, freq="D")
# Simulate stock price with trend and noise
trend = np.linspace(100, 150, 365)
seasonal = 10 * np.sin(np.arange(365) * 2 * np.pi / 365)
noise = np.random.randn(365) * 2
prices = trend + seasonal + noise

df = pd.DataFrame(
    {"date": dates, "price": prices, "volume": np.random.randint(100000, 1000000, 365)}
)
df = df.set_index("date")

print("Sample Time Series:")
print(df.head(10))
print(f"Shape: {df.shape}")
print()

# =============================================================================
# 1. ROLLING WINDOW
# =============================================================================

print("=" * 60)
print("1. ROLLING WINDOW")
print("=" * 60)

# Basic rolling
df["rolling_mean_7"] = df["price"].rolling(window=7).mean()
df["rolling_std_7"] = df["price"].rolling(window=7).std()
df["rolling_min_7"] = df["price"].rolling(window=7).min()
df["rolling_max_7"] = df["price"].rolling(window=7).max()

print("Rolling 7-day stats (first 15 rows):")
print(df[["price", "rolling_mean_7", "rolling_std_7"]].head(15))
print()

# Rolling with different window types
df["rolling_sum_30"] = df["price"].rolling(window=30).sum()
df["rolling_median_30"] = df["price"].rolling(window=30).median()
df["rolling_quantile_30"] = df["price"].rolling(window=30).quantile(0.95)

print("Rolling sum, median, 95th percentile (30-day):")
print(df[["price", "rolling_sum_30", "rolling_median_30", "rolling_quantile_30"]].head(35).tail(10))
print()


# Rolling apply - custom function
def rolling_sharpe(x):
    if len(x) < 2 or x.std() == 0:
        return np.nan
    return x.mean() / x.std()


df["rolling_sharpe_30"] = df["price"].rolling(window=30).apply(rolling_sharpe, raw=False)
print("Rolling Sharpe ratio (30-day):")
print(df[["price", "rolling_sharpe_30"]].head(35).tail(10))
print()

# Rolling on multiple columns
df[["rolling_mean_price_7", "rolling_mean_vol_7"]] = (
    df[["price", "volume"]].rolling(window=7).mean()
)
print("Rolling mean on multiple columns:")
print(df[["price", "volume", "rolling_mean_price_7", "rolling_mean_vol_7"]].head(10))
print()

# =============================================================================
# 2. ROLLING WITH TIME-AWARE WINDOWS
# =============================================================================

print("=" * 60)
print("2. TIME-AWARE ROLLING (window='7D')")
print("=" * 60)

# Create irregular time series
irregular_dates = pd.date_range("2023-01-01", "2023-01-31", freq="6h")
irregular_dates = irregular_dates[np.random.choice(len(irregular_dates), 50, replace=False)]
irregular_dates = irregular_dates.sort_values()

irregular_df = pd.DataFrame({"value": np.random.randn(50).cumsum() + 100}, index=irregular_dates)

print("Irregular time series:")
print(irregular_df.head(10))
print()

# Fixed window (counts rows)
irregular_df["rolling_5_rows"] = irregular_df["value"].rolling(window=5).mean()
# Time-aware window (counts time)
irregular_df["rolling_3_days"] = irregular_df["value"].rolling(window="3D").mean()

print("Rolling 5 rows vs 3 days:")
print(irregular_df[["value", "rolling_5_rows", "rolling_3_days"]].head(15))
print()

# =============================================================================
# 3. EXPANDING WINDOW
# =============================================================================

print("=" * 60)
print("3. EXPANDING WINDOW (CUMULATIVE)")
print("=" * 60)

df["expanding_mean"] = df["price"].expanding().mean()
df["expanding_std"] = df["price"].expanding().std()
df["expanding_min"] = df["price"].expanding().min()
df["expanding_max"] = df["price"].expanding().max()
df["expanding_count"] = df["price"].expanding().count()

print("Expanding stats:")
print(df[["price", "expanding_mean", "expanding_std", "expanding_min", "expanding_max"]].head(10))
print()

# Expanding apply
df["expanding_sharpe"] = df["price"].expanding().apply(rolling_sharpe, raw=False)
print("Expanding Sharpe:")
print(df[["price", "expanding_sharpe"]].head(15).tail(5))
print()

# =============================================================================
# 4. EXPONENTIAL WEIGHTED MOVING (EWM)
# =============================================================================

print("=" * 60)
print("4. EXPONENTIAL WEIGHTED MOVING (EWM)")
print("=" * 60)

# Span-based (common in finance)
df["ewm_span_10"] = df["price"].ewm(span=10, adjust=False).mean()
df["ewm_span_30"] = df["price"].ewm(span=30, adjust=False).mean()

# Alpha-based
df["ewm_alpha_0.1"] = df["price"].ewm(alpha=0.1, adjust=False).mean()
df["ewm_alpha_0.3"] = df["price"].ewm(alpha=0.3, adjust=False).mean()

# Half-life
df["ewm_halflife_5"] = df["price"].ewm(halflife=5, adjust=False).mean()

print("EWM comparisons (last 10 rows):")
print(df[["price", "ewm_span_10", "ewm_span_30", "ewm_alpha_0.1", "ewm_halflife_5"]].tail(10))
print()

# EWM std/var
df["ewm_std_10"] = df["price"].ewm(span=10, adjust=False).std()
df["ewm_var_10"] = df["price"].ewm(span=10, adjust=False).var()

print("EWM std/var (span=10):")
print(df[["price", "ewm_std_10", "ewm_var_10"]].tail(10))
print()

# =============================================================================
# 5. PRACTICAL APPLICATIONS
# =============================================================================

print("=" * 60)
print("5. PRACTICAL APPLICATIONS")
print("=" * 60)

# Application 1: Moving Average Crossover Strategy
df["sma_20"] = df["price"].rolling(window=20).mean()
df["sma_50"] = df["price"].rolling(window=50).mean()
df["signal"] = np.where(df["sma_20"] > df["sma_50"], 1, -1)  # 1 = long, -1 = short
df["position"] = df["signal"].shift(1)  # Avoid lookahead bias
df["returns"] = df["price"].pct_change()
df["strategy_returns"] = df["position"] * df["returns"]

print("Moving Average Crossover (last 20 days):")
print(df[["price", "sma_20", "sma_50", "signal", "strategy_returns"]].tail(20))
print()

# Cumulative returns
df["cum_returns"] = (1 + df["returns"]).cumprod()
df["cum_strategy"] = (1 + df["strategy_returns"]).cumprod()
print(f"Buy & Hold Return: {df['cum_returns'].iloc[-1]:.4f}")
print(f"Strategy Return: {df['cum_strategy'].iloc[-1]:.4f}")
print()

# Application 2: Bollinger Bands
df["bb_middle"] = df["price"].rolling(window=20).mean()
df["bb_std"] = df["price"].rolling(window=20).std()
df["bb_upper"] = df["bb_middle"] + 2 * df["bb_std"]
df["bb_lower"] = df["bb_middle"] - 2 * df["bb_std"]
df["bb_position"] = (df["price"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

print("Bollinger Bands (last 10):")
print(df[["price", "bb_middle", "bb_upper", "bb_lower", "bb_position"]].tail(10))
print()

# Application 3: Rolling correlation (between price and volume)
df["rolling_corr"] = df["price"].rolling(window=30).corr(df["volume"])
print("Rolling correlation price vs volume (last 10):")
print(df[["price", "volume", "rolling_corr"]].tail(10))
print()

# Application 4: Rolling linear regression (trend)
from scipy import stats


def rolling_slope(x):
    if len(x) < 2:
        return np.nan
    y = x.values
    x_vals = np.arange(len(y))
    slope, _, _, _, _ = stats.linregress(x_vals, y)
    return slope


df["rolling_slope_20"] = df["price"].rolling(window=20).apply(rolling_slope, raw=False)
print("Rolling slope (20-day trend):")
print(df[["price", "rolling_slope_20"]].tail(10))
print()

# Application 5: Volatility regime detection
df["volatility_20"] = df["returns"].rolling(window=20).std() * np.sqrt(252)  # Annualized
df["vol_regime"] = pd.qcut(df["volatility_20"].dropna(), q=3, labels=["Low", "Medium", "High"])
print("Volatility regimes (last 10):")
print(df[["price", "returns", "volatility_20", "vol_regime"]].tail(10))
print()

# =============================================================================
# 6. ADVANCED: GROUPBY + ROLLING
# =============================================================================

print("=" * 60)
print("6. GROUPBY + ROLLING")
print("=" * 60)

# Create multi-asset data
multi_dates = pd.date_range("2023-01-01", periods=100, freq="D")
assets = ["AAPL", "GOOGL", "MSFT"]
multi_data = []

for asset in assets:
    prices = 100 + np.random.randn(100).cumsum() * 2 + np.arange(100) * 0.1
    asset_df = pd.DataFrame({"date": multi_dates, "asset": asset, "price": prices})
    multi_data.append(asset_df)

multi_df = pd.concat(multi_data, ignore_index=True).set_index("date")

# Rolling per asset
multi_df["rolling_mean_10"] = multi_df.groupby("asset")["price"].transform(
    lambda x: x.rolling(10).mean()
)
multi_df["rolling_std_10"] = multi_df.groupby("asset")["price"].transform(
    lambda x: x.rolling(10).std()
)

print("Groupby + Rolling (AAPL only):")
print(
    multi_df[multi_df["asset"] == "AAPL"][
        ["asset", "price", "rolling_mean_10", "rolling_std_10"]
    ].tail(10)
)
print()

# =============================================================================
# 7. PERFORMANCE CONSIDERATIONS
# =============================================================================

print("=" * 60)
print("7. PERFORMANCE CONSIDERATIONS")
print("=" * 60)

import time

# Large DataFrame
large_df = pd.DataFrame(
    {"value": np.random.randn(100000).cumsum() + 100},
    index=pd.date_range("2020-01-01", periods=100000, freq="min"),
)

# Method 1: rolling with window (default)
start = time.time()
result1 = large_df["value"].rolling(window=1000).mean()
time1 = time.time() - start

# Method 2: rolling with min_periods
start = time.time()
result2 = large_df["value"].rolling(window=1000, min_periods=1).mean()
time2 = time.time() - start

# Method 3: ewm (often faster for large windows)
start = time.time()
result3 = large_df["value"].ewm(span=1000, adjust=False).mean()
time3 = time.time() - start

print(f"Rolling window=1000: {time1:.4f}s")
print(f"Rolling window=1000, min_periods=1: {time2:.4f}s")
print(f"EWM span=1000: {time3:.4f}s")
print()

# Tips
print("PERFORMANCE TIPS:")
print("1. Use min_periods=1 to avoid NaN at start (slightly faster)")
print("2. EWM is often faster than rolling for large windows")
print("3. Use raw=True in apply() when possible (passes numpy arrays)")
print("4. For groupby+rolling, consider transform() with vectorized ops")
print("5. Avoid apply() with Python functions - use built-in methods")

print("\n" + "=" * 60)
print("END OF WINDOW FUNCTIONS")
print("=" * 60)
