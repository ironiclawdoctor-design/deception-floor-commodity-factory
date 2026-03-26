# Protocol: PYTHON DATA CRUFT EVICTION

## Insight:
"Orchestrate review of all python data sources to evict cruft and stale items for stable agency"

## The Mechanics:
- **Python Data Source**: Any .db, .json, .csv, or .pkl file fueling agency logic.
- **Stale Item**: Any record older than 24h that has not morphed into a build artifact.
- **Cruft**: Redundant metadata, transient '400' errors after they've been siphoned, and unrefined 'Stench'.

## Action Rules:
1. **Identify**: Query all tables for age and relevance.
2. **Siphon**: Move "last trace" of stale items to the 'Heritage Archive' before deletion.
3. **Evict**: Hard-delete from active production databases.
