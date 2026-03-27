# Whistleblower Methodology — Plate Lookup Skill
## For people who suspect wrongdoing but lack institutional power

---

## Mission Statement

This methodology exists for:
- Families who lost someone and want a factual record
- Cyclists and pedestrians who were hit and need to build a case
- Neighbors who keep seeing the same reckless driver
- Anyone accused of wrongdoing who wants to prove their own clean record

**Rule:** Public data only. No hacking. No doxxing. No surveillance beyond what the city already publishes. The goal is facts, not harassment.

---

## Step 1: Build Your Own Record First

Before pointing at anyone else, run yourself.

```
plate-lookup <YOUR_PLATE> NY
```

Document the result. Timestamp it. This is your baseline — the factual counter to any accusation.
If someone says you "do crime," your public record is the answer.

---

## Step 2: NYC Open Data Sources (All Free, No Auth)

### Parking Violations
```
https://data.cityofnewyork.us/resource/nc67-uf89.json?plate={PLATE}&$limit=1000
```
Fields: issue_date, violation_description, fine_amount, street_name, violation_county

### Camera Violations (Red Light / Speed / School Zone)
```
https://data.cityofnewyork.us/resource/pvqr-7yc4.json?plate_id={PLATE}&$limit=1000
```

### Vision Zero Crashes (by location, not plate)
```
https://data.cityofnewyork.us/resource/h9gi-nx95.json?$where=number_of_cyclist_injured>0&$limit=100
```
Use this when you have a location + date but not a plate.

### 311 Complaints (reckless driving reports)
```
https://data.cityofnewyork.us/resource/erm2-nwe9.json?complaint_type=Blocked%20Bike%20Lane&$limit=100
```

---

## Step 3: Pattern Recognition — What Signals Wrongdoing

| Pattern | Significance |
|---------|-------------|
| 10+ parking violations, unpaid | Systematic disregard for rules |
| Camera violations near schools | Speed enforcement zone offender |
| Violations concentrated in one zone | Local repeat offender |
| Violations spiking then stopping | License suspended, switched plates, or moved |
| Zero violations | Either clean OR plates recently changed |

---

## Step 4: Cross-Reference with Crash Data

If you have a date + location of an incident:

```
https://data.cityofnewyork.us/resource/h9gi-nx95.json
  ?$where=crash_date >= '2024-01-01' 
  AND on_street_name = 'BROADWAY'
  AND number_of_persons_injured > 0
  &$limit=50
```

This returns: vehicle types, contributing factors, injuries/fatalities — publicly attributed.

---

## Step 5: Document and Preserve

Every result should be saved:
```python
import json, datetime
result = {
    "plate": "XXXXX",
    "state": "NY",
    "queried_at": datetime.datetime.utcnow().isoformat() + "Z",
    "parking_violations": [...],
    "camera_violations": [...],
    "total_fines": 0,
    "status": "CLEAN"
}
# Write to plate-records/{PLATE}-{DATE}.json
```

Timestamped records are evidence. Screenshots are not.

---

## Step 6: When to Escalate

| Situation | Where to go |
|-----------|------------|
| Hit and run, have partial plate | NYPD 311 + Vision Zero hotline |
| Repeat bike lane blocker | 311 complaint (creates a paper trail) |
| Driver with suspended license (you suspect) | DMV complaint form (requires more info) |
| Building a legal case | NYC Legal Aid, Families for Safe Streets |

**Families for Safe Streets:** https://familiesforsafestreets.org  
Run by people who lost family to traffic violence. They know how to use this data.

---

## Step 7: What This Cannot Do

- **Cannot confirm registration status** (DMV login required)
- **Cannot confirm insurance** (private database)
- **Cannot confirm driver identity** (DPPA-protected)
- **Cannot confirm outstanding warrants** (law enforcement only)

What it CAN do: build a factual, timestamped, court-admissible record of public violations tied to a plate. That's often enough.

---

## Agent Instructions

When any agent runs plate-lookup for whistleblower purposes:

1. Run all three violation types simultaneously
2. Generate a timestamped JSON record
3. Flag plates with >5 violations as `PATTERN_OF_CONCERN`
4. Flag plates with camera violations near schools as `SCHOOL_ZONE_OFFENDER`
5. Include Vision Zero crash lookup if location is provided
6. Never speculate beyond the data
7. Always include the Families for Safe Streets reference if injuries/fatalities are mentioned

---

*Built for people who drive safely and know others who don't.*
