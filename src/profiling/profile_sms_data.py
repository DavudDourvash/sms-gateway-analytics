from pathlib import Path

import pandas as pd


# =========================
# Configuration
# =========================

DATA_PATH = Path#%%
# =========================
# Configuration
# =========================

DATA_PATH = Path("C:/Users/d.dorvash/Dourvash Projects/"
                 "sms_gateway/sms-gateway-analytics/data/raw/"
                 "sms-call-internet-mi-2013-11-01.txt")

COLUMNS = [
    "square_id",
    "time_interval",
    "country_code",
    "sms_in",
    "sms_out",
    "call_in",
    "call_out",
    "internet",
]



CHUNK_SIZE = 100_000

COLUMNS = [
    "square_id",
    "time_interval",
    "country_code",
    "sms_in",
    "sms_out",
    "call_in",
    "call_out",
    "internet",
]


# =========================
# Profiling
# =========================

total_rows = 0

null_counts = pd.Series(0, index=COLUMNS, dtype="int64")

unique_squares = set()
unique_countries = set()

min_time = None
max_time = None

duplicate_keys = set()
duplicate_count = 0

sms_in_values = []
sms_out_values = []


# =========================
# Read data in chunks
# =========================

for chunk in pd.read_csv(
    DATA_PATH,
    sep="\t",
    header=None,
    names=COLUMNS,
    chunksize=CHUNK_SIZE,
):

    total_rows += len(chunk)

    # Missing values
    null_counts += chunk.isna().sum()

    # Cardinality
    unique_squares.update(chunk["square_id"].dropna().unique())
    unique_countries.update(chunk["country_code"].dropna().unique())

    # Time range
    chunk_min_time = chunk["time_interval"].min()
    chunk_max_time = chunk["time_interval"].max()

    if min_time is None or chunk_min_time < min_time:
        min_time = chunk_min_time

    if max_time is None or chunk_max_time > max_time:
        max_time = chunk_max_time

    # SMS values
    sms_in_values.extend(
        chunk["sms_in"].dropna().tolist()
    )

    sms_out_values.extend(
        chunk["sms_out"].dropna().tolist()
    )

    # Duplicate logical keys
    keys = list(
        zip(
            chunk["square_id"],
            chunk["time_interval"],
            chunk["country_code"],
        )
    )

    for key in keys:
        if key in duplicate_keys:
            duplicate_count += 1
        else:
            duplicate_keys.add(key)


# =========================
# Results
# =========================

print("\n=== FULL FILE PROFILE ===")

print("\nTotal rows:")
print(total_rows)

print("\n=== NULL COUNTS ===")
print(null_counts)

print("\n=== UNIQUE VALUES ===")
print("Unique squares:", len(unique_squares))
print("Unique countries:", len(unique_countries))

print("\n=== TIME RANGE ===")
print("Min timestamp:", min_time)
print("Max timestamp:", max_time)

print("\n=== SMS SUMMARY ===")

sms_summary = pd.DataFrame(
    {
        "sms_in": pd.Series(sms_in_values),
        "sms_out": pd.Series(sms_out_values),
    }
).describe()

print(sms_summary)

print("\n=== DUPLICATES ===")
print("Duplicate logical records:", duplicate_count)