# Proposed Architecture Changes

No accepted architecture decision is proposed for change from this local run.

## Experimental clarification candidate (not an ADR change)

- **Decision affected:** AD-013 / Mapping 0.1.
- **Evidence:** Exact-token mapping can be partial and extractor-dependent, especially for bidi,
  MathML, SVG/vector content, and large nested nodes.
- **Why change is proposed:** None yet; the evidence comes from one implementation.
- **Alternative options:** Add confidence/provenance and explicit unmappable outcomes; use renderer
  instrumentation; post-process tagged PDF; narrow map targets to leaf semantic objects.
- **Migration impact:** Unknown until multi-renderer trials.
- **Recommendation:** Test all alternatives before changing the accepted decision.
