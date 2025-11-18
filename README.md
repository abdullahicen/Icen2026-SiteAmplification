Icen2026 – Regional Site Amplification Model for Türkiye
<p align="center"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />  <img src="https://img.shields.io/badge/Model-Icen2026-black.svg" /> <img src="https://img.shields.io/badge/Regions-Marmara%20%7C%20Aegean%20%7C%20Coastal%20Aegean%20%7C%20East-blueviolet.svg" /> <img src="https://img.shields.io/badge/Geo-Polygon%20Region%20Mapping-success.svg" /> </p>

This repository provides the complete implementation of the Icen (2026) regional, period-dependent site amplification model for Türkiye.
The framework includes automatic region detection, period interpolation, and nonlinear site response scaling using calibrated regional coefficients.

📍 Overview

The model assigns each site to one of the four tectonically consistent regions:

Marmara

Aegean

Coastal Aegean

East Türkiye

Region boundaries are stored as polygons in:

Coefficients/Coordinates/Coordinates.xlsx

📁 Repository Structure
Icen2026-SiteAmplification/
│
├── main.py                 # Main driver script
├── Icen2026.py             # Region mapping + amplification functions
├── Input.xlsx              # Station, Vs30, Latitude, Longitude
├── Periods.txt             # List of spectral periods
├── PSAr.txt                # Reference PSA values (same length/order as Periods.txt)
├── Output.xlsx             # Generated output
│
└── Coefficients/
    ├── Icen_coeffs.txt     # Period-dependent model coefficients
    └── Coordinates/
         └── Coordinates.xlsx   # Region polygons (WKT)

🔧 How the Model Works

For each site:

Determine region using geographic coordinates and polygon boundaries.

Load period-dependent coefficients from Icen_coeffs.txt.

Interpolate coefficients if the requested period is not explicitly tabulated.

Compute linear term using Vs* and hinge velocities (V1, Vc).

Compute nonlinear term using reference rock PSA (PSAr.txt).

Output amplification factors for all periods.

📥 Input Requirements
Input.xlsx

Required columns:

Station	Vs30	Latitude	Longitude
Periods.txt

One period (s) per line

Must match the periods used in your analyses

PSAr.txt

PSA_r(T) values

Must be the same length and order as Periods.txt

📤 Output

The script generates:

Output.xlsx


which contains:

Original input columns

Amplification factors for each period

Columns are added in the order of Periods.txt.

▶️ Running the Code

Install required Python packages:

numpy
pandas
shapely
openpyxl


Run the model:

python main.py

📚 Citation

If you use this model in research or engineering studies, please cite:

Icen, A. (2026). Regional Site Amplification Model for Türkiye.
