# T04 sentence bank and speech authoring

P0-T04 authoring is complete under B-U-51 primary self-review. The task authority remains [the owner HTML](../../index.html#T04). The [generated inventory](inventory.md) and [revision-bound report](validation-report.json) expose the actual completion result; they do not establish native application or release acceptance.

## Canonical inputs and identities

- `identities.json` owns the opaque UUIDv4 overlay for forms, senses, teaching targets and speech records. All original curriculum UUIDs are preserved. Exact JSON pointers and full-item source hashes bind the overlay to its source revision. Dictionary forms have separate form IDs linked to their original senses. Never regenerate this registry to hide drift.
- `bank.json` owns 3,275 reviewed complete contextual sentences/utterances: 304 retained original examples and 2,971 new examples. The originals retain their UUIDs, Japanese, translations, context and speech. Complete-span analysis names lexical form/sense IDs and supporting grammar; simplicity is editorial metadata. Only reviewed candidates enter the reference oracle.
- `word_bindings` links every source-owned Kanji lexical occurrence to explicitly reviewed equivalent vocabulary form/sense targets or an exact source lexical fact. Repeated source identities remain separate. Source-curated master-example UUID relations establish character correspondence; the sentence must also display that character. A glyph/substring check alone never certifies meaning.
- `bare_character_bindings` contains 122 primary-reviewed character/word pairs. Only the actual bare character meaning being taught may be new. A compound, another same-glyph sense or unrelated supporting grammar is not exempted. The validator requires the applicable taught-target exception rather than counting that target as unfamiliar support.
- `support_lexemes` identifies the existing authored names and additional contextual lexical facts. Actual lesson introductions require revision-bound content evidence. A word's occurrence in a sentence or unlocked Kanji unit does not by itself prove it was taught. Context-only words and the observed third-person-desire construction remain unintroduced and unfamiliar. The 60 reviewed repeated-lexeme groups may share actual introductions; they never merge IDs, senses, favorites or N5/N4 prefixes.
- `bound-contexts.json` owns 155 separately authored complete pronunciation contexts, each with exact form linkage and VI/EN labels. A word-only context receives no sentence coverage credit. `bank.schema.json` describes the bounded authoring interface; the validator supports the JSON Schema keywords used here, not arbitrary extensions.
- `speech.json` owns 5,616 exact speech records, including 466 separate dictionary forms. Source orthographic readings inherit T02's pinned primary review. Explicit contextual particle edits preserve lexical は/へ and project particles once. Latin abbreviations use contextual ruby, without concatenating base and ruby. Bound records pin the exact reviewed context digest; labels and translations are never spoken. Bare On/Kun playback is not added.
- `review.json` pins every reviewed candidate, speech record and context. Its continuation batches disclose the primary review and refinements. `history/initial-*.json` preserves the incomplete starting handoff. Validators regenerate reports only; they cannot create or refresh editorial pins.

The complete denominator is 6,126 targets: 2,731 vocabulary forms/senses (including 466 dictionary forms), 255 grammar points, 280 pattern variants, 536 characters and 2,324 Kanji lexical occurrences. The [coverage ledger](coverage.json) has zero missing targets. These are source surface identities, not counts of distinct Japanese words or proof of all possible dictionary senses. The bound denominator is 114 vocabulary entries / 120 forms plus 35 Kanji lexical occurrences. The historical count of 53 missed U+FF5E and marker-free readings.

## Selection and speech boundary

The Python oracle derives familiarity from genuinely taught vocabulary/grammar in the two independently marked lesson prefixes. It ranks by unfamiliar supporting grammar, unfamiliar supporting words, reviewed simplicity, Japanese length, then stable authored order/ID. Target exceptions are exact and scoped. Context-only knowledge stays unfamiliar; when all matching examples have unfamiliar support, the best corresponding reviewed example remains available.

Selection returns at most three genuine examples. It suppresses duplicate displayed/spoken sentences and identical spoken VI/EN content with alternate orthography, while preserving distinct contextual readings such as 一日 (いちにち / ついたち). Forced search inclusion occupies one of the same three slots. Duplicate suppression does not create semantic correspondence. Dialogue scripts remain fixed and unchanged.

`resolve_form_speech` requires the exact entity/form/sense tuple. Wrong pairs, missing contexts, stale source readings or changed unreviewed contexts return unavailable; a future native caller can keep the form and meaning readable. It never defaults to the first form or sense.

These are offline authoring tools. T08.05 owns native selection and visible snapshots; T05 owns ruby/playback/voice evidence. T01's draft runtime boundary and zero candidate/speech index versions remain unchanged. No authoring file has been bundled into app resources. No voice listening, iOS application, device/performance, independent-human, other-17-language or release acceptance is claimed.

## Generate and validate

```sh
python3 scripts/validate_sentence_bank.py --complete --self-test --write
python3 scripts/validate_sentence_bank.py --complete --self-test --check
python3 scripts/render_authoring_content.py
python3 scripts/sync_project_review.py
python3 scripts/audit_project_docs.py
```

`--write` regenerates validation and coverage reports only. After an actual editorial review, update the relevant records and review pins explicitly, preserving historical evidence. `--check` rejects stale reports, identity/source drift and changes after review. `--complete` requires every target to have reviewed matching candidates, complete candidate annotations and reviewed speech records. Structural validation is distinct from the recorded primary semantic review and from native/release acceptance.
