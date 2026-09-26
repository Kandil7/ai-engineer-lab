"""
Pandas I/O: CSV, JSON, Excel, Parquet, SQL, HTML
==================================================

Reading and writing data in various formats.
"""

import pandas as pd
import numpy as np
import io
import json

try:
    import openpyxl  # noqa: F401

    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("[skip] openpyxl not installed — pip install openpyxl")

np.random.seed(42)

# =============================================================================
# 1. CREATE SAMPLE DATA
# =============================================================================

df = pd.DataFrame(
    {
        "id": range(1, 101),
        "name": [f"User_{i}" for i in range(1, 101)],
        "email": [f"user{i}@example.com" for i in range(1, 101)],
        "age": np.random.randint(18, 70, 100),
        "salary": np.random.randint(30000, 150000, 100),
        "department": np.random.choice(["Eng", "Sales", "HR", "Marketing", "Finance"], 100),
        "join_date": pd.date_range("2020-01-01", periods=100, freq="W"),
        "is_active": np.random.choice([True, False], 100, p=[0.8, 0.2]),
        "score": np.random.uniform(1.0, 5.0, 100).round(2),
    }
)

print("Sample DataFrame:")
print(df.head())
print(f"Shape: {df.shape}")
print()

# =============================================================================
# 2. CSV
# =============================================================================

print("=" * 60)
print("2. CSV")
print("=" * 60)

# Write to string buffer
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)
csv_content = csv_buffer.getvalue()
print("First 200 chars of CSV:")
print(csv_content[:200])
print("...")
print()

# Read from string
df_csv = pd.read_csv(io.StringIO(csv_content))
print(f"Read CSV shape: {df_csv.shape}")
print()

# Key CSV options
print("KEY CSV OPTIONS:")
print("""
read_csv:
  - sep/delimiter: delimiter character (default ',')
  - header: row number for header (default 0), None for no header
  - names: column names if no header
  - index_col: column to use as index
  - usecols: list of columns to read
  - dtype: dict of column -> dtype
  - parse_dates: parse date columns
  - date_parser: custom date parser
  - na_values: additional strings to recognize as NaN
  - keep_default_na: whether to include default NaN values
  - chunksize: read in chunks (returns iterator)
  - nrows: number of rows to read
  - skiprows: rows to skip
  - encoding: file encoding (e.g., 'utf-8', 'latin1')
  - compression: 'gzip', 'bz2', 'zip', 'xz'
  - on_bad_lines: 'error', 'warn', 'skip'

to_csv:
  - index: write row index (default True)
  - header: write column names (default True)
  - sep: delimiter
  - na_rep: string for NaN (default '')
  - float_format: format for floats
  - columns: columns to write
  - mode: 'w' or 'a' (append)
  - compression: compression type
  - quoting: csv.QUOTE_MINIMAL, etc.
""")

# Chunked reading example
print("Chunked reading:")
chunk_iter = pd.read_csv(io.StringIO(csv_content), chunksize=25)
chunk_list = []
for i, chunk in enumerate(chunk_iter):
    chunk_list.append(chunk)
    if i == 0:
        print(f"  Chunk {i}: {chunk.shape}")
print(f"  Total chunks: {len(chunk_list)}")
print()

# =============================================================================
# 3. JSON
# =============================================================================

print("=" * 60)
print("3. JSON")
print("=" * 60)

# Write JSON (different orientations)
json_str_records = df.to_json(orient="records", date_format="iso")
print("orient='records' (first 200 chars):")
print(json_str_records[:200])
print("...")
print()

json_str_split = df.to_json(orient="split")
print("orient='split' (first 200 chars):")
print(json_str_split[:200])
print("...")
print()

json_str_index = df.to_json(orient="index")
print("orient='index' (first 200 chars):")
print(json_str_index[:200])
print("...")
print()

# Read JSON (pandas 3 requires a file-like object for JSON strings)
df_json = pd.read_json(io.StringIO(json_str_records), orient="records")
print(f"Read JSON (records) shape: {df_json.shape}")
print()

# Read with date parsing
df_json_dates = pd.read_json(
    io.StringIO(json_str_records), orient="records", convert_dates=["join_date"]
)
print(f"Join date dtype: {df_json_dates['join_date'].dtype}")
print()

# JSON Lines (one record per line)
json_lines = df.to_json(orient="records", lines=True)
print("JSON Lines (first 2 lines):")
print("\n".join(json_lines.split("\n")[:2]))
print()

# =============================================================================
# 4. EXCEL
# =============================================================================

print("=" * 60)
print("4. EXCEL")
print("=" * 60)

if not HAS_OPENPYXL:
    print("[skip] openpyxl not installed — Excel section skipped (pip install openpyxl)")
else:
    # Write to BytesIO buffer
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Employees", index=False)
        # Multiple sheets
        df.head(20).to_excel(writer, sheet_name="Sample", index=False)
        # With formatting
        summary = df.groupby("department").agg({"salary": "mean", "age": "mean"}).round(2)
        summary.to_excel(writer, sheet_name="Summary")

    excel_data = excel_buffer.getvalue()
    print(f"Excel file size: {len(excel_data)} bytes")
    print()

    # Read Excel
    df_excel = pd.read_excel(io.BytesIO(excel_data), sheet_name="Employees")
    print(f"Read Excel shape: {df_excel.shape}")
    print()

    # Read specific sheet
    df_sample = pd.read_excel(io.BytesIO(excel_data), sheet_name="Sample")
    print(f"Sample sheet shape: {df_sample.shape}")
    print()

    # Read all sheets
    all_sheets = pd.read_excel(io.BytesIO(excel_data), sheet_name=None)
    print(f"All sheets: {list(all_sheets.keys())}")
    for name, sheet_df in all_sheets.items():
        print(f"  {name}: {sheet_df.shape}")
    print()

    print("KEY EXCEL OPTIONS:")
    print("""
read_excel:
  - sheet_name: str, int, list, or None (all sheets)
  - header: row number for header
  - usecols: columns to parse
  - dtype: column types
  - parse_dates: date columns
  - na_values: custom NaN values
  - engine: 'openpyxl' (xlsx), 'xlrd' (xls)

to_excel / ExcelWriter:
  - engine: 'openpyxl' (default), 'xlsxwriter'
  - index: write index
  - header: write header
  - startrow, startcol: offset
  - freeze_panes: freeze rows/cols
""")

# =============================================================================
# 5. PARQUET
# =============================================================================

print("=" * 60)
print("5. PARQUET (COLUMNAR, EFFICIENT)")
print("=" * 60)

# Write Parquet
parquet_buffer = io.BytesIO()
df.to_parquet(parquet_buffer, index=False)
parquet_data = parquet_buffer.getvalue()
print(f"Parquet size: {len(parquet_data)} bytes")
print(f"CSV size: {len(csv_content)} bytes")
print(f"Compression ratio: {len(csv_content) / len(parquet_data):.1f}x")
print()

# Read Parquet
df_parquet = pd.read_parquet(io.BytesIO(parquet_data))
print(f"Read Parquet shape: {df_parquet.shape}")
print(f"Dtypes preserved: {df_parquet.dtypes.tolist()}")
print()

# Partitioned Parquet
# NOTE: pyarrow cannot partition into a BytesIO file object ("Argument 'filesystem'
# has incorrect type ... got NoneType"); write to a real directory under output/
partition_dir = "output/parquet_partitioned/"
df.to_parquet(partition_dir, partition_cols=["department"], index=False)
print(f"Partitioned Parquet written to {partition_dir}")
print()

# Read with filters
df_filtered = pd.read_parquet(partition_dir, filters=[("department", "in", ["Eng", "Sales"])])
print(f"Filtered read (Eng, Sales): {df_filtered.shape}")
print()

print("KEY PARQUET OPTIONS:")
print("""
to_parquet:
  - engine: 'pyarrow' (default), 'fastparquet'
  - compression: 'snappy', 'gzip', 'brotli', 'lz4', 'zstd', None
  - partition_cols: list of columns for partitioning
  - index: write index

read_parquet:
  - engine: 'pyarrow', 'fastparquet'
  - columns: list of columns to read
  - filters: list of (col, op, val) for partition pruning
  - filesystem: pyarrow filesystem (for cloud storage)
""")

# =============================================================================
# 6. SQL
# =============================================================================

print("=" * 60)
print("6. SQL DATABASES")
print("=" * 60)

# Using SQLite (built-in)
import sqlite3

# Create in-memory database
conn = sqlite3.connect(":memory:")

# Write DataFrame to SQL
df.to_sql("employees", conn, index=False, if_exists="replace")

# Read from SQL
df_sql = pd.read_sql('SELECT * FROM employees WHERE department = "Eng"', conn)
print(f"SQL query result: {df_sql.shape}")
print()

# Read with chunks
chunk_iter = pd.read_sql("SELECT * FROM employees", conn, chunksize=30)
sql_chunks = list(chunk_iter)
print(f"SQL chunks: {len(sql_chunks)} chunks of ~30 rows")
print()

# Parameterized query
dept = "Sales"
df_param = pd.read_sql("SELECT * FROM employees WHERE department = ?", conn, params=[dept])
print(f"Parameterized query (Sales): {df_param.shape}")
print()

# Write with dtype specification
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Boolean

engine = create_engine("sqlite:///:memory:")

df.to_sql(
    "employees_typed",
    engine,
    index=False,
    if_exists="replace",
    dtype={
        "id": Integer(),
        "name": String(50),
        "email": String(100),
        "age": Integer(),
        "salary": Integer(),
        "department": String(20),
        "join_date": DateTime(),
        "is_active": Boolean(),
        "score": Float(),
    },
)

print("KEY SQL OPTIONS:")
print("""
read_sql / read_sql_query / read_sql_table:
  - con: SQLAlchemy engine or DBAPI connection
  - sql: SQL query or table name
  - index_col: column(s) to set as index
  - coerce_float: convert to float
  - params: parameters for parameterized query
  - parse_dates: date columns
  - chunksize: return iterator

to_sql:
  - con: engine or connection
  - name: table name
  - if_exists: 'fail', 'replace', 'append'
  - index: write index
  - dtype: dict of column -> SQLAlchemy type
  - method: 'multi' for batch inserts
  - chunksize: batch size
""")

# =============================================================================
# 7. HTML
# =============================================================================

print("=" * 60)
print("7. HTML TABLES")
print("=" * 60)

# Sample HTML
html_content = """
<table>
  <thead>
    <tr><th>Name</th><th>Age</th><th>City</th></tr>
  </thead>
  <tbody>
    <tr><td>Alice</td><td>30</td><td>NYC</td></tr>
    <tr><td>Bob</td><td>25</td><td>LA</td></tr>
    <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
  </tbody>
</table>
"""

# Read HTML tables (pandas 3 requires a file-like object for HTML strings)
tables = pd.read_html(io.StringIO(html_content))
print(f"Number of tables found: {len(tables)}")
print(tables[0])
print()

# Write HTML
html_output = df.head(10).to_html(index=False, classes="table table-striped", border=0)
print("HTML output (first 300 chars):")
print(html_output[:300])
print("...")
print()

print("KEY HTML OPTIONS:")
print("""
read_html:
  - io: URL, file path, or string
  - match: regex to match table text
  - flavor: 'lxml', 'html5lib', 'bs4'
  - header: header row
  - index_col: index column
  - parse_dates: parse dates
  - thousands: thousands separator
  - decimal: decimal point

to_html:
  - classes: CSS classes
  - border: border width
  - index: include index
  - header: include header
  - na_rep: NaN representation
  - float_format: float formatter
  - justify: left/right/center
""")

# =============================================================================
# 8. OTHER FORMATS
# =============================================================================

print("=" * 60)
print("8. OTHER FORMATS")
print("=" * 60)

# Feather (fast, interoperable)
try:
    feather_buffer = io.BytesIO()
    df.to_feather(feather_buffer)
    print(f"Feather size: {len(feather_buffer.getvalue())} bytes")
    df_feather = pd.read_feather(io.BytesIO(feather_buffer.getvalue()))
    print(f"Read Feather: {df_feather.shape}")
except Exception as e:
    print(f"Feather not available: {e}")
print()

# Pickle (Python native, preserves everything)
pickle_buffer = io.BytesIO()
df.to_pickle(pickle_buffer)
print(f"Pickle size: {len(pickle_buffer.getvalue())} bytes")
df_pickle = pd.read_pickle(io.BytesIO(pickle_buffer.getvalue()))
print(f"Read Pickle: {df_pickle.shape}")
print()

# Stata
try:
    stata_buffer = io.BytesIO()
    df.to_stata(stata_buffer, write_index=False)
    print(f"Stata size: {len(stata_buffer.getvalue())} bytes")
except Exception as e:
    print(f"Stata not available: {e}")
print()

# HDF5
try:
    hdf_buffer = io.BytesIO()
    df.to_hdf(hdf_buffer, key="data", mode="w")
    print(f"HDF5 size: {len(hdf_buffer.getvalue())} bytes")
except Exception as e:
    print(f"HDF5 not available: {e}")
print()

# =============================================================================
# 9. PERFORMANCE COMPARISON
# =============================================================================

print("=" * 60)
print("9. PERFORMANCE COMPARISON")
print("=" * 60)

import time
import os

# Larger DataFrame for testing
large_df = pd.DataFrame(
    {
        "id": range(100000),
        "value1": np.random.randn(100000),
        "value2": np.random.randn(100000),
        "category": np.random.choice(["A", "B", "C", "D", "E"], 100000),
        "date": pd.date_range("2020-01-01", periods=100000, freq="min"),
    }
)

formats = {}

# CSV
start = time.time()
csv_buf = io.StringIO()
large_df.to_csv(csv_buf, index=False)
formats["CSV_write"] = time.time() - start

start = time.time()
pd.read_csv(io.StringIO(csv_buf.getvalue()))
formats["CSV_read"] = time.time() - start

# Parquet
start = time.time()
pq_buf = io.BytesIO()
large_df.to_parquet(pq_buf, index=False)
formats["Parquet_write"] = time.time() - start

start = time.time()
pd.read_parquet(io.BytesIO(pq_buf.getvalue()))
formats["Parquet_read"] = time.time() - start

# Feather
try:
    start = time.time()
    feather_buf = io.BytesIO()
    large_df.to_feather(feather_buf)
    formats["Feather_write"] = time.time() - start

    start = time.time()
    pd.read_feather(io.BytesIO(feather_buf.getvalue()))
    formats["Feather_read"] = time.time() - start
except:
    formats["Feather_write"] = "N/A"
    formats["Feather_read"] = "N/A"

# Pickle
start = time.time()
pickle_buf = io.BytesIO()
large_df.to_pickle(pickle_buf)
formats["Pickle_write"] = time.time() - start

start = time.time()
pd.read_pickle(io.BytesIO(pickle_buf.getvalue()))
formats["Pickle_read"] = time.time() - start

print("Performance (100k rows, 5 cols):")
for k, v in formats.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}s")
    else:
        print(f"  {k}: {v}")

print("\nRECOMMENDATIONS:")
print("  - Parquet: Best for analytics, columnar, compression")
print("  - Feather: Fastest read/write, good for interop")
print("  - CSV: Universal, human-readable, slow for large data")
print("  - Pickle: Python-only, preserves everything, not secure")
print("  - SQL: For querying, sharing, concurrent access")

print("\n" + "=" * 60)
print("END OF I/O")
print("=" * 60)
