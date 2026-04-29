# Complexity Metrics Reference

## Cyclomatic Complexity

Count one point for each:
- `if` / `elif` / `else`
- `for` / `while`
- `try` / `except`
- `and` / `or` in conditions
- `case` in match statements

**Thresholds:**
| Score | Rating     | Action         |
|-------|------------|----------------|
| 1–5   | Simple     | No action   |
| 6–10  | Moderate   | Acceptable  |
| 11–15 | Complex    | Refactor    |
| 16+   | Very High  | Must refactor|

## Cognitive Complexity

Measures how hard code is to *read* (not just how many branches). Penalize:
- Nesting (+1 per level)
- Breaks in linear flow (early returns, recursion)
- Mixed concerns in one function

## Refactoring Patterns to Suggest

### Extract Function
When a block inside a function has a clear single purpose, extract it.

### Replace Conditionals with Polymorphism
When `if isinstance(x, TypeA)` chains appear — suggest strategy pattern or dispatch dict.

### Guard Clauses
Replace deeply nested if-else with early returns.

### Parameter Object
When 5+ params appear, wrap in a dataclass/TypedDict.

### Decompose Conditional
Extract complex boolean expressions into named variables or functions.
