# -*- coding: utf-8 -*-
"""
Site amplification models for Türkiye with automatic region selection.

Folder structure (relative to this script):

    <BASE_DIR>/
        site_amp_main.py              (this file)
        Coefficients/
            Icen_coeffs.txt
            Coordinates/
                Coordinates.xlsx

Coordinates.xlsx structure (current):

    Columns:
        wkt_geom : polygon in WKT format
        fid      : 'Coastal Aegean', 'Marmara', 'Aegean', 'East'

Mapping used here:
    fid = 'Coastal Aegean' -> region 'Coastal_Aegean', model 'Coastal Aegean'
    fid = 'Marmara'        -> region 'Marmara',        model 'Marmara'
    fid = 'Aegean'         -> region 'Aegean',         model 'Aegean'
    fid = 'East'           -> region 'East',           model 'East'

Available models (Icen, 2025):
    'Marmara', 'Coastal Aegean', 'Aegean', 'East'
"""

import os
import pandas as pd
import numpy as np

from shapely.geometry import Point
from shapely import wkt

# ============================================================
#  BASE DIRECTORY & FILE PATHS
# ============================================================

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback for interactive runs (e.g., in an interpreter)
    BASE_DIR = os.getcwd()

COEFF_FILE = os.path.join(BASE_DIR, "Coefficients", "Icen_coeffs.txt")
COORDS_FILE = os.path.join(BASE_DIR, "Coefficients", "Coordinates", "Coordinates.xlsx")

def load_coefficients_interpolated(model: str, periods):
    """
    Load Icen (2025) coefficients from Icen_coeffs.txt and interpolate
    to requested periods.

    The file columns (from your final version) are:

        Period, c1,
        Δc1,Marmara, Δc1,Coastal Aegean, Δc1,Aegean, (Δc1,East),
        c2, c3, c4, VC, V1, Standard Deviation

    We rename them to simpler names once and interpolate all numeric
    columns except 'Period'.
    """
    if not os.path.isfile(COEFF_FILE):
        raise FileNotFoundError(f"Coefficient file not found:\n  {COEFF_FILE}")

    df = pd.read_csv(COEFF_FILE, sep=r"\s+")
    df = df.sort_values("Period")

    # Rename columns by position so we don’t fight with Δ / commas etc.
    cols = df.columns.tolist()
    # Expected order from the file:
    # 0: Period
    # 1: c1
    # 2: Δc1,Marmara
    # 3: Δc1,Coastal Aegean
    # 4: Δc1,Aegean
    # 5: Δc1,East 
    # 6: c2
    # 7: c3
    # 8: c4
    # 9: VC
    # 10: V1
    # 11: Sigma
    if len(cols) != 12:
        raise ValueError(
            f"Unexpected number of columns in Icen_coeffs.txt: {len(cols)} "
            f"(expected 12). Got: {cols}"
        )

    cols[2] = "d_c1_Marmara"
    cols[3] = "d_c1_Coastal"
    cols[4] = "d_c1_Aegean"
    cols[5] = "d_c1_East"
    cols[6] = "c2"
    cols[7] = "c3"
    cols[8] = "c4"
    cols[9] = "Vc"
    cols[10] = "V1"
    cols[11] = "sigma"

    df.columns = cols

    result = []
    for p in periods:
        if p in df["Period"].values:
            row = df[df["Period"] == p].iloc[0].to_dict()
        else:
            # Interpolate all numeric columns except 'Period'
            row = {"Period": p}
            for col in df.columns:
                if col == "Period":
                    continue
                row[col] = np.interp(p, df["Period"], df[col])
        result.append(row)

    return result


# ============================================================
#  fid -> REGION / MODEL MAPPING
# ============================================================

FID_TO_REGION = {
    "Coastal Aegean": "Coastal_Aegean",
    "Marmara":        "Marmara",
    "Aegean":         "Aegean",
    "East":           "East",
}

FID_TO_MODEL = {
    "Coastal Aegean": "Coastal Aegea",  # NOTE: Aegean (your model name)
    "Marmara":        "Marmara",
    "Aegean":         "Aegea",          # NOTE: Aegean (your model name)
    "East":           "East",
}


# ============================================================
#  LOAD REGIONS (POLYGONS) FROM COORDINATES.XLSX
# ============================================================

def load_regions_from_excel(excel_path: str):
    """
    Read region polygons from Coordinates.xlsx.

    Expected columns (case-insensitive):
        wkt_geom : WKT polygon string
        fid      : 'Coastal Aegean', 'Marmara', 'Aegean', 'East'

    Returns
    -------
    regions : list of dicts with keys:
        'fid', 'region_name', 'model', 'polygon'
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Coordinates file not found:\n  {excel_path}")

    # Read first sheet (your file uses a simple single sheet)
    df = pd.read_excel(excel_path, sheet_name=0)

    # Normalize column names
    cols_lower = {c.lower(): c for c in df.columns}

    if "wkt_geom" not in cols_lower or "fid" not in cols_lower:
        raise ValueError(
            f"Coordinates.xlsx must have 'wkt_geom' and 'fid' columns "
            f"(case-insensitive). Current columns: {list(df.columns)}"
        )

    wkt_col = cols_lower["wkt_geom"]
    fid_col = cols_lower["fid"]

    regions = []
    for _, row in df.iterrows():
        fid_val = str(row[fid_col]).strip()
        wkt_str = str(row[wkt_col])

        if not wkt_str.strip():
            continue  # skip empty geometries

        if fid_val not in FID_TO_REGION or fid_val not in FID_TO_MODEL:
            raise ValueError(
                f"fid='{fid_val}' not found in FID_TO_REGION/FID_TO_MODEL mapping. "
                f"Update FID_TO_REGION / FID_TO_MODEL in this script."
            )

        region_name = FID_TO_REGION[fid_val]
        model_name = FID_TO_MODEL[fid_val]
        poly = wkt.loads(wkt_str)

        regions.append(
            {
                "fid": fid_val,
                "region_name": region_name,
                "model": model_name,
                "polygon": poly,
            }
        )

    if not regions:
        raise ValueError("No valid regions found in Coordinates.xlsx.")

    return regions


# Load regions once
REGIONS = load_regions_from_excel(COORDS_FILE)


def find_region_for_point(lat: float, lon: float):
    """
    Given latitude and longitude, return the region dict that contains the point.

    Returns
    -------
    region_dict or None
        region_dict keys: 'fid', 'region_name', 'model', 'polygon'.
        Returns None if the point is not inside any region.
    """
    pt = Point(lon, lat)  # shapely uses (x, y) = (lon, lat)
    for region in REGIONS:
        poly = region["polygon"]
        # include boundary as well
        if poly.contains(pt) or poly.touches(pt):
            return region
    return None


def get_model_for_coordinate(lat: float, lon: float):
    """
    Return model name (e.g. 'Marmara', 'Coastal Aegean', 'Aegean', 'East')
    for a given coordinate, or None if outside all regions.
    """
    region = find_region_for_point(lat, lon)
    if region is None:
        return None
    return region["model"]


# ============================================================
#  LOAD COEFFICIENTS & SITE AMPLIFICATION FORMULAS
# ============================================================

def compute_site_amplification(Vs30, PSAr_list, model: str, periods,
                               V1: float = 150.0, Vc: float = 800.0):
    """
    Compute site amplification using the final Icen (2025) model,
    allowing PSAr to be period-dependent.

        c1,r = c1 + Δc1,r
        f_linear = c1,r * ln(V*/Vref)
        f_nonlinear = c2 [exp(c3(min(Vs30,760)-360)) - exp(c3*400)]
                      * ln((PSAr(T) + c4)/c4)

        ln(Amp) = f_linear + f_nonlinear

    Parameters
    ----------
    Vs30 : float or array-like
        Time-averaged shear-wave velocity in top 30 m.
    PSAr_list : list or array-like
        Rock/reference PSA values for EACH period.
        Must have same length as 'periods'.
    model : str
        One of 'Marmara', 'Coastal Aegean', 'Aegean', 'East'.
    periods : list or array-like
        Periods (s) for which coefficients are needed.
    V1, Vc : float
        Defaults; per-period values in the file override these.

    Returns
    -------
    amps : ndarray, shape (n_periods, n_Vs30)
    """
    Vs30 = np.array(Vs30, ndmin=1)
    Vref = 760.0
    periods = list(periods)
    PSAr_arr = np.array(PSAr_list, dtype=float)

    if len(PSAr_arr) != len(periods):
        raise ValueError(
            f"Length of PSAr_list ({len(PSAr_arr)}) must match "
            f"length of periods ({len(periods)})."
        )

    results = []

    # Choose which Δc1 column to use for each model
    dcol_map = {
        "Marmara":        "d_c1_Marmara",
        "Coastal Aegean": "d_c1_Coastal",
        "Aegean":         "d_c1_Aegean",
        "East":           "d_c1_East",
    }
    if model not in dcol_map:
        raise ValueError(
            "Model must be 'Marmara', 'Coastal Aegean', 'Aegean', or 'East'. "
            f"Got: {model}"
        )
    dcol = dcol_map[model]

    coeff_list = load_coefficients_interpolated(model, periods)

    # Loop over periods and corresponding PSAr
    for i, (coeffs, PSAr_T) in enumerate(zip(coeff_list, PSAr_arr)):
        # Per-period hinge velocities and nonlinear parameters
        V1_p = float(coeffs.get("V1", V1))
        Vc_p = float(coeffs.get("Vc", Vc))
        c1 = float(coeffs["c1"])
        d_c1 = float(coeffs[dcol])
        c1_r = c1 + d_c1

        c2 = float(coeffs["c2"])
        c3 = float(coeffs["c3"])
        c4 = float(coeffs["c4"])

        if c4 <= 0:
            raise ValueError(f"c4 must be > 0, got c4={c4}")

        # ---------- f_linear ----------
        VN = np.where(
            Vs30 < V1_p,
            np.log(V1_p / Vref),
            np.where(
                Vs30 <= Vc_p,
                np.log(Vs30 / Vref),
                np.log(Vc_p / Vref),
            ),
        )
        f_linear = c1_r * VN

        # ---------- f_nonlinear ----------
        Vs_min = np.minimum(Vs30, 760.0)
        nonlinear_shape = np.exp(c3 * (Vs_min - 360.0)) - np.exp(c3 * 400.0)
        f_nonlinear = c2 * nonlinear_shape * np.log((PSAr_T + c4) / c4)

        ln_amp = f_linear + f_nonlinear
        Amp = np.exp(ln_amp)

        results.append(Amp)

    return np.array(results)  # (n_periods, n_Vs30)
