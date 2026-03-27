---
name: plate-lookup
description: Look up US license plates using free public data sources. Returns parking violations (NYC Open Data), NHTSA recall data by VIN if available, and state registration hints. Triggers on phrases like "look up plate", "license plate", "plate lookup", "run a plate".
user-invocable: true
argument-hint: [plate <PLATE> <STATE>]
allowed-tools: read, write, web_fetch, exec
---

# Plate Lookup Skill

## Data Sources (free, no auth required)

| Source | What it returns | URL pattern |
|--------|----------------|-------------|
| NYC Open Data — Parking violations | All NYC parking tickets for plate | `data.cityofnewyork.us/resource/nc67-uf89.json?plate={PLATE}` |
| NYC Open Data — Camera violations | Red light / school zone violations | `data.cityofnewyork.us/resource/pvqr-7yc4.json?plate={PLATE}` |
| OpenDMV (if available) | Make/model/year from VIN decode | `vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{VIN}?format=json` |
| NHTSA Recalls | Recalls by make/model/year | `api.nhtsa.gov/recalls/recallsByVehicle?make={MAKE}&model={MODEL}&modelYear={YEAR}` |

## Workflow

### 1. Run parking violations check (always first — free, instant)
```
GET https://data.cityofnewyork.us/resource/nc67-uf89.json?plate={PLATE}&$limit=10&$order=issue_date DESC
```
Returns: issue_date, violation_description, fine_amount, plate_type, registration_state

### 2. Run camera violations check
```
GET https://data.cityofnewyork.us/resource/pvqr-7yc4.json?plate={PLATE}&$limit=10
```
Returns: issue_date, violation, fine_amount, state

### 3. Summarize
- Total violations found
- Most recent violation date
- Total fines (sum fine_amount)
- Violation type breakdown
- Clean record statement if empty

## Output Format

```
PLATE: {PLATE} ({STATE})
━━━━━━━━━━━━━━━━━━━━━
PARKING VIOLATIONS (NYC): {count}
CAMERA VIOLATIONS (NYC):  {count}
TOTAL FINES:              ${total}
LAST VIOLATION:           {date or "none on record"}
━━━━━━━━━━━━━━━━━━━━━
STATUS: {CLEAN / VIOLATIONS FOUND}
```

## Bicycle & Pedestrian Safety Extension

### Mission
This skill exists for families who've lost someone to reckless driving. Free public data only.
No surveillance. Just what NYC already exposes.

### Additional Data Sources

| Source | What it returns | URL pattern |
|--------|----------------|-------------|
| NYC Vision Zero — Crashes | All crashes with injuries/fatalities by location | `data.cityofnewyork.us/resource/h9gi-nx95.json` |
| NYC Vision Zero — Vehicle type | Filter crashes involving bikes | `...?contributing_factor_vehicle_1=Unsafe Speed` |
| NYC DCAS — Bike lane violations | Vehicles blocking bike lanes (camera enforcement) | `data.cityofnewyork.us/resource/puhe-ghj9.json?plate_id={PLATE}` |
| NYC Open Data — Cyclist injuries | Crashes with number_of_cyclist_injured > 0 | `data.cityofnewyork.us/resource/h9gi-nx95.json?$where=number_of_cyclist_injured>0` |

### Bike Lane Violation Check
```
GET https://data.cityofnewyork.us/resource/puhe-ghj9.json?plate_id={PLATE}&$limit=10
```
Returns: issue_date, violation_description, fine_amount

### Extended Output Format
```
PLATE: {PLATE} ({STATE})
━━━━━━━━━━━━━━━━━━━━━
PARKING VIOLATIONS (NYC): {count}
CAMERA VIOLATIONS (NYC):  {count}
BIKE LANE VIOLATIONS:     {count}
TOTAL FINES:              ${total}
LAST VIOLATION:           {date or "none on record"}
━━━━━━━━━━━━━━━━━━━━━
STATUS: {CLEAN / VIOLATIONS FOUND / BIKE LANE OFFENDER}
```

### Vision Zero Context
NYC Vision Zero crash data is public and queryable by borough, date, contributing factor.
A plate with repeated bike lane violations is a leading indicator — not proof, but signal.
Families who've lost cyclists or pedestrians can use this data to build a factual record.

## Notes

- NYC data only covers violations issued IN NYC regardless of plate state
- Empty result = no violations in NYC public records (not a statewide clean record)
- Owner info / make / model require paid APIs (faxvin, carfax) or DMV login
- For VIN-based decode: NHTSA vPIC API is free and returns make/model/year/engine/trim
- Bike lane violation dataset: `puhe-ghj9` — confirm field name `plate_id` before querying
