# Validator impact and limits of convergence

Audit only: no validator code, dependencies or tests were modified or executed. Source review covers Validator A **0.1.0-draft.2** and Validator B **0.1.1**, with shared attribution contract **0.1.1**. Existing recorded results were inspected and their fixture hashes checked.

## EPUBCheck's exact current role

The normative dependency is EPUB conformance; the project's implementation uses **EPUBCheck 5.3.0** as an external Base-validation dependency. A document's conformance is not defined by a particular executable. The [Draft](../../spec/FORMAT_0.1_DRAFT.md) does not mandate that every third-party implementation invoke EPUBCheck by name. The [conformance matrix](../../spec/CONFORMANCE_MATRIX.md) identifies it as a validation technique.

There are three distinct dependency sets:

| Kind | Exact current requirement IDs |
| --- | --- |
| A marks incomplete when inherited tool evaluation is unavailable on an otherwise passing package | SPD-BASE-001, SPD-BASE-002 |
| B explicitly marks NOT_TESTED when EPUBCheck is unavailable/times out | SPD-BASE-002; Base roll-up also depends on tool availability |
| Contract 0.1.1 permits external errors to add failures | **6 IDs:** SPD-BASE-002, SPD-SEM-002, SPD-ID-006, SPD-SEC-004, SPD-SEC-005, SPD-SEC-006 |

The broader conformance matrix mentions EPUBCheck in **11 rows**: BASE-001/002/005/006, SEM-002/003, FIX-003, CAP-003 and DISC-001/002/003. That generic technique label is not evidence that EPUBCheck implements each SPD-specific predicate. In particular PDF/A's non-requirement and SPD descriptor semantics are not certified by EPUBCheck.

The six externally attributed IDs are defined by **seven guarded mappings** in [the shared attribution table](../../validator-convergence/attribution-table.md): OPF-060 duplicate ZIP → BASE-002; RSC-016 XML parse → SEM-002; RSC-005 duplicate ID → ID-006; RSC-005 specified invalid XML/content messages → SEM-002; RSC-006 remote CSS → SEC-005; RSC-006 remote image → SEC-006; RSC-008 remote font → SEC-004. There are two distinct guarded routes to SEM-002.

Frozen evidence records **70 completed executions per validator, 140 total**, **62 EPUBCheck PASS and 8 FAIL per validator**, and **7 fixtures with nonempty external SPD attribution**. A and B's normalized results match on all 70, and **all 40 Base-PASS fixtures have EPUBCheck PASS**. “70 executed” is not “70 EPUB-valid”: intentional negatives remain in the corpus.

## A shared completeness gap matters to this architecture gate

[A validate_path](../../validator-a/src/validator.rs) sets Base failure for **attributed IDs**. An external FAIL with no mapped ID does not by itself change an otherwise passing Base result. [B's adapter](../../validator-b/spd_validator_b/epubcheck.py) similarly records the raw result and emits only mapped failures; [its roll-up](../../validator-b/spd_validator_b/validator.py) tests availability and findings, not every raw EPUB conformance error. The contract explicitly leaves unmatched diagnostics as raw evidence.

Therefore independent agreement on the attribution contract is **not proof of complete EPUB conformance enforcement**. The corpus's `invalid/javascript` has an unmatched OPF-014 error, but native script detection already fails it; it is not an observed Base false positive. No current Base-PASS fixture has a failing external result. The concern is a source-confirmed untested acceptance route, not a fabricated exploit result. A's public `validate_reader` function also performs native-only validation; its PASS must not be confused with complete inherited publication validation supplied by the `validate_path`/external-tool route.

Before A RC, define how every applicable inherited EPUB ERROR/FATAL prevents an unconditional Base PASS while preserving honest diagnostic attribution. An unmatched diagnostic can make inherited conformance failed/incomplete without inventing a more specific SPD predicate. Review the blanket BASE-002 attribution scope and operational-error handling; do not simply map every arbitrary stderr line to a semantic failure. Add a fixture with an EPUB-only error such as missing required OPF metadata and no overlapping native security failure.

## Native security coverage is narrower than registration coverage

Both validators represent **113/113** requirements and register **74/74** automated checks in the frozen evidence. That does not establish exhaustive parser/security coverage. A's `validate_security` uses suffix-gated UTF-8 text/regex checks for literal tags/attributes and limited remote font/image/style patterns. It is not a complete XML/CSS-aware passive validator. B parses XHTML/SVG and tokenizes standalone stylesheets, but its reviewed path does not uniformly cover inline style attributes/style elements, every SVG embedding context, import-cycle graphs or every URL-bearing construct. Its `_is_remote` recognizes a finite scheme set; a positive package-local resolver is a safer policy boundary than enumerating hostile schemes.

ZIP mode/decoded-collision/overlap/actual-expansion gaps are detailed in [the threat model](threat_model.md). These findings warrant targeted tests and clarification under **either A or B**. EPUBCheck does not implement SPD's full passive profile and should not be expected to close these gaps.

## Validator A module impact

There are **8 source files** in the reviewed A source tree. Ratings below distinguish retaining A's boundary from B-min migration and C replacement. They concern behavior, not routine release version strings.

| File/module | A boundary only | B-min | C | Concrete effect |
| --- | --- | --- | --- | --- |
| src/package.rs | NONE | NONE for retained ZIP scan | REWRITE if container changes | B-min keeps ZIP rules; shared hardening may still change the scan under all options |
| src/strict_json.rs | NONE | NONE | NONE | Strict descriptor JSON stays |
| src/model.rs | NONE | LOW | MEDIUM | Review external evidence/profile labels and incomplete-result representation |
| src/lib.rs | NONE | LOW | LOW | Module/profile wiring if a replacement checker is added |
| src/policy.rs | NONE | LOW | MEDIUM | Revise imported-rule/tool attribution, retaining lifecycle guards |
| src/epubcheck.rs | NONE | LOW role change | LOW role change | Retain as diagnostic/export adapter; remove whole-source Base authority |
| src/validator.rs | NONE | HIGH | REWRITE at package/publication stages | Discovery/OPF/inherited-conformance orchestration and roll-up; retain inventory/projection/state/mapping/annotation algorithms |
| src/bin/spd-validator.rs | NONE | LOW | MEDIUM | CLI tool/profile configuration and reporting |

B-min counts: **2 source files unaffected, 5 with low changes, 1 with high changes**, plus new complete imported-publication validation responsibility. A's large validator.rs also contains `validate_inventory`, `projection`, `projection_render`, `descriptor_digest`, `validate_annotations` and `validate_mapping`: their algorithms are unaffected by B even though their containing file changes. Do not call that a full validator rewrite.

For the common passive/pre-RC package, A is **HIGH in the security-checking component**, **MEDIUM in orchestration/attribution**, and retains the semantic algorithms. Replacing the regex security function with grammar/context-aware checking is more than a prose-only update. The overall A clarification package is rated **HIGH**, bounded to the security/package-validation surface rather than architecture redesign.

## Validator B module impact

There are **19 Python source modules**. B-min can preserve the existing `PackageDocument`/`SecurePackage` interfaces and OPF grammar; changes to an adapter do not force a new semantic model.

| Module(s) | Count | B-min rating | Concrete effect |
| --- | ---: | --- | --- |
| __init__.py, __main__.py | 2 | NONE | Entrypoint behavior stays; routine version metadata excluded |
| xmlutil.py, strictjson.py, schemas.py | 3 | NONE for packaging | Safe parsing/schema infrastructure retained; accessibility field meaning reviewed separately |
| descriptors.py, integrity.py, mapping.py, annotations.py | 4 | NONE | Retain discovery-result/OPF interfaces and frozen semantics |
| semantics.py | 1 | NONE for packaging | Same content grammar and passive profile; shared hardening separately requires changes |
| package.py | 1 | NONE for B-min | Same ZIP gate/local resolver; shared security gaps remain |
| models.py | 1 | LOW | Review result/profile representation and external evidence semantics |
| constants.py, coverage.py, policy.py, cli.py | 4 | LOW | Pins, incorporation coverage, attribution and optional diagnostic configuration |
| epubcheck.py | 1 | LOW role change | Diagnostic/export rather than independent-source conformance authority |
| validator.py | 1 | MEDIUM | Internal marker check, external-tool gating and roll-up |
| epub.py | 1 | HIGH | Own complete incorporated OPF/nav/resource conformance beyond current extraction checks |

B-min counts: **11 modules unaffected for packaging, 6 low, 1 medium, 1 high**, plus replacement validation logic. Overall **HIGH** because dropping EPUBCheck's complete-source role transfers substantial inherited checks, despite many reusable modules. Under C, package.py/epub.py/discovery adapters need **REWRITE** at the boundary; validator.py and annotations/semantic resource-discovery adapters change, while JSON, identity, digest and mapping algorithms remain.

The A-boundary-only change is **NONE** for B. Its common passive/pre-RC work is **MEDIUM**: extend semantics.py/XML/CSS/reference traversal, package checks and validator.py/epubcheck.py/policy.py result handling; add focused tests. B's blanket DOCTYPE rejection also needs applicability review: a harmless HTML doctype and an external-entity dependency are not the same condition. Neither issue requires leaving EPUB. No whole-validator rewrite is indicated for A.

## New logic B would own

Preserving OPF parsing is not enough. B must cover incorporated OCF marker/headers/path rules; full package document grammar and required metadata; manifest properties and membership; spine/nav conformance and targets; core/foreign resources and applicable fallbacks; URI/XML and content integration; accessibility applicability/reporting; and complete diagnostic/operational status. These are the eight B rule groups in [the impact matrix](requirement_impact_matrix.md). They may reuse existing schemas/libraries or a controlled EPUB compatibility projection, but the projection's differences must be validated independently.

[EPUBCheck's CLI](https://www.w3.org/publishing/epubcheck/docs/cli/) supports partial OPF/nav/XHTML/SVG checks. Such checks omit whole-publication relationships. Under B they remain useful diagnostics for unchanged components and checks for exported EPUB; their success cannot certify the independent envelope. Simply ignoring all marker-related errors in a full run is not a specified independent validator.

## Rating summary and validation evidence

| Architecture / work | Validator A | Validator B |
| --- | --- | --- |
| A packaging decision alone | NONE | NONE |
| A plus proposed pre-RC passive/completeness work | HIGH, concentrated in security and inherited-result completeness | MEDIUM |
| B-min plus same passive work | HIGH; no semantic algorithm rewrite | HIGH; no semantic algorithm rewrite |
| C | REWRITE package/publication layer; retain model algorithms | REWRITE package/publication layer; retain model algorithms |

After implementation, rerun all 70 fixtures, added package cases, and existing meaningful validator checks. Review all 113 requirement statuses, keeping manual/history-dependent work honest. No new timing or line-count estimate is manufactured from module counts. The current 17 A tests, 57 B tests and 21 repository tests are **recorded prior evidence**, not tests rerun by this audit.
