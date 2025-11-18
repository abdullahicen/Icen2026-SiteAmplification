This program computes period-dependent site amplification factors using the ICEN (2026) regional model for Türkiye. The user only needs to provide Vs30, Latitude, Longitude, and rock PSA (PSAr). The code automatically finds the correct region based on coordinates and applies the appropriate regional amplification model.

REQUIRED FILES AND FOLDER STRUCTURE

Place all files in the following structure:

…\Codes
main.py
Icen2026.py
Periods.txt
Input.xlsx
Coefficients
Icen_coeffs.txt
Coordinates
Coordinates.xlsx

Do NOT change file and folder names.

PURPOSE OF EACH FILE

main.py
- Main driver script.
- Reads Input.xlsx and Periods.txt.
- Finds region from coordinates.
- Computes amplification for all periods.
- Writes Output.xlsx.

Icen2026.py
- Contains all model formulas and region logic.
- Reads coefficients from Icen_coeffs.txt.
- Reads region boundaries from Coordinates.xlsx.
- Determines the correct regional model from latitude/longitude.
- Computes amplification.

Periods.txt
- List of periods (one per line).
- Example: -1, 0, 0.01, 0.02, …, 10.

Input.xlsx
- User input file.
- The user inserts coordinates here.
- Required columns:
Station
Vs30
Latitude
Longitude
PSAr

Output.xlsx
- Automatically created.
- Contains all input columns plus one column for each period.

Icen_coeffs.txt
- Final coefficient table for the ICEN (2026) model.
- Includes c1, regional Δc1 terms, c2, c3, c4, V1, Vc.

Coordinates.xlsx
- Contains polygon boundaries for each region in WKT format.
- Valid region names:
Coastal Aegean
Marmara
Aegean
East

HOW REGION SELECTION WORKS

You only enter Latitude and Longitude in Input.xlsx.

The program:
- Reads polygon boundaries from Coordinates.xlsx.
- Checks which polygon contains the coordinate.
- Automatically assigns one of the four models:
Coastal Aegea
Marmara
Aegea
East
- No manual selection is required.

If a point is outside all polygons:
- Region = None
- Amplification = NaN

HOW AMPLIFICATION IS COMPUTED

For each period:
- Linear term: (c1 + Δc1_region) * ln(V* / 760)
- Nonlinear term: c2 * (exp(c3*(min(Vs30,760)–360)) – exp(c3*400))
* ln((PSAr + c4) / c4)
- Total amplification: exp(linear + nonlinear)

Coefficients come from Icen_coeffs.txt.
Region comes from the coordinate.

HOW TO RUN THE PROGRAM

Open a terminal in the Codes folder and run:

python main.py


The program:
- Loads periods
- Loads all stations from Input.xlsx
- Determines region for each station
- Computes amplification for all periods
- Saves Output.xlsx in the same folder

WHAT THE USER MUST DO

Open Input.xlsx

Enter Station, Vs30, Latitude, Longitude, PSAr

Save Input.xlsx

Run main.py

Read results in Output.xlsx

Nothing else is required.