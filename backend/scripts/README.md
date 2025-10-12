# GHG Data Import Scripts

## Overview

This directory contains scripts for importing real-world emissions data from the GHG Sheet.xlsx file into the PostgreSQL database.

## Prerequisites

1. **Install required packages:**

   ```bash
   pip install pandas openpyxl
   ```

2. **Ensure GHG Sheet.xlsx is in the project root directory**

3. **Database must be running:**
   ```bash
   docker-compose up -d db
   ```

## Usage

### Import GHG Data

Run the import script from the backend directory:

```bash
cd backend
python scripts/import_ghg_data.py
```

### What the Script Does

1. **Clears existing sample data** from the database
2. **Reads GHG Sheet.xlsx** with three sheets:

   - Scope 1: Direct emissions (123+ records)
   - Scope 2: Indirect energy emissions (18+ records)
   - Scope 3: Value chain emissions (30+ records)

3. **Creates emission factors** from unique combinations of:

   - Activity name (material/energy type)
   - Emission factor value
   - Unit of measurement

4. **Creates emission records** linked to the appropriate factors with:

   - Activity date (parsed from quarters/months)
   - Activity value (quantity consumed)
   - Calculated CO2e emissions
   - Location and department information

5. **Maintains historical accuracy** by:
   - Creating versioned emission factors
   - Linking records to specific factor versions
   - Preserving immutable historical data

## Data Transformation

### Scope 1 (Direct Emissions)

- **Source:** Materials like Coal, Diesel, Natural Gas, etc.
- **Quarters:** Q1, Q2 → Converted to dates (Q1 = Jan 31, Q2 = Apr 30)
- **Units:** Converted from tCO2 to kgCO2e (multiply by 1000)
- **Location:** Central Steel Plant
- **Sections:** Pellet Plant, DRI, SMS, Rolling Mill, etc.

### Scope 2 (Indirect Energy)

- **Source:** Purchased Electricity, Imported Steam
- **Quarters:** Q1, Q2, Q3 → Converted to dates
- **Units:** kWh, GJ
- **Suppliers:** Grid, Solar, Local Discom
- **Processes:** EAF, Rolling Mill, Pellet Plant, etc.

### Scope 3 (Value Chain)

- **Source:** 15 GHG Protocol categories
- **Months:** 2024-01, 2024-02, 2024-03 → Converted to month-end dates
- **Categories:** Purchased Goods, Transportation, Business Travel, etc.
- **Vendors:** Tracked for supply chain analysis

## Output

The script provides detailed logging:

```
==============================================================
Starting GHG Data Import
==============================================================
Reading data from: ../../GHG Sheet.xlsx
Clearing existing sample data...
✓ Sample data cleared

==============================================================
Processing Scope 1 Data
==============================================================
Read 123 rows from Scope 1 sheet
Found 66 unique emission factors
✓ Scope 1 import complete

==============================================================
Processing Scope 2 Data
==============================================================
Read 18 rows from Scope 2 sheet
Found 6 unique emission factors
✓ Scope 2 import complete

==============================================================
Processing Scope 3 Data
==============================================================
Read 30 rows from Scope 3 sheet
Found 12 unique emission factors
✓ Scope 3 import complete

==============================================================
IMPORT SUMMARY
==============================================================
Emission Factors Created: 84
Emission Records Created: 171
Business Metrics Created: 0
```

## Verification

After import, verify the data:

```bash
# Check emission factors
docker exec ghg_postgres_db psql -U ghg_user -d ghg_platform -c "SELECT COUNT(*) FROM emission_factors;"

# Check emission records
docker exec ghg_postgres_db psql -U ghg_user -d ghg_platform -c "SELECT COUNT(*) FROM emission_records;"

# Check by scope
docker exec ghg_postgres_db psql -U ghg_user -d ghg_platform -c "SELECT scope, COUNT(*) FROM emission_records GROUP BY scope;"
```

## Troubleshooting

### File Not Found Error

```
ERROR: Excel file not found: ../../GHG Sheet.xlsx
```

**Solution:** Ensure `GHG Sheet.xlsx` is in the project root directory (same level as docker-compose.yml)

### Database Connection Error

```
ERROR: could not connect to server
```

**Solution:** Start the database: `docker-compose up -d db`

### Import Errors

Check the log output for specific errors. Common issues:

- Missing columns in Excel file
- Invalid data types
- Duplicate factor combinations

## Re-running the Import

The script is idempotent - it clears existing data before importing. You can safely re-run it multiple times:

```bash
python scripts/import_ghg_data.py
```

## Next Steps

After successful import:

1. **Test the API endpoints:**

   ```bash
   curl http://localhost:8000/api/analytics/yoy?current_year=2024&previous_year=2023
   ```

2. **View interactive docs:**
   Open http://localhost:8000/docs

3. **Query the data:**
   Use the analytics endpoints to explore the imported data
