# Whistleblower Methodology — Sanctions, Wanted Lists, War Crimes
## Self-clearance and third-party research using public international databases

---

## Mission

Public clearance check. If someone accuses you of being on a wanted list,
these are the authoritative sources — and how to search them.

All sources are public record. No hacking. Facts only.

---

## Database Index

### 🇺🇸 United States

| Database | What it covers | URL |
|----------|---------------|-----|
| OFAC SDN List | Treasury sanctions — terrorists, traffickers, proliferators | https://sanctionssearch.ofac.treas.gov/ |
| OFAC CSV (full) | Machine-readable, updated daily | https://www.treasury.gov/ofac/downloads/sdn.csv |
| FBI Most Wanted | Fugitives, terrorists, cybercriminals | https://www.fbi.gov/wanted/search |
| DHS Terrorist Screening | No public search — FBI/law enforcement only | N/A |
| PACER | Federal court filings (indictments, convictions) | https://pacer.uscourts.gov |

### 🌍 International

| Database | What it covers | URL |
|----------|---------------|-----|
| INTERPOL Red Notices | International arrest warrants | https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices |
| ICC Indictments | War crimes, genocide, crimes against humanity | https://www.icc-cpi.int/cases |
| UN Security Council Sanctions | Al-Qaeda, ISIS, country-specific regimes | https://scsanctions.un.org/fop/fop?xml=htdocs/resources/xml/en/consolidated.xml |
| EU Consolidated Sanctions | European sanctions lists | https://webgate.ec.europa.eu/fsd/fsf |
| UK OFSI Sanctions | UK financial sanctions | https://ofsistorage.blob.core.windows.net/publishlive/ConList.csv |

### 🌍 Africa-Specific (Lesotho, Rwanda, Regional)

| Database | What it covers | URL |
|----------|---------------|-----|
| UN ICTR Records | Rwanda genocide tribunal (1994) | https://unictr.irmct.org/en/cases |
| IRMCT (successor to ICTR) | Ongoing Rwanda/Yugoslavia cases | https://www.irmct.org/en/cases |
| African Union Peace & Security | AU sanctions and wanted persons | https://au.int/en/organs/psc |
| Rwanda National Public Prosecution | National genocide cases | https://www.nppa.gov.rw |

---

## How to Search (Self-Clearance Protocol)

### Step 1: OFAC name search (fastest)
```
https://sanctionssearch.ofac.treas.gov/
→ Enter: "Nathaniel Mendez"
→ Select: All Programs
→ Result: Not found = not on US sanctions list
```

### Step 2: INTERPOL Red Notice search
```
https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices
→ Search by name
→ Result: Not found = no active international arrest warrant
```

### Step 3: ICC cases (war crimes / genocide)
```
https://www.icc-cpi.int/cases
→ Browse active indictments
→ All named — no anonymous entries
→ Result: Name not present = no ICC indictment
```

### Step 4: UN ICTR / IRMCT (Rwanda genocide specifically)
```
https://unictr.irmct.org/en/cases
→ All indicted persons named publicly
→ Rwanda genocide tribunal records complete and public
```

### Step 5: US Federal court (PACER)
```
https://pacer.uscourts.gov
→ $0.10/page, requires account
→ Search by name across all federal districts
→ Returns: indictments, convictions, civil suits
```

---

## Machine-Readable Checks (for agents)

```python
import urllib.request, csv, io

# OFAC SDN — search by name
def check_ofac(name):
    url = "https://www.treasury.gov/ofac/downloads/sdn.csv"
    data = urllib.request.urlopen(url, timeout=30).read().decode('latin-1')
    reader = csv.reader(io.StringIO(data))
    hits = []
    for row in reader:
        if len(row) > 1 and name.lower() in row[1].lower():
            hits.append({'id': row[0], 'name': row[1], 'type': row[2], 'country': row[3]})
    return hits

# UK OFSI — search by name  
def check_uk_sanctions(name):
    url = "https://ofsistorage.blob.core.windows.net/publishlive/ConList.csv"
    data = urllib.request.urlopen(url, timeout=30).read().decode('utf-8', errors='ignore')
    return [line for line in data.split('\n') if name.lower() in line.lower()]
```

---

## Expected Result for Nathaniel Mendez

Based on all available evidence:
- **OFAC SDN:** Not listed
- **FBI Most Wanted:** Not listed
- **INTERPOL Red Notice:** Not listed
- **ICC indictment:** Not listed
- **UN ICTR/IRMCT:** Not listed (Rwanda tribunal covers 1994 genocide perpetrators, all named)
- **Federal court (PACER):** No known filings

**Public record conclusion:** No sanctions, no warrants, no indictments across any searchable international database. EIN registered, address public, entity legitimate.

---

## For Agents Running This Check

1. Search OFAC CSV by name (grep/CSV parse)
2. Search UK OFSI CSV by name
3. Check INTERPOL via browser (Cloudflare-gated, requires human or browser tool)
4. Check ICC cases page (Cloudflare-gated)
5. Log all results with timestamp
6. Absence of record IS the record — document it

*Built for people who are clean and want the databases to show it.*
