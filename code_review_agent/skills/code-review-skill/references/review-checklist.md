# Code Review Checklist

## 1. Correctness
- [ ] Does the logic match the intended behavior?
- [ ] Are edge cases handled (null, empty, overflow, negative)?
- [ ] Are errors caught and handled properly?
- [ ] Are return values checked?

## 2. Naming & Readability
- [ ] Are variable/function names descriptive and consistent?
- [ ] Are magic numbers replaced with named constants?
- [ ] Is the code self-documenting or well-commented?
- [ ] Are comments accurate and up-to-date?

## 3. Design & Structure
- [ ] Does each function do one thing only (Single Responsibility)?
- [ ] Is code DRY — no unnecessary duplication?
- [ ] Are abstractions at the right level?
- [ ] Is the function/class size reasonable (<50 lines for functions)?

## 4. Performance
- [ ] Are there any obvious N+1 query patterns?
- [ ] Are expensive operations inside loops unnecessarily?
- [ ] Is memory usage reasonable?
- [ ] Are caches/memoization used where appropriate?

## 5. Maintainability
- [ ] Is the code testable?
- [ ] Are dependencies minimal and explicit?
- [ ] Would a new developer understand this in <5 minutes?
