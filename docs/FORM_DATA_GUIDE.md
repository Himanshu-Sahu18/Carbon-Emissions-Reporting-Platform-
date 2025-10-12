# Form Data Guide - Valid Input Reference

## 🎯 Understanding the Emission Form

### Why You're Getting Errors:

The form validates against **emission factors in the database**. You can ONLY use activity names that exist in the database with matching units.

---

## ✅ Valid Activity Names & Their Units

Here's the EXACT data you can use:

### 1. **Diesel** (Scope 1 - Direct Emissions)

```
Activity Name: Diesel
Activity Unit: litres
Valid Range: 1 - 10,000 litres
Typical Values: 100-500 litres per day
Example: 450 litres
```

**What it represents**: Diesel fuel for generators, vehicles, machinery

---

### 2. **Natural Gas** (Scope 1 - Direct Emissions)

```
Activity Name: Natural Gas
Activity Unit: cubic meters
Valid Range: 1 - 50,000 cubic meters
Typical Values: 500-2,000 cubic meters per month
Example: 850 cubic meters
```

**What it represents**: Natural gas for heating, boilers, furnaces

---

### 3. **Gasoline** (Scope 1 - Direct Emissions)

```
Activity Name: Gasoline
Activity Unit: litres
Valid Range: 1 - 5,000 litres
Typical Values: 100-300 litres per day
Example: 240 litres
```

**What it represents**: Gasoline for company vehicles, fleet

---

### 4. **Grid Electricity** (Scope 2 - Indirect Emissions)

```
Activity Name: Grid Electricity
Activity Unit: kWh
Valid Range: 1 - 100,000 kWh
Typical Values: 3,000-6,000 kWh per month
Example: 4200 kWh
```

**What it represents**: Electricity purchased from the grid

---

### 5. **Business Travel - Air** (Scope 3 - Other Indirect)

```
Activity Name: Business Travel - Air
Activity Unit: km
Valid Range: 1 - 50,000 km
Typical Values: 500-3,000 km per trip
Example: 1200 km
```

**What it represents**: Air travel for business purposes

---

### 6. **Employee Commute** (Scope 3 - Other Indirect)

```
Activity Name: Employee Commute
Activity Unit: km
Valid Range: 1 - 100,000 km
Typical Values: 2,000-5,000 km per month (all employees)
Example: 2400 km
```

**What it represents**: Employee commuting to work

---

### 7. **Waste Disposal** (Scope 3 - Other Indirect)

```
Activity Name: Waste Disposal
Activity Unit: kg
Valid Range: 1 - 10,000 kg
Typical Values: 200-600 kg per month
Example: 380 kg
```

**What it represents**: Waste sent to landfill

---

## 📅 Date Rules

```
✅ Valid: Any date from 2000-01-01 to TODAY
❌ Invalid: Future dates
❌ Invalid: Dates before 2000

Examples:
✅ 2024-10-15
✅ 2023-06-20
✅ 2024-01-01
❌ 2025-12-31 (future)
❌ 1999-01-01 (too old)
```

---

## 📝 Complete Test Examples

### Example 1: Factory Diesel Usage

```
Activity Name: Diesel
Activity Value: 450
Activity Unit: litres
Activity Date: 2024-10-15
Location: Factory A
Department: Operations
```

**Expected CO2e**: ~1,228.5 kg

---

### Example 2: Office Electricity

```
Activity Name: Grid Electricity
Activity Value: 4200
Activity Unit: kWh
Activity Date: 2024-10-10
Location: Office Building
Department: Facilities
```

**Expected CO2e**: ~1,764 kg

---

### Example 3: Heating Gas

```
Activity Name: Natural Gas
Activity Value: 850
Activity Unit: cubic meters
Activity Date: 2024-10-20
Location: Factory A
Department: Operations
```

**Expected CO2e**: ~1,742.5 kg

---

### Example 4: Company Fleet

```
Activity Name: Gasoline
Activity Value: 240
Activity Unit: litres
Activity Date: 2024-10-25
Location: Fleet Garage
Department: Logistics
```

**Expected CO2e**: ~559.2 kg

---

### Example 5: Business Trip

```
Activity Name: Business Travel - Air
Activity Value: 1200
Activity Unit: km
Activity Date: 2024-10-30
Location: Airport
Department: Sales
```

**Expected CO2e**: ~300 kg

---

## 🚫 Common Errors & Why

### Error: "Not Found"

**Cause**: Activity name doesn't match exactly

```
❌ Wrong: "diesel" (lowercase)
✅ Correct: "Diesel" (capital D)

❌ Wrong: "Electricity"
✅ Correct: "Grid Electricity"

❌ Wrong: "Air Travel"
✅ Correct: "Business Travel - Air"
```

### Error: "Unit Mismatch"

**Cause**: Wrong unit for the activity

```
❌ Wrong: Diesel with "gallons"
✅ Correct: Diesel with "litres"

❌ Wrong: Natural Gas with "litres"
✅ Correct: Natural Gas with "cubic meters"
```

### Error: "Future Date"

**Cause**: Date is in the future

```
❌ Wrong: 2025-12-31
✅ Correct: 2024-10-15
```

### Error: "Negative Value"

**Cause**: Activity value is negative or zero

```
❌ Wrong: -100 or 0
✅ Correct: 450 (any positive number)
```

---

## 📊 Business Metrics Form

### Valid Metric Names:

```
1. Tons of Steel Produced
   Unit: tons
   Range: 1 - 50,000 tons
   Example: 13100 tons

2. Revenue
   Unit: USD
   Range: 1 - 10,000,000 USD
   Example: 2620000 USD

3. Employee Count
   Unit: employees
   Range: 1 - 10,000 employees
   Example: 250 employees

4. Production Hours
   Unit: hours
   Range: 1 - 10,000 hours
   Example: 720 hours
```

**Note**: You can use ANY metric name for business metrics - they're not restricted like emission activities.

---

## 💡 Understanding the Data

### Scope 1 (Direct Emissions)

- **What**: Emissions you directly control
- **Examples**: Diesel, Natural Gas, Gasoline
- **Typical %**: 60-80% of total emissions
- **Why it matters**: These are the easiest to reduce through operational changes

### Scope 2 (Indirect - Electricity)

- **What**: Emissions from purchased electricity
- **Examples**: Grid Electricity
- **Typical %**: 15-30% of total emissions
- **Why it matters**: Can be reduced through renewable energy or efficiency

### Scope 3 (Other Indirect)

- **What**: Emissions from your value chain
- **Examples**: Business Travel, Commute, Waste
- **Typical %**: 5-20% of total emissions
- **Why it matters**: Often overlooked but important for complete footprint

---

## 🎯 Realistic Data Ranges by Organization Size

### Small Office (10-50 employees)

```
Diesel: 50-200 litres/month
Natural Gas: 200-800 cubic meters/month
Gasoline: 100-400 litres/month
Grid Electricity: 1,000-3,000 kWh/month
Business Travel: 500-2,000 km/month
Employee Commute: 1,000-3,000 km/month
Waste: 100-300 kg/month
```

### Medium Factory (50-200 employees)

```
Diesel: 300-800 litres/month
Natural Gas: 800-2,000 cubic meters/month
Gasoline: 200-600 litres/month
Grid Electricity: 3,000-8,000 kWh/month
Business Travel: 1,000-4,000 km/month
Employee Commute: 3,000-8,000 km/month
Waste: 300-800 kg/month
```

### Large Industrial (200+ employees)

```
Diesel: 500-2,000 litres/month
Natural Gas: 1,500-5,000 cubic meters/month
Gasoline: 400-1,000 litres/month
Grid Electricity: 5,000-20,000 kWh/month
Business Travel: 2,000-8,000 km/month
Employee Commute: 5,000-15,000 km/month
Waste: 500-2,000 kg/month
```

---

## ✅ Quick Copy-Paste Test Data

Just copy these exactly into the form:

### Test 1: Diesel

```
Activity Name: Diesel
Activity Value: 450
Activity Unit: litres
Activity Date: 2024-10-15
Location: Factory A
Department: Operations
```

### Test 2: Electricity

```
Activity Name: Grid Electricity
Activity Value: 4200
Activity Unit: kWh
Activity Date: 2024-10-10
Location: Office
Department: Facilities
```

### Test 3: Natural Gas

```
Activity Name: Natural Gas
Activity Value: 850
Activity Unit: cubic meters
Activity Date: 2024-10-20
Location: Factory A
Department: Operations
```

### Test 4: Gasoline

```
Activity Name: Gasoline
Activity Value: 240
Activity Unit: litres
Activity Date: 2024-10-25
Location: Fleet
Department: Logistics
```

### Test 5: Air Travel

```
Activity Name: Business Travel - Air
Activity Value: 1200
Activity Unit: km
Activity Date: 2024-10-30
Location: Airport
Department: Sales
```

---

## 🔍 How to Check Valid Activities

Run this command to see all available activities in your database:

```bash
docker exec ghg_postgres_db psql -U ghg_user -d ghg_platform -c "SELECT activity_name, activity_unit, scope, co2e_per_unit FROM emission_factors WHERE valid_to IS NULL ORDER BY activity_name;"
```

This shows you exactly what activity names and units are valid!

---

## 📋 Quick Reference Table

| Activity Name         | Unit         | Scope | Typical Monthly Value | CO2e Factor   |
| --------------------- | ------------ | ----- | --------------------- | ------------- |
| Diesel                | litres       | 1     | 300-600               | 2.73 kg/litre |
| Natural Gas           | cubic meters | 1     | 800-1,500             | 2.05 kg/m³    |
| Gasoline              | litres       | 1     | 200-400               | 2.33 kg/litre |
| Grid Electricity      | kWh          | 2     | 3,000-6,000           | 0.42 kg/kWh   |
| Business Travel - Air | km           | 3     | 1,000-3,000           | 0.25 kg/km    |
| Employee Commute      | km           | 3     | 3,000-6,000           | 0.17 kg/km    |
| Waste Disposal        | kg           | 3     | 300-600               | 0.52 kg/kg    |

---

## 💡 Pro Tips

1. **Case Sensitive**: Activity names must match EXACTLY (including capitals)
2. **Copy-Paste**: To avoid typos, copy activity names from this guide
3. **Units Matter**: Each activity has a specific unit - don't mix them up
4. **Dates**: Use format YYYY-MM-DD (e.g., 2024-10-15)
5. **Location/Department**: These are optional but helpful for reporting
6. **Start Small**: Test with one entry first before bulk data entry

---

## 🆘 Still Getting Errors?

### Check These:

1. ✅ Activity name spelled exactly right (case-sensitive)
2. ✅ Unit matches the activity (see table above)
3. ✅ Date is not in the future
4. ✅ Value is positive (greater than 0)
5. ✅ Date format is YYYY-MM-DD

### Common Mistakes:

- Using "electricity" instead of "Grid Electricity"
- Using "meters" instead of "cubic meters"
- Using lowercase "diesel" instead of "Diesel"
- Forgetting the space in "Business Travel - Air"

---

## 📞 Need Help?

If you're still having issues:

1. Check the browser console (F12) for detailed error messages
2. Verify the backend is running: `docker-compose ps`
3. Check backend logs: `docker-compose logs backend`
4. Review the API docs: http://localhost:8000/docs

---

**Key Rule**: Activity Name + Unit must EXACTLY match what's in the database. Copy-paste from the examples above to avoid typos! 🎯
