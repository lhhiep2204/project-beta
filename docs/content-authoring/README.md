# Editorial content authoring

This is draft 0.1 of a development-time authoring format for the approved 50-lesson and 50-unit Vietnamese/English batch. Lessons 1 and 26 were the initial samples. It is a concrete review artifact under B-U-03/04/15/18/19/24/48/50 and the source inventory. It does not select the app runtime package, persistence schema, content-update policy or public module contract. The owner separately confirmed independent per-level learned prefixes in B-U-58; preserve source lesson numbering and milestone references when adopting these drafts for runtime use.

## Browse the content

- [Current lesson and Kanji content index](content-index.md).
- [Source corrections, all seven confirmed by the owner](source-corrections.md).

## Initial samples

- [Lesson 1: introductions](lesson-01.md), with [structured JSON](lesson-01.json).
- [Lesson 26: explanations and requests](lesson-26.md), with [structured JSON](lesson-26.json).
- [Draft JSON Schema](authoring.schema.json).
- [Editorial findings and delegated self-review record](editorial-review.md), with [item-level records](editorial-review.json).
- [Targeted source-image comparisons](source-checks.json) and [structural validation result](validation-report.json).
- [PDF reference inventory](../reference-inventory/README.md) and [OCR pilot](../reference-inventory/ocr-pilot/README.md).

The current versions of the two initial samples contain 92 vocabulary entries with variants/senses, 12 editorial grammar points, 13 sentence patterns, 27 original examples and two original dialogues. N5 includes all six source grammar groups; N4 includes all four, with explanatory group 1 split into three smaller teaching points. Both initial samples include the common vocabulary and useful phrases from their two lesson vocabulary pages. Proper names in the assigned vocabulary pages are retained under B-U-59. Full supplementary reference matrices, source passages and exercises are excluded. The sample counts do not represent the full batch.

## Authoring structure

| Component | Representation and reason |
| --- | --- |
| Editorial identity | Opaque UUIDv4 for each lesson/item/grammar/pattern/example/dialogue. Preserve on edits. Lesson numbers and editorial keys are navigational labels, not generated IDs. These stable authoring IDs are retained by the implementation design in ../engineering-contract.md; runtime adoption is still pending. |
| Japanese text | Ordered `segments`, each with `base` and contextual `ruby` when it contains Kanji or a source-written uppercase Latin abbreviation such as CD/ATM/JR. This preserves the printed spelling and its Japanese reading without replacing the spelling with kana. Plain text is the concatenation of base strings; it is not redundantly stored. Ruby may cover a whole compound or a Kanji segment followed by unannotated okurigana. |
| Kana reading | Vocabulary `kana_reading` must equal the concatenated ruby/base reading. It is an orthographic kana reading, preserving written particles such as は; it is not a phonetic TTS override. The は→わ pronunciation is explained in the lesson. |
| Forms and senses | A vocabulary entry has named forms, register and meanings linked to form keys. `見る/診る` use distinct sense-to-form links. Polite and dictionary forms remain separate; dictionary forms are editorial conjugations from printed polite forms. |
| Bound forms | Suffixes and expressions containing 〜 are explicitly typed. 〜 is a placeholder in these entries, not a character to pronounce literally. Sentence templates use typed slots rather than searching/replacing arbitrary text. |
| Verb groups | I/II/III are separate data, rather than part of a Japanese string. Targeted checks preserve みます as II and れんらくします as III against the source image. |
| Grammar and templates | Grammar explanations link to source topic groups. Sentence patterns link to grammar and declare slots. Templates carry explicit variants, including じゃありません / ではありません. Examples identify a pattern and variant. |
| Example context | Optional English/Vietnamese `context` states the situation for interpreting a sentence; it is separate from the spoken Japanese and its translation. |
| Examples and dialogues | Newly authored Japanese sentences with contextual ruby and English/Vietnamese translations. Dialogues declare speakers and references to relevant grammar. Reference locators align the skill/topic; they do not assert that original dialogue wording came from the PDF. |
| Search-only romaji | Aliases are vocabulary metadata. They are omitted from the readable teaching samples. No search normalization/ranking algorithm is selected. |
| Translations | English and Vietnamese are authored. The other 17 approved release languages remain explicitly missing. English fallback approval does not make the full localization gate complete. |
| Provenance | Source ID and inclusive one-based PDF pages resolve through the reference catalog. Source facts/readings are distinct from independently authored explanations/examples/dialogues/translations. |
| Review state | Primary source comparison completed for the listed forms/topics. Independent Japanese/translation review is pending; every sample is `draft_not_for_release`. |

No PDF images, OCR dumps, runtime dependencies or app resources were added to these samples. Existing reference extraction remains in its own directory. No claim of independent linguistic, release-rights, device, rendering or TTS acceptance follows from structural validation.

## Validate

From the repository root:

```sh
python3 scripts/validate_authoring_samples.py --self-test --report docs/content-authoring/validation-report.json
```

The validator uses Python’s standard library. Its schema walker supports the keywords used by this draft and rejects unsupported keywords; it is not a general JSON Schema implementation. It checks required fields/types, opaque IDs, references, slot/template variants, speaker links, kana/ruby consistency, declared language gaps, draft state, source page bounds and all six PDF hashes. Twelve short, visually checked source anchors guard recurring OCR errors. Sixteen negative fixtures exercise incorrect data; no application build is required for these document/data changes.

Structural checks cannot judge whether a newly written sentence is natural, whether all translations preserve nuance, or whether a contextual reading sounds correct on an actual Japanese voice.

## Bounded editorial review procedure

1. Compare each lexical form and printed verb group to the source image, keeping variants and annotations separate. Mark uncertain readings explicitly; do not fill them from raw OCR.
2. Review the new explanation, examples and dialogue as teaching content, including prerequisite vocabulary, politeness, intended context and translation equivalence. Confirm kana/ruby in context.
3. Apply the primary-agent self-review gate delegated by B-U-51. Record item IDs, findings and corrections; confirm concrete uncertainties with the owner. This supersedes waiting for owner manual approval and is not independent human certification.
4. Resolve findings, retain editorial IDs, rerun validation, then assess additional language coverage and release gates. Adopt an app runtime schema and update semantics only through the separate approved architecture process.

The two samples have passed the delegated self-review gate for batch authoring; see the [review record](editorial-review.md). The current batch covers 50 lessons and 50 Kanji units, Vietnamese/English first, with all common reference vocabulary including source proper names under B-U-59 (superseding the name exclusion in B-U-53). Raw OCR remains reference material, not authored app content. Other languages and release acceptance remain separate gates.

## Kanji and readable outputs

The `kanji/` directory separates 536 character definitions from 50 unit reading lists. Units can reuse earlier characters; units 21–25 are preparation/review through the preceding volume’s lesson 25. On/Kun preserve the reference-listed subset with approved source corrections. All seven Kanji/translation correction decisions are confirmed and closed under B-U-57, superseding the B-U-55/56 open-flag disposition. Extra characters inside a contextual word do not create a fabricated character master.

```sh
python3 scripts/validate_authoring_batch.py --complete --self-test --report docs/content-authoring/batch-validation-report.json
python3 scripts/render_authoring_content.py
python3 scripts/render_authoring_content.py --check
```

Use `--complete` at the final 50-lesson/50-unit gate; omit it during authoring. Readable Markdown is generated from canonical JSON. Source discrepancies and review flags remain in the separate correction ledger, with links on affected lesson and Kanji pages. Editorial IDs and schemas remain draft authoring tools, not an approved runtime storage or migration contract.

## Current Vietnamese/English batch

The authored set contains **50 lessons, 2,212 vocabulary entries, 255 grammar points, 278 typed sentence patterns, 304 original examples and 50 original dialogues**, plus **50 Kanji units and 536 character definitions**. Kanji word lists contain 2,324 occurrences (1,498 unit words and 826 master examples); this is not a distinct-headword count across repeated units.

T02 now records the delegated primary review of all 102 lesson/unit/master files for source alignment, contextual reading/ruby and VI/EN meaning. Its [ledger](source-reconciliation/ledger.md) maps 2,189 source vocabulary rows, 253 numbered grammar groups, 536 definitions and all 1,498 assigned unit lexical rows; all 826 curated master examples have source links. All 28 grammar locator findings are resolved. The [item/field correction log](source-reconciliation/content-corrections.json) preserves identities and before/after evidence. Kanji transcription seeds and fresh image comparison are disclosed; this is primary self-review rather than independent human certification. Optional supplementary reference matrices and unselected dictionary illustrations, source reading passages, exercises and answer keys are excluded. Proper names are retained regardless of fictional status. Keep source spelling, identity and contextual reading; distinguish fictional entities in meanings/context and never merge homonymous names. Existing original dialogue characters are authored identities, not automatic replacements for textbook characters. The source’s full dialogue and passage wording is not repackaged.

See the [batch review](batch-review.md), [coverage record](batch-source-coverage.json) and [structural validation](batch-validation-report.json). Cross-agent review includes final corrective rechecks; its exact scope and limits are recorded. The owner confirmed applying all seven source-note values under B-U-57; their recheck flags are closed and source provenance remains visible. Other 17 languages, independent human language review, runtime schema adoption, ruby/TTS/device checks and release acceptance remain separate work.

## Proper-name correction, 2026-11-08

Owner decision B-U-59 restores 41 names from 38 previously excluded source rows in 19 lessons. Each row was visually checked on its original vocabulary page (19 pages total). The source-row mappings and item IDs are in [the review record](source-reconciliation/proper-name-review.json). All 50 lesson inventories and 50 unit/master identity relationships receive structural checks; this is not a new independent linguistic review of all sentences or source pages. Historical sample/peer reviews predate these additions.
