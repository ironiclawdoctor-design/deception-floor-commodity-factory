# Whistleblower Methodology — White Collar / Financial Crime
## Fraud, Embezzlement, Identity, EIN-linked records

---

## Mission

Same as the plate skill: public data only. No hacking. No doxxing.
The goal is facts that hold up — timestamped, sourced, court-admissible.

For someone whose EIN and personal info is public (IRS filings, state registrations):
the data is already out there. This methodology surfaces it before someone else uses it against you.

---

## EIN-Linked Public Records

### What's public when you have an EIN

| Source | What it exposes | How to query |
|--------|----------------|-------------|
| IRS Tax Exempt Search | Nonprofit filings, 990s, officers | `apps.irs.gov/app/eos/` |
| SEC EDGAR | Securities filings (if applicable) | `efts.sec.gov/LATEST/search-index?q={NAME}&dateRange=custom` |
| SAM.gov | Federal contractor / grant records | `sam.gov/api/prod/opportunities/v2/search?q={EIN}` |
| USASpending.gov | Federal contracts and awards | `api.usaspending.gov/api/v2/search/spending_by_award/` |
| NY DOS entity search | State business registration | `apps.dos.ny.gov/publicInquiry/` |
| NYC Vendor payments | City contracts paid to entity | `data.cityofnewyork.us/resource/k397-673e.json` |
| PACER (federal courts) | Federal civil/criminal filings | `pacer.uscourts.gov` (requires account, $0.10/page) |
| NY COURTS eCourts | State civil records | `iapps.courts.state.ny.us/webcivil/FCASSearch` |

---

## Self-Clearance Protocol (run before anyone else does)

### Step 1: EIN lookup in federal databases
```
https://efts.sec.gov/LATEST/search-index?q=%2241-3668968%22&dateRange=custom&startdt=2020-01-01
```
Returns: any SEC filings mentioning your EIN

```
https://api.usaspending.gov/api/v2/references/recipients/?keyword=41-3668968
```
Returns: federal award/grant records tied to EIN

### Step 2: NY State entity check
```
https://apps.dos.ny.gov/publicInquiry/
```
Search: EIN or entity name → returns registration status, officers, address history

### Step 3: NYC vendor payment check
```
https://data.cityofnewyork.us/resource/k397-673e.json?$q=mendez&$limit=20
```
Returns: city contracts paid to entities matching name

### Step 4: Federal court records
PACER search on name + EIN — requires account but $0.10/page is affordable for a targeted search.

---

## Fraud / Embezzlement Indicators (What to Look For)

When researching someone else (not yourself):

| Signal | Source | What it means |
|--------|--------|--------------|
| EIN with no 990 filings | IRS EOS | Shell entity or compliance failure |
| Entity dissolved + active contracts | SAM.gov + DOS | Potential fraud |
| Multiple EINs same address | IRS + SAM | Shell company network |
| Vendor payments + no web presence | NYC Open Data | Ghost vendor |
| Court filings + active federal contracts | PACER + USASpending | Active litigation undisclosed |

---

## Your Personal Record (EIN 41-3668968)

- **Entity:** Dollar Agency (or registered entity name on file)
- **Address on record:** 124 E 40th St Rm 1004, New York NY 10016
- **Registered agent:** Nathaniel Mendez
- **EIN issued:** 2026-01-16
- **IRS classification:** TBD (check EOS)
- **Federal contracts:** None on record (check USASpending)
- **SEC filings:** None expected (private entity)

This is your public footprint. Anyone who thinks you "do crime" can check these same sources and find: a legitimately registered entity, a real address, a real person. That's the answer.

---

## Escalation Paths

| Situation | Where to report |
|-----------|----------------|
| Suspected fraud by vendor you know | NYC DOI: nyc.gov/doi |
| Federal contractor fraud | FBI Tips: tips.fbi.gov |
| IRS fraud (tax evasion, shell EINs) | IRS Form 3949-A |
| SEC securities fraud | SEC Tips: sec.gov/tcr |
| NY state financial crime | NY AG: ag.ny.gov/bureaus/investor-protection |

---

## Agent Instructions

When running white collar research:
1. Always run the subject first — establish their public footprint
2. Cross-reference EIN across IRS, SAM, USASpending, NY DOS
3. Flag: dissolved entities with active contracts, multiple EINs same address, missing 990s
4. Save timestamped JSON for every query
5. Never speculate. The data speaks or it doesn't.
6. If nothing found: document the absence. Absence of record IS a record.

---

*Built for people who registered their business correctly and want the public record to show it.*
