# Review Output Format

Always structure your review exactly as follows:

---

## Code Review Summary

**Language:** {detected language}
**Overall Score:** {X}/10
**Verdict:** {APPROVE / REQUEST CHANGES / NEEDS DISCUSSION}

---

## Critical Issues (must fix)
> These block approval.

- **[CRITICAL]** `{file/line reference}` — {issue description}
  - **Fix:** {concrete suggestion}

---

## Warnings (should fix)
> These are strong recommendations.

- **[WARNING]** `{file/line reference}` — {issue description}
  - **Fix:** {concrete suggestion}

---

## Suggestions (optional improvements)
> Nice-to-haves that improve long-term maintainability.

- **[SUGGEST]** `{file/line reference}` — {issue description}
  - **Idea:** {concrete suggestion}

---

## What's Good
> Acknowledge good patterns — this builds trust and context.

- {positive observation}

---

## Checklist Summary
| Category       | Status |
|----------------|--------|
| Correctness    | OK / WARNING / CRITICAL |
| Naming         | OK / WARNING / CRITICAL |
| Design         | OK / WARNING / CRITICAL |
| Performance    | OK / WARNING / CRITICAL |
| Maintainability| OK / WARNING / CRITICAL |
