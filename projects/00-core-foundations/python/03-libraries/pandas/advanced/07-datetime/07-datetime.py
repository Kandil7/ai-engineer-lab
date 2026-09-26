"""
Pandas Datetime: Timestamp, Timedelta, resampling, time zones
=============================================================

Complete guide to working with time series data in pandas.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. TIMESTAMP CREATION
# =============================================================================

print("=" * 60)
print("1. TIMESTAMP CREATION")
print("=" * 60)

# From string
ts1 = pd.Timestamp("2020-01-01")
print(f"From string: {ts1}, type: {type(ts1)}")

# From components
ts2 = pd.Timestamp(year=2020, month=1, day=1, hour=10, minute=30, second=45)
print(f"From components: {ts2}")

# From datetime
import datetime

ts3 = pd.Timestamp(datetime.datetime(2020, 1, 1, 10, 30, 45))
print(f"From datetime: {ts3}")

# From epoch (nanoseconds)
ts4 = pd.Timestamp(1577836800000000000)  # nanoseconds since epoch
print(f"From nanoseconds: {ts4}")

# Current time
ts_now = pd.Timestamp.now()
ts_today = pd.Timestamp.today()
print(f"Now: {ts_now}")
print(f"Today (midnight): {ts_today}")

# Array of timestamps
ts_array = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"])
print(f"Array: {ts_array}")
print(f"Type: {type(ts_array)}")

# DatetimeIndex
dti = pd.DatetimeIndex(["2020-01-01", "2020-01-02", "2020-01-03"])
print(f"DatetimeIndex: {dti}")
print(f"Freq: {dti.freq}")

# =============================================================================
# 2. DATE RANGES & FREQUENCIES
# =============================================================================

print("\n" + "=" * 60)
print("2. DATE RANGES & FREQUENCIES")
print("=" * 60)

# date_range - most common
dr1 = pd.date_range("2020-01-01", "2020-01-10", freq="D")
print(f"Daily range: {dr1}")

# Periods instead of end
dr2 = pd.date_range("2020-01-01", periods=10, freq="D")
print(f"10 periods daily: {dr2}")

# Business days
dr3 = pd.date_range("2020-01-01", periods=10, freq="B")
print(f"Business days: {dr3}")

# Monthly
dr4 = pd.date_range("2020-01-01", periods=6, freq="ME")  # month END ('M' removed in pandas 3)
print(f"Month end: {dr4}")

dr5 = pd.date_range("2020-01-01", periods=6, freq="MS")
print(f"Month start: {dr5}")

# Quarterly
dr6 = pd.date_range("2020-01-01", periods=4, freq="QE")  # quarter END ('Q' removed in pandas 3)
print(f"Quarter end: {dr6}")

# Hourly
dr7 = pd.date_range("2020-01-01", periods=24, freq="h")  # lowercase since pandas 3
print(f"Hourly (first 5): {dr7[:5]}")

# Minutes
dr8 = pd.date_range("2020-01-01", periods=60, freq="min")  # 'T' removed in pandas 3
print(f"Minutely (first 5): {dr8[:5]}")

# Custom frequency
dr9 = pd.date_range("2020-01-01", periods=10, freq="2D")
print(f"Every 2 days: {dr9}")

# Offset aliases
print("\nCommon frequency aliases:")
print("  D, B - Day, Business day")
print("  W - Week (Sunday)")
print("  M, MS - Month end/start")
print("  Q, QS - Quarter end/start")
print("  A, AS - Year end/start")
print("  H, T, S - Hour, Minute, Second")
print("  L, U, N - Millisecond, Microsecond, Nanosecond")

# =============================================================================
# 3. TIMEDELTA
# =============================================================================

print("\n" + "=" * 60)
print("3. TIMEDELTA")
print("=" * 60)

# Create Timedelta
td1 = pd.Timedelta("1 day")
td2 = pd.Timedelta("2 days 3 hours 4 minutes 5 seconds")
td3 = pd.Timedelta(days=1, hours=2, minutes=3, seconds=4)
td4 = pd.Timedelta(hours=25)

print(f"1 day: {td1}")
print(f"Complex: {td2}")
print(f"Components: {td3}")
print(f"25 hours: {td4}")
print(f"Total seconds: {td4.total_seconds()}")

# Timedelta arithmetic
ts = pd.Timestamp("2020-01-01 10:00:00")
print(f"\nTimestamp: {ts}")
print(f"+ 1 day: {ts + td1}")
print(f"+ 25 hours: {ts + td4}")
print(f"- 3 hours: {ts - pd.Timedelta(hours=3)}")

# TimedeltaIndex
td_index = pd.TimedeltaIndex(["1 day", "2 days", "3 days", "4 days"])
print(f"\nTimedeltaIndex: {td_index}")

# Series of timedeltas
td_series = pd.Series(pd.to_timedelta(["1 day", "2 days 3 hours", "45 minutes"]))
print(f"Timedelta Series:\n{td_series}")
print(f"Dtype: {td_series.dtype}")

# Components
print(f"\nComponents:")
print(f"  days: {td_series.dt.days.tolist()}")
print(f"  hours: {td_series.dt.components.hours.tolist()}")
print(f"  minutes: {td_series.dt.components.minutes.tolist()}")

# =============================================================================
# 4. TIME SERIES DATAFRAME
# =============================================================================

print("\n" + "=" * 60)
print("4. TIME SERIES DATAFRAME")
print("=" * 60)

# Create time series data
dates = pd.date_range("2020-01-01", periods=100, freq="h")
values = np.random.randn(100).cumsum() + 100

ts_df = pd.DataFrame(
    {"timestamp": dates, "value": values, "category": np.random.choice(["A", "B", "C"], 100)}
)

# Set timestamp as index
ts_df = ts_df.set_index("timestamp")
print("Time series DataFrame:")
print(ts_df.head())
print(f"Index type: {type(ts_df.index)}")
print(f"Index freq: {ts_df.index.freq}")

# Select by date
print("\nSelect '2020-01-01':")
print(ts_df.loc["2020-01-01"])

print("\nSelect '2020-01-01 10:00' to '2020-01-01 12:00':")
print(ts_df.loc["2020-01-01 10:00":"2020-01-01 12:00"])

print("\nSelect January 2020:")
print(ts_df.loc["2020-01"])

# =============================================================================
# 5. RESAMPLING (FREQUENCY CONVERSION)
# =============================================================================

print("\n" + "=" * 60)
print("5. RESAMPLING")
print("=" * 60)

# Downsample (hourly -> daily)
daily = ts_df["value"].resample("D").mean()
print("Daily mean (first 5):")
print(daily.head())

# Multiple aggregations
daily_agg = ts_df["value"].resample("D").agg(["mean", "std", "min", "max", "count"])
print("\nDaily aggregations:")
print(daily_agg.head())

# Upsample (daily -> hourly) with interpolation
daily_series = pd.Series(
    np.random.randn(10), index=pd.date_range("2020-01-01", periods=10, freq="D")
)
print("\nOriginal daily:")
print(daily_series)

hourly = daily_series.resample("h").interpolate("time")
print("\nUpsampled to hourly (first 5):")
print(hourly.head())

# Resample with groupby
grouped_resample = ts_df.groupby("category")["value"].resample("D").mean()
print("\nGrouped daily mean:")
print(grouped_resample.head(10))

# =============================================================================
# 6. ROLLING WINDOWS
# =============================================================================

print("\n" + "=" * 60)
print("6. ROLLING WINDOWS")
print("=" * 60)

# Rolling window on time series ('24H' removed in pandas 3 -> '24h')
ts_df["rolling_mean_24h"] = ts_df["value"].rolling("24h").mean()
ts_df["rolling_std_24h"] = ts_df["value"].rolling("24h").std()

print("Rolling 24H mean/std (first 30):")
print(ts_df[["value", "rolling_mean_24h", "rolling_std_24h"]].head(30))

# Expanding window
ts_df["expanding_mean"] = ts_df["value"].expanding().mean()
print("\nExpanding mean (first 10):")
print(ts_df[["value", "expanding_mean"]].head(10))

# EWM (Exponential Weighted Moving)
ts_df["ewm_span_24"] = ts_df["value"].ewm(span=24).mean()
print("\nEWM span=24 (first 10):")
print(ts_df[["value", "ewm_span_24"]].head(10))

# =============================================================================
# 7. TIME ZONES
# =============================================================================

print("\n" + "=" * 60)
print("7. TIME ZONES")
print("=" * 60)

# Create timezone-aware timestamps
ts_utc = pd.Timestamp("2020-01-01 12:00:00", tz="UTC")
ts_ny = pd.Timestamp("2020-01-01 12:00:00", tz="America/New_York")
ts_london = pd.Timestamp("2020-01-01 12:00:00", tz="Europe/London")

print(f"UTC: {ts_utc}")
print(f"NY: {ts_ny}")
print(f"London: {ts_london}")

# Localize naive timestamps
ts_naive = pd.Timestamp("2020-01-01 12:00:00")
ts_aware = ts_naive.tz_localize("UTC")
print(f"\nNaive: {ts_naive}")
print(f"Localized to UTC: {ts_aware}")

# Convert timezone
ts_ny_converted = ts_utc.tz_convert("America/New_York")
print(f"UTC to NY: {ts_ny_converted}")

# DataFrame with timezone
df_tz = pd.DataFrame(
    {"value": np.random.randn(5)}, index=pd.date_range("2020-01-01", periods=5, freq="h", tz="UTC")
)
print(f"\nDataFrame with UTC index:\n{df_tz}")

# Convert index timezone
df_ny = df_tz.tz_convert("America/New_York")
print(f"\nConverted to NY:\n{df_ny}")

# =============================================================================
# 8. PERIODS
# =============================================================================

print("\n" + "=" * 60)
print("8. PERIODS (SPAN-BASED)")
print("=" * 60)

# Period represents a span of time
p1 = pd.Period("2020-01", freq="M")
p2 = pd.Period("2020-01-01", freq="D")
p3 = pd.Period("2020-Q1", freq="Q")

print(f"Month period: {p1}")
print(f"Day period: {p2}")
print(f"Quarter period: {p3}")

# Period arithmetic
print(f"\n{p1} + 1 = {p1 + 1}")
print(f"{p1} - 2 = {p1 - 2}")

# PeriodIndex
period_idx = pd.period_range("2020-01", periods=12, freq="M")
print(f"\nPeriodIndex: {period_idx}")

# Convert between Period and Timestamp
ts_from_period = p1.to_timestamp()
print(f"\nPeriod to timestamp: {ts_from_period}")

period_from_ts = pd.Period(ts_naive, freq="M")
print(f"Timestamp to period: {period_from_ts}")

# =============================================================================
# 9. PRACTICAL TIME SERIES OPERATIONS
# =============================================================================

print("\n" + "=" * 60)
print("9. PRACTICAL OPERATIONS")
print("=" * 60)

# Create realistic time series
dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
np.random.seed(42)
sales = (
    1000
    + np.random.randn(len(dates)).cumsum() * 10
    + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 100
)

df_sales = pd.DataFrame({"sales": sales}, index=dates)

# 1. Monthly aggregation
monthly = df_sales.resample("ME").agg(["sum", "mean", "std"])
print("Monthly sales stats:")
print(monthly.head())

# 2. Year-over-year comparison (if multi-year)
# 3. Seasonal decomposition prep
df_sales["month"] = df_sales.index.month
df_sales["dayofweek"] = df_sales.index.dayofweek
df_sales["quarter"] = df_sales.index.quarter

monthly_avg = df_sales.groupby("month")["sales"].mean()
print("\nAverage sales by month:")
print(monthly_avg)

# 4. Shift / lag features
df_sales["sales_lag_1"] = df_sales["sales"].shift(1)
df_sales["sales_lag_7"] = df_sales["sales"].shift(7)
df_sales["sales_diff_1"] = df_sales["sales"].diff(1)
df_sales["sales_pct_change"] = df_sales["sales"].pct_change()

print("\nLag features (first 10):")
print(
    df_sales[["sales", "sales_lag_1", "sales_lag_7", "sales_diff_1", "sales_pct_change"]].head(10)
)

# 5. Rolling statistics for anomaly detection
df_sales["rolling_mean_7"] = df_sales["sales"].rolling(7).mean()
df_sales["rolling_std_7"] = df_sales["sales"].rolling(7).std()
df_sales["z_score"] = (df_sales["sales"] - df_sales["rolling_mean_7"]) / df_sales["rolling_std_7"]
anomalies = df_sales[abs(df_sales["z_score"]) > 3]
print(f"\nAnomalies (|z| > 3): {len(anomalies)} found")
if len(anomalies) > 0:
    print(anomalies[["sales", "rolling_mean_7", "z_score"]].head())

# 6. Business day operations
bday_range = pd.date_range("2023-01-01", "2023-01-31", freq="B")
print(f"\nBusiness days in Jan 2023: {len(bday_range)}")

# Custom business day (e.g., US holidays)
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

us_bday = CustomBusinessDay(calendar=USFederalHolidayCalendar())
us_range = pd.date_range("2023-01-01", "2023-01-31", freq=us_bday)
print(f"US business days in Jan 2023: {len(us_range)}")

print("\n" + "=" * 60)
print("END OF DATETIME")
print("=" * 60)
