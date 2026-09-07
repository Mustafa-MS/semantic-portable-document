# Experimental capability reporting — NON_NORMATIVE

24 of 69 fixtures differ; 45 agree. All differences are Fixed-Experimental: A=PRESENT_EXPERIMENTAL, B=NOT_CLAIMED. Archive-Experimental agrees throughout. These statuses are excluded from every normative agreement metric.

In every differing package the authoritative declaration is exactly Base + Mapping, without an explicit Fixed-Experimental claim; fixed.pdf exists. A reports physical fixed-rendition presence; B reports explicit capability claims. The Draft permits Mapping without a separate Fixed-Experimental declaration (§§34,54,56–57). Neither presence nor a Mapping dependency creates that explicit claim.

Source explanation, after byte inspection: A validator.rs:1296–1307 tests fixed status != absent; B validator.py:94–97 tests capability membership. This is a future report-model consistency issue, not a normative conformance failure. Prefer separate fixedRenditionPresent and fixedExperimentalClaimed fields; neither means PDF conformance was tested.

| Fixture | Explicit claims | Fixed status | A | B | Severity |
|---|---|---|---|---|---|
| edge/combining-character-range | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| edge/emoji-range | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| edge/node-not-visible | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| edge/partial-mapping | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| edge/rtl-range | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| edge/unsupported-mapping | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-invalid-geometry | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-invalid-page | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-invalid-range | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-with-stale-fixed | Base, Mapping | stale | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-wrong-rendition | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mapping-wrong-revision | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mutation-asset | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mutation-css | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mutation-fixed | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mutation-mapping | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/mutation-semantic | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/not-visible-reason | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/partial-mapping-reason | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/sealed-after-semantic-modification | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| invalid/stale-fixed-rendition | Base, Mapping | stale | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| valid/mapped | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| valid/mapping-with-current-fixed | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
| valid/sealed | Base, Mapping | current | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |
