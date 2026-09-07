# Specification blocker register

## OPEN SPEC BLOCKERS

None. **OPEN SPEC BLOCKERS = 0.**

## RESOLVED NON-SPEC ISSUES

### SPEC_BLOCKER-001 — Accessible roll-up without human evidence

- Classification: `CORPUS_EXPECTATION_ERROR`
- Draft sections: 58 and 74
- Requirement IDs: SPD-ACC-001 and SPD-ACC-004
- Resolution: conformance corpus expected result corrected to
  `Accessible: NOT_TESTED`; Base remains PASS and no artificial violation was
  introduced.
- Draft change: **NONE**
- Validator code semantic change: **NONE**

The original fixture oracle represented an unresolved required human WCAG
evaluation as PASS. Validator A's existing interpretation—no established failure
but incomplete certification means NOT_TESTED—was correct.
