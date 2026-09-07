# Corpus 0.1.1 changes

70 fixtures: 18 valid, 39 invalid, 13 edge. Exactly one historical package changed; 68 are byte-identical. One negative was added. All 70 expectations have versioned reporting fields and fresh hashes, validated by the versioned infrastructure report schema; canonical Format schemas were not edited.

## Multi-spine repair and negative regression

The old positive repeated `n_article01` in chapter1.xhtml and chapter2.xhtml (line 4 each). The repaired positive retains `n_article01` in chapter 1 and uses `n_article02` in chapter 2. All addressable IDs are revision-wide unique. Both validators independently return Base PASS with no failures.

Old package SHA-256: `7e38a98b2c52e2552613cd5ef22046f1ee39c9ffc273a06470b1b0d712e0a5d3`.

New package SHA-256: `855c60d10d048f266fed92bb170312230740593f1d764486add64defe71d5cb7`.

The new `invalid/cross-spine-duplicate-node-id` is the exact old multi-spine package, preserving valid inventory and state bindings while isolating the duplicate. IDs are locally unique within each XHTML but `n_article01` repeats across the revision. Both return Base FAIL with exactly SPD-ID-006. EPUBCheck exits 0 for both packages: it does not treat cross-resource XML IDs as an EPUB error.

The chapter 2 resource hash/length, document projections, document resource binding, exact inventory binding and lifecycle descriptor JCS digest were recomputed and independently audited:

| Resource | Verified byteLength | Verified SHA-256 |
| --- | --- | --- |
| EPUB/chapter1.xhtml | 512 | sha256:ed07a7006f21d2045fa90c578a1517b63914f13ec7a325a23749c43239797800 |
| EPUB/chapter2.xhtml | 359 | sha256:306959906117606e0567228266ed9cfac5e8435c7d39d4b1a210a77787fbe337 |
| EPUB/nav.xhtml | 443 | sha256:c64ae88cd4188f701fd333296c8ab5e012e7907c4b00ee73052a4004bf8fa4b0 |
| EPUB/package.opf | 886 | sha256:2ad26aa77f4ed77e3f5c4cc37a329a88c8bc1a88a1eb828551692e4775c9e0e7 |
| EPUB/style.css | 95 | sha256:b68ee1ec263cff1ff6d3768be4598dfab0946fa8a44fd1f055614e30632552e2 |
| META-INF/container.xml | 621 | sha256:b7e4422f52b5bfaeea172c809bbb3516bc0f4c65b05660d54bad1e4e27af7004 |
| META-INF/spd/document-state.json | 607 | sha256:d56ec42009a21a2c45b8b01ca7a817b1346830857d2b29a5bfcf3ecd95c3a2ad |
| mimetype | 20 | sha256:e468e350d1143eb648f60c7b0bd6031101ec0544a361ca74ecef256ac901f48b |

semanticStateDigest: `sha256:e45345e4477d2bc14ed5a3d1d9d02aefe254854f8ecc214f9114628ebf350ba5`.

renditionInputDigest: `sha256:1e4bc8e098e670f65d415b3efc00cbbe222ac35b4e929cb79640f7548cae91f2`.

Exact inventory SHA-256: `sha256:88e603e0ba876661aacd468a7476981b4e4121ef1bd5e04a397804e1cc1f8e4e`.

descriptorDigest: `sha256:28da9b2ab6365b223270ffe8085f6e9b880a327484f6805b777fafa6b13a9fc3`.

Lifecycle is EDITABLE and fixed rendition is absent; there is no seal/fixed/mapping binding to regenerate. Existing document/revision identity is retained for this synthetic fixture repair.

## Oracle attribution changes

`invalid/stale-fixed-rendition` now expects SPD-STATE-007 instead of SPD-STATE-001. Mapping depends on current fixed output; the fixture supplies no processor-behavior evidence. Its package bytes and FAIL verdict did not change.

The oracle is authored by `build_corpus.py` from preserved expected files, actual descriptor bytes, the shared contract, and the explicit reviewed predicate table. It never reads either validator's outputs. `oracle-review-decisions.json` lists all 70 old/new failed-ID sets, including unchanged rows. These are every failed-ID expectation change:

| Fixture | Historical expected IDs | Reviewed expected IDs |
| --- | --- | --- |
| invalid/bad-resource-hash | SPD-INT-003 | SPD-INT-003, SPD-INT-004, SPD-INT-005, SPD-RES-004 |
| invalid/duplicate-normalized-path | SPD-BASE-002 | SPD-BASE-002, SPD-RES-002 |
| invalid/event-handler | SPD-SEC-001 | SPD-ID-006, SPD-SEC-001 |
| invalid/mapping-invalid-geometry | SPD-MAP-011 | SPD-MAP-011, SPD-MAP-012 |
| invalid/mutation-asset | SPD-INT-003 | SPD-INT-003, SPD-RES-004, SPD-STATE-003 |
| invalid/mutation-css | SPD-INT-003 | SPD-INT-003, SPD-RES-004 |
| invalid/mutation-fixed | SPD-INT-003 | SPD-INT-003, SPD-RES-004, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007 |
| invalid/mutation-mapping | SPD-INT-003 | SPD-INT-003, SPD-RES-004, SPD-STATE-002 |
| invalid/mutation-semantic | SPD-INT-003 | SPD-INT-003, SPD-RES-004, SPD-STATE-003 |
| invalid/path-traversal | SPD-BASE-002 | SPD-BASE-002, SPD-RES-002 |
| invalid/sealed-after-annotation-modification | SPD-ANN-004 | SPD-ANN-004, SPD-INT-003, SPD-RES-004 |
| invalid/sealed-after-semantic-modification | SPD-STATE-003 | SPD-INT-003, SPD-RES-004, SPD-STATE-003 |
| invalid/stale-fixed-rendition | SPD-STATE-001 | SPD-STATE-007 |
| invalid/unlisted-non-normative-resource | SPD-RES-006 | SPD-RES-003, SPD-RES-006 |
| invalid/unlisted-normative-resource | SPD-RES-003 | SPD-RES-003, SPD-RES-006 |
| invalid/cross-spine-duplicate-node-id | — | SPD-ID-006 |

All expectations add corpusVersion, operational status, authority status and NOT_TESTED sets. All retain ID-013 NOT_TESTED for absent lineage evidence; Accessible adds ACC-001/004. Invalid XHTML blocks ID-006; missing/conflicting authority uses the contract's explicit blocked groups and UNKNOWN capabilities, not empty claims. Experimental expectations are derived from actual explicit declarations, separate from physical presence; legacy scenario metadata is not claim authority. No normative requirement was reclassified.

Use this versioned builder and oracle for convergence. Historical corpus/freezer scripts remain historical artifacts and must not be used to overwrite the old freezes. The historical archive preserves all pre-repair expectations and package bytes.
