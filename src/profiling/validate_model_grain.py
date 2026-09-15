# %%
from pathlib import Path

import pandas as pd
# %%
DATA_PATH = Path("C:/Users/d.dorvash/Dourvash Projects/sms_gateway/sms-gateway-analytics/data/raw/sms-call-internet-mi-2013-11-01.txt")


# %%
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


duplicate_count = 0
seen_keys = set()



# %%
for chunk in pd.read_csv(
    DATA_PATH,
    sep="\t",
    header=None,
    names=COLUMNS,
    chunksize=CHUNK_SIZE,
):

    keys = zip(
        chunk["square_id"],
        chunk["time_interval"],
        chunk["country_code"],
    )

    for key in keys:
        if key in seen_keys:
            duplicate_count += 1
        else:
            seen_keys.add(key)



# %%
print(f"Duplicate grain records: {duplicate_count}")
# %%
