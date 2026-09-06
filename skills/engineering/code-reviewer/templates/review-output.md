# Code Review: {FEATURE_NAME}

**Reviewer:** Code Reviewer Agent  
**Date:** {DATE}  
**Commits:** {BASE_SHA}..{HEAD_SHA}  
**Plan Reference:** {PLAN_FILE}

---

## Summary

{SUMMARY - 2-3 sentences overview}

**Verdict:** {✅ Approved / ⚠️ Needs Changes / ❌ Blocked}

---

## Strengths

- {Positive observation 1}
- {Positive observation 2}
- {Good practices observed}

---

## Plan Alignment

| Requirement | Status | Notes |
|-------------|--------|-------|
| {Req 1} | ✅ / ⚠️ / ❌ | {details} |
| {Req 2} | ✅ / ⚠️ / ❌ | {details} |
| {Req 3} | ✅ / ⚠️ / ❌ | {details} |

**Deviations:**
- {Any deviations from plan and whether justified}

---

## Issues

### 🔴 Critical

**{Issue Title}**
- **Location:** `{path/to/file.ts:line}`
- **Problem:** {Description}
- **Impact:** {Why this matters}
- **Fix:** 

```{language}
// Current
{problematic code}

// Recommended
{fixed code}
```

### 🟠 Important

**{Issue Title}**
- **Location:** `{path/to/file.ts:line}`
- **Problem:** {Description}
- **Fix:** {Recommendation}

### 🟡 Suggestions

- {Suggestion 1}
- {Suggestion 2}

---

## Code Quality Checklist

- [ ] Error handling comprehensive
- [ ] Type safety enforced
- [ ] Naming conventions followed
- [ ] Test coverage adequate
- [ ] No security vulnerabilities
- [ ] Performance acceptable

---

## Recommendations

1. {Priority action - must do}
2. {Second priority - should do}
3. {Optional improvement - nice to have}

---

## Questions for Author

- {Any clarifying questions about implementation decisions}
