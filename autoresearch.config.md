# Autoresearch Configuration: Time Zone Reframe Skill Optimization

## Goal
Optimize the "time zone reframe skill" to maintain >93% effectiveness while reducing churn and integrating Excel for time zone calculations.

## Metric
- **Name**: Time zone conversion success rate
- **Direction**: Higher is better (target >93%)
- **Extract command**: Count successful conversions / total attempted, expressed as percentage
- **Excel integration**: Success rate of Excel export/import operations for time zone data

## Target Files
- `time-zone-reframe-skill.md` (to be created) - Main skill implementation
- `excel-integration.py` (to be created) - Excel time zone calculation utilities
- `tz-test-suite.py` (to be created) - Test suite for accuracy measurement

## Read-Only Files
- All other files - Only modifying the 3 target files above

## Run Command
```
python tz-test-suite.py --iterations=1000 --excel-integration-test=true
```

## Time Budget
- **Per experiment**: 30 seconds
- **Kill timeout**: 60 seconds

## Constraints
- Must maintain >93% accuracy baseline
- Excel integration must handle both .xlsx and .csv formats
- Skill must handle all US time zones (EST, CST, MST, PST, AKST, HST) + UTC
- Must reduce "churn" (unnecessary recalculations) by at least 50%
- No external API calls for time zone data (use Python built-in libraries)
- Must work with Python 3.8+ standard library only

## Branch
autoresearch/tz-reframe-excel-2026-03-27

## Notes
- Current time: EST for user (UTC-5/UTC-4 during DST)
- Target churn reduction: <50% recalculations for same inputs
- Excel integration: Read/write time zone conversion tables
- Skill format: Must follow OpenClaw skill structure (name, description, user-invocable, argument-hint, allowed-tools)

## Baseline Requirements
1. Create initial skill file with basic time zone conversion
2. Create Excel integration module
3. Create test suite with 1000 random time conversions
4. Measure baseline accuracy and churn rate
5. Record baseline metrics before starting experiments

## Experimental Variables
1. **Conversion algorithm**: pytz vs zoneinfo vs custom calculation
2. **Caching strategy**: Memoization depth, TTL, invalidation logic
3. **Excel format**: .xlsx vs .csv, sheet naming, column structure
4. **Error handling**: Graceful degradation for ambiguous times
5. **User experience**: Skill argument hints, response formatting