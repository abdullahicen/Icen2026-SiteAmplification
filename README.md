Icen2026 – Regional Site Amplification Model for Türkiye
<p align="center"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />  <img src="https://img.shields.io/badge/Model-Icen2026-black.svg" /> <img src="https://img.shields.io/badge/Regions-Marmara%20%7C%20Aegean%20%7C%20Coastal%20Aegean%20%7C%20East-blueviolet.svg" /> <img src="https://img.shields.io/badge/Geo-Polygon%20Region%20Mapping-success.svg" /> </p>

This repository provides the full implementation of the Icen (2026) regional, period-dependent site amplification model for Türkiye.
The model automatically selects the correct region (Marmara, Aegean, Coastal Aegean, East) based on geographic coordinates and computes nonlinear + linear amplification for all periods

Icen2026-SiteAmplification/
│
├── main.py                # Main script (runs model and writes Output.xlsx)
├── Icen2026.py            # Region selection + amplification equations
├── Periods.txt            # Spectral periods (one per line)
├── PSAr.txt               # Rock PSA values per period (same length as Periods.txt)
├── Input.xlsx             # User input: Station, Vs30, Latitude, Longitude
├── Output.xlsx            # Auto-generated results
│
└── Coefficients/
    ├── Icen_coeffs.txt
    └── Coordinates/
         └── Coordinates.xlsx   # Region polygons in WKT format

Coefficients/Coordinates/Coordinates.xlsx
