import pandas as pd
import numpy as np

hpc_path = "data/hpc_hno_2025.csv"
summary_path = "data/country_level_summary (1).csv"

# Skip the HXL tag row (row index 1) by reading and dropping it
hpc_raw = pd.read_csv(hpc_path, dtype=str, keep_default_na=False)
hpc_raw = hpc_raw.drop(index=0).reset_index(drop=True)  # drop HXL row

# Normalise column names
hpc_raw.columns = hpc_raw.columns.str.strip()

# Filter: Cluster == "ALL" and Category is blank/NaN
mask = (hpc_raw["Cluster"] == "ALL") & (hpc_raw["Category"].str.strip() == "")
filtered = hpc_raw[mask].copy()

# Keep first occurrence per country
first_per_country = filtered.drop_duplicates(subset=["Country ISO3"], keep="first")

# Cast In Need / Targeted to numeric
first_per_country["In Need"] = pd.to_numeric(first_per_country["In Need"], errors="coerce")
first_per_country["Targeted"] = pd.to_numeric(first_per_country["Targeted"], errors="coerce")

lookup = first_per_country.set_index("Country ISO3")[["In Need", "Targeted"]]

print("Lookup values extracted from hpc_hno_2025.csv:")
print(lookup.to_string())

# Load summary file
summary = pd.read_csv(summary_path)

# Overwrite In Need and Targeted from lookup
summary["In Need"] = summary["Country ISO3"].map(lookup["In Need"])
summary["Targeted"] = summary["Country ISO3"].map(lookup["Targeted"])

# Write back to the same file
summary.to_csv(summary_path, index=False)

print("\nUpdated country_level_summary (1).csv:")
print(summary[["Country ISO3", "In Need", "Targeted"]].to_string(index=False))
print("\nDone — file overwritten successfully.")
