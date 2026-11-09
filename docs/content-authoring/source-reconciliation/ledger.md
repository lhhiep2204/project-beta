# T02 source reconciliation (generated)

Run `python3 scripts/validate_source_reconciliation.py --complete --self-test --write` after actual content review to regenerate; edit the adjacent JSON inputs.

**Status: complete for the delegated primary T02 review.** Structural checks and recorded linguistic self-review remain distinct; neither establishes human/release certification.

| Checked inventory | Count |
| --- | --- |
| vocabulary pages | 100 |
| source vocabulary rows | 2189 |
| mapped source rows | 2189 |
| excluded source rows | 0 |
| authored vocabulary mapped | 2211 |
| editorial additions | 1 |
| authored form links | 2264 |
| source grammar groups | 253 |
| linked pattern variants | 280 |
| source kanji definitions | 536 |
| source kanji units | 50 |
| source unit lexical rows | 1498 |
| mapped unit words | 1498 |
| mapped master examples | 826 |
| unit master links | 1257 |
| primary reviewed content files | 102 |

Open grammar locator range findings: 0.

The vocabulary denominator comes from 100 manually enumerated source pages. The 253 numbered grammar groups and Kanji source facts are frozen separately from their authored ID mappings. Kanji transcription seeds, curated dictionary-example scope, contextual-lemma normalization and fresh image comparisons are disclosed in the inventory/review.

The B-U-59 restoration of 41 lesson names is retained. T02 additionally restores 23 Kanji name occurrences and three counter readings with new IDs; all pre-existing IDs, PDFs and fixed dialogue scripts remain unchanged. See the correction log for form, provenance, terminology and bilingual edits.

## Evidence inputs

- [Source pages, lexical rows and numbered grammar groups](source-inventory.json)
- [Vocabulary dispositions and stable form/ID links](vocabulary-ledger.json)
- [Grammar, pattern, variant, example links and locator findings](grammar-ledger.json)
- [Kanji source definitions, unit readings and milestones](kanji-source-inventory.json)
- [Kanji unit/master/compound identity links](kanji-ledger.json)
- [Item-level content correction log](content-corrections.json)
- [Exact review scope and remaining work](review.json)
- [Machine validation report](validation-report.json)

## Limits

- Primary-agent linguistic self-review under B-U-51 is recorded as such; no independent human Japanese/translation certification is claimed.
- The denominator and source facts are manually reviewed evidence. Structural validation guards identities, forms, reading snapshots, relationships, coverage and revision drift; it cannot prove the absence of a human transcription or linguistic error.
- Kanji uses disclosed historical transcription seeds followed by fresh image comparison. It is not represented as a second independent original transcription or an exhaustive vocabulary inventory of all optional appendix illustrations.
- Only the assigned vocabulary/topic/unit/definition scope was reviewed; the entire 1451-page corpus, optional matrices, exercises, source passages and answer keys were not re-transcribed.
- The other 17 release languages and native kana integration, sentence-bank, voice/device and release acceptance remain separate. No application/browser/device/TTS/WidgetKit/performance/release acceptance follows from this content review.

Current task status is owned by [the owner HTML](../../index.html#T02).
