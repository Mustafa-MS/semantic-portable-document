# Unicode Environment Impact

Environment: Python 3.13.3, `unicodedata` 15.1.0.

Classification: `IMPLEMENTATION_ENVIRONMENT_DIFFERENCE`

Result: `NO_OBSERVED_CORPUS_IMPACT`

Validator B explicitly tested Arabic, mixed bidi, combining-character ranges, emoji, a ZWJ sequence, Indic characters, CJK, the vertical-writing fixture, NFC package paths, and Unicode-scalar-value offsets.

Corpus scan evidence:

- 69 packages scanned; no decoded normative text contained surrogate code points or Unicode-15.1-unassigned characters.
- Arabic-name code points: 148; Devanagari-name code points: 4; CJK-name code points: 9; Hiragana-name code points: 4.
- One resource contains a ZWJ sequence and executes without range failure.
- Exactly one non-NFC package path exists, in the intentional `invalid/duplicate-normalized-path` fixture; it is deterministically rejected.
- `valid/arabic`, `valid/mixed-bidi`, `edge/combining-character-range`, `edge/emoji-range`, `edge/rtl-range`, and `edge/cjk-vertical` produce no Unicode-related violation.
- The source-order oracle detects `SPD-I18N-001` in `invalid/visual-order-arabic-source`.
- Synthetic scalar tests establish: combining `e + U+0301` is two scalar values, one supplementary-plane emoji is one, `woman + ZWJ + laptop` is three, and a Devanagari consonant/virama/ZWJ/consonant sequence is four.

Scalar-value counting does not use grapheme segmentation tables. Valid parsed XML/JSON is checked for surrogate exclusion before Python `len()` is used as the scalar count. NFC is applied only where the Draft requires it for paths and never to authoritative text or resource bytes.

