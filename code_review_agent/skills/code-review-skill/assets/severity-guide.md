# Severity Guide

## CRITICAL
Issues that MUST be fixed before merging. Examples:
- Logic bugs that cause incorrect output
- Unhandled exceptions that crash the app
- Off-by-one errors in loops/indices
- Broken error handling (silent failures)
- Hardcoded credentials or secrets

## WARNING   
Strong recommendations. Should be fixed unless there's a deliberate reason. Examples:
- Missing input validation
- Functions doing multiple unrelated things
- Deep nesting (>3 levels)
- Duplicate logic blocks
- Missing docstrings on public APIs

## SUGGEST
Optional improvements for code health. Examples:
- Better variable naming
- Opportunity to extract a helper function
- Minor style consistency
- Performance optimizations that don't affect correctness
