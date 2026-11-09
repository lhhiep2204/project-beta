# Documentation and source audit

Current review revision: `16b0c0dcd02a093cb63f9510eb062165748f6a719c3d5ebf08855dd049e4efa8`. Date: 2026-11-09. Generated; edit docs/index.html contract for product/status changes.

## Scope and evidence

All 279 pre-consolidation files are enumerated with hashes in baseline-manifest.json. Lesson/Kanji structural checks and the separate kana authoring validator define their own evidence scopes; generated readable content is checked. All six PDF hashes and page counts match the catalog. The 2026-11-07 audit visually rechecked seven source pages; the 2026-11-08 proper-name review checks 38 rows on 19 pages. Prior author/cross-agent evidence is historical, not a new independent full-corpus review.

Current counts: `{"vocabulary": 2212, "grammar_points": 255, "sentence_patterns": 278, "examples": 304, "dialogues": 50, "lessons": 50, "units": 50, "characters": 536, "source_pages": 1451, "source_grammar_groups": 253, "bound_entries": 114, "kanji_word_occurrences": 2324, "editorial_bytes": 29881825, "unit_word_occurrences": 1498, "character_example_occurrences": 826}`.

H02 (legacy T02) records 2189 vocabulary rows,253 grammar groups,536 definitions,1498 unit words and826 master examples with primary VI/EN/reading review of102 files; see its revision-bound evidence below. This is not independent human certification. Kana authoring has a separate 301-item primary review. Native kana/candidate integration and remaining locales stay open; H04 authoring evidence is reported separately.

## Findings

Completed P0 foundation groups are retained as handoff documentation and omitted from the execution roadmap. The completed former T01 proof is retained as a handoff; remaining development groups use the current IDs. P1 translation/audio work belongs to development, app/performance acceptance to acceptance, and sign-off to release. Track these in their owning tasks rather than duplicate them as current documentation issues. Preserve open finding status, dependencies and execution evidence; hiding a scheduled issue does not resolve it. P0/P1 are priorities, distinct from execution phases. Current task IDs follow DOC-PLAN-06; the completed native/audio group is no longer an execution task.

## Proper names — B-U-59, 2026-11-08

Restored 41 names from 38 rows on 19 visually checked source pages. The source spelling, contextual reading, VI/EN entity description and stable identity are recorded in [the item-level review](../content-authoring/source-reconciliation/proper-name-review.json). All 2189 vocabulary ledger row targets resolve to the correct lesson/form. This focused check does not certify every source row or sentence.

## Validation limits

- No independent full re-transcription of 1451 source pages.
- Assigned-scope primary source/VI/EN/reading review completed under B-U-51; independent human full-corpus certification is not claimed.
- Kana and sentence-bank authoring have separate revision-bound primary reviews; native playback/integration remains open.
- Other 17 languages and independent linguistic/release review pending.
- Current browser visual/interaction QA was blocked by the URL policy rejecting local file:// access; no bypass attempted.
- T01 physical audio closure uses two real-driver iPhone tests and explicit owner manual listening/actual-event confirmation. Physical UI automation did not execute; exact voice identifier and headset model were not recorded. Full application/performance/release acceptance remains separate.

The same conclusions, priority tasks and owner proposals are readable in [the only owner HTML](../index.html).

## H04 authoring handoff (legacy T04)

3275 dependency-complete candidates cover 6126/6126 targets; 0 remain in the gap ledger. 5616 speech authoring records include 466 dictionary forms and 155 bound contexts. Authoring completion: True. See [the inventory](../content-authoring/sentence-bank/inventory.md) and [revision-bound validation](../content-authoring/sentence-bank/validation-report.json). Python reference fixtures and primary reading review are not native voice/application acceptance.

## H03 kana authoring (legacy T03)

301 entries with VI/EN contexts, source-table denominator and revision-bound primary self-review; 29 remain in a separate reference group. See [kana authoring](../content-authoring/kana/README.md) and its [validation report](../content-authoring/kana/validation-report.json). No native voice or release pass.

## T01 physical audio closure — 2026-11-09

Two real-driver integration tests passed on physical iPhone 18 Pro / iOS 27.2. The owner explicitly confirmed the complete offline/silent and real interruption/headset/background cases. See [the physical audio report](t01-02-physical-audio-validation.json) for exact prompts, owner replies and revision-bound native results. Manual audio is owner-observed; there is no agent recording or physical screenshot review. Physical UI automation was blocked before execution by the free-profile app limit. Historical Simulator reports remain unchanged; no full-app or release acceptance is implied.

## H02 source/content review (legacy T02)

Completed the B-U-51 primary source/VI/EN/contextual-reading review of all 102 lesson/unit/master files: 2,189 vocabulary rows,253 grammar groups,536 definitions and 50 Kanji units (1,498 unit words plus 826 curated master examples). Resolved 28 grammar locator findings, restored 23 Kanji surname occurrences and 3 counter readings; all 6033 prior IDs and 50 dialogue objects retained. This is recorded primary self-review, not independent human or release certification.

The primary review compares100 vocabulary pages,100 grammar explanation pages,104 Kanji unit reading pages,82 definition pages and12 milestone/header pages. Inspect [the detailed review boundary](../content-authoring/source-reconciliation/review.json) and [the ledger validation](../content-authoring/source-reconciliation/validation-report.json). Recorded primary source/VI/EN/contextual-reading acceptance is distinct from machine integrity checks. Optional dictionary illustrations are not exhaustive. No independent human, native voice/device or release certification is implied.
