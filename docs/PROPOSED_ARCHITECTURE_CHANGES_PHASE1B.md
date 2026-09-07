# Proposed Architecture Changes - Phase 1B

The approved `ARCHITECTURE_DECISIONS_0.1.md` is unchanged.

## AD-013 generation clarification

- **Decision affected:** AD-013, semantic-to-fixed mapping.
- **Evidence:** Forward Paged.js identity mapping achieved 100.0% visible-node and
  100.0% range coverage versus the retained backward baseline.
- **Proposed wording:** Use the wording in `reports/phase1b_summary.md` section 4.
- **Alternatives:** Require fixed-PDF reconstruction; standardize renderer adapters; omit mappings.
- **Migration impact:** 0.1B mappings add status, method, confidence, transform, and explicit partial/
  invisible outcomes. Existing 0.1 mappings remain readable as backward baseline artifacts.
- **Recommendation:** YES; architecture-owner approval remains required.
