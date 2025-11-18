# -*- coding: utf-8 -*-
"""
main.py
-------
Reads:
    - Periods.txt      : list of periods (-1, 0, 0.01, ..., 10)
    - Input.xlsx       : Station, Vs30, Latitude, Longitude, PSAr
Uses:
    - Icen2026.py      : region selection + site amplification model

Writes:
    - Output.xlsx      : same first 5 columns + amplification for each period

Folder structure (example):

    C:\Rock Site Amplification\Revision\Codes\
        main.py
        Icen2026.py
        Periods.txt
        Input.xlsx
        Coefficients\
            Icen_coeffs.txt
            Coordinates\
                Coordinates.xlsx
"""

import os
import numpy as np
import pandas as pd

from Icen2026 import get_model_for_coordinate, compute_site_amplification


# ============================================================
#  PATHS
# ============================================================

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

PERIODS_FILE = os.path.join(BASE_DIR, "Periods.txt")
INPUT_FILE   = os.path.join(BASE_DIR, "Input.xlsx")
OUTPUT_FILE  = os.path.join(BASE_DIR, "Output.xlsx")


# ============================================================
#  LOAD PERIODS
# ============================================================

def load_periods(path):
    """Read periods from Periods.txt as floats (one value per line)."""
    periods = []
    with open(path, "r") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            periods.append(float(s))
    return periods


# ============================================================
#  MAIN WORKFLOW
# ============================================================

def main():
    # 1) Load periods
    periods = load_periods(PERIODS_FILE)
    # Example: [-1.0, 0.0, 0.01, ..., 10.0] :contentReference[oaicite:1]{index=1}

    # 2) Load input sites
    df_in = pd.read_excel(INPUT_FILE)

    # Expected columns in Input.xlsx
    required_cols = ["Station", "Vs30", "Latitude", "Longitude", "PSAr"]
    missing = [c for c in required_cols if c not in df_in.columns]
    if missing:
        raise ValueError(
            f"Input.xlsx is missing required columns: {missing}. "
            f"Found columns: {list(df_in.columns)}"
        )

    # 3) Loop over sites and compute amplification
    amp_rows = []  # list of [amp(T1), amp(T2), ...] for each row
    model_list = []  # optional: keep track of which model was used per site

    for idx, row in df_in.iterrows():
        station = row["Station"]
        vs30    = float(row["Vs30"])
        lat     = float(row["Latitude"])
        lon     = float(row["Longitude"])
        psar    = float(row["PSAr"])  # PSA at rock / reference

        # Determine model based on coordinate
        model_name = get_model_for_coordinate(lat, lon)
        model_list.append(model_name)

        if model_name is None:
            print(
                f"[WARN] Station {station}: "
                f"(lat={lat}, lon={lon}) outside all regions. "
                "Amplification set to NaN."
            )
            amp_vals = [np.nan] * len(periods)
        else:
            # Compute site amplification for this site
            # Vs30 is scalar -> result shape (n_periods, 1)
            amps = compute_site_amplification(
                Vs30=vs30,
                PGA_ref=psar,
                model=model_name,
                periods=periods,
            )
            amp_vals = amps[:, 0].tolist()

            print(
                f"Station {station}: model={model_name}, "
                f"Vs30={vs30}, PSAr={psar}"
            )

        amp_rows.append(amp_vals)

    # 4) Build amplification DataFrame with period columns
    #    Use numeric column names (float) like in your Output.xlsx
    amp_df = pd.DataFrame(amp_rows, columns=periods)

    # 5) Combine input columns + amplification columns
    #    If you also want the model name in output, uncomment the line below.
    # df_out = pd.concat([df_in, pd.Series(model_list, name="Model"), amp_df], axis=1)
    df_out = pd.concat([df_in, amp_df], axis=1)

    # 6) Save to Output.xlsx
    df_out.to_excel(OUTPUT_FILE, index=False)
    print(f"\nSaved results to:\n  {OUTPUT_FILE}")


# ============================================================
#  RUN
# ============================================================

if __name__ == "__main__":
    main()
