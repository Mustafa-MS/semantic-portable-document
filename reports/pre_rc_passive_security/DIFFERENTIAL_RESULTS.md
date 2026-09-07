# Independent validator reconvergence

- Validator A 0.1.0-draft.3 ↔ Validator B 0.1.2: **107/107** exact agreement.
- Validator A ↔ reviewed oracle: **107/107**.
- Validator B ↔ reviewed oracle: **107/107**.
- Experimental and authoritative-claim reporting: **107/107** exact agreement.
- Base results: {'PASS': 48, 'FAIL': 58, 'NOT_TESTED': 1}.
- Final operational status: 105 COMPLETE, one MALFORMED_INPUT and one RESOURCE_LIMIT, as independently specified by the operational fixtures; no INTERNAL_ERROR.
- Manifest SHA-256: `943e9794e756b07e3180651329d78aa3bc7522c769f94457083b1d009a7bb7cc`.

Compared fields: Base, normative capabilities, failed requirement IDs, NOT_TESTED IDs, operational status; also experimental capabilities, fixed reporting and known/unknown authoritative claims. Both implementations evaluated identical package bytes. Source identities were stable during each accepted evaluation. The oracle is derived from reviewed requirements/profiles, fixture bytes and direct EPUB diagnostic attribution, not validator consensus.

No historical Base-PASS fixture became invalid under the clarification. All 70 historical packages are byte-identical. New human/processor NOT_TESTED obligations are disclosed without claiming runtime PASS. Corpus 0.1.1 expectations and historical convergence remain immutable.
