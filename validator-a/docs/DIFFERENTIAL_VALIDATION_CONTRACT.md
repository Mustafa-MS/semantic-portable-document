# Differential validation contract

Independent validators compare the deterministic normalized surface only:

1. Base result;
2. results for claimed normative capabilities;
3. sorted unique failed requirement IDs;
4. sorted unique `NOT_TESTED` requirement IDs;
5. operational status.

Experimental presence, richer messages, evidence ordering below the documented
sort key, performance metrics, and absolute temporary paths are excluded. The
same Draft, registry/schema digests, options, Unicode data, and EPUBCheck version
must be used. This contract specifies no Validator B implementation choices.

## Normalized capability roll-up

- `PASS`: every applicable normative requirement necessary for the claimed
  capability has been positively established within the supplied evaluation
  scope, including required manual evaluation.
- `FAIL`: at least one applicable normative requirement has been established as
  failed.
- `NOT_TESTED`: no established failure exists, but at least one applicable
  normative requirement required for complete certification was not evaluated.
- `NOT_CLAIMED`: the document does not claim the capability.

Experimental capability presence/status remains separately represented by the
existing experimental result model.
