# Kana authoring — P0-T03

Canonical text and identities live in [inventory.json](inventory.json), governed by [kana.schema.json](kana.schema.json). The generated [readable inventory](inventory.md) is embedded in the single [owner HTML](../../index.html#curriculum). Edit JSON, never the generated Markdown. Existing IDs are opaque UUIDv4 and must survive corrections; labels and table positions are not IDs.

The primary agent reviewed 301 entries and their 301 examples in English/Vietnamese under B-U-51/52. The [source inventory](source-inventory.json) records the source-cell denominator, item IDs, locators and explicit exclusions. The [review](review.json) pins all three input documents and every entry/example to that bounded self-review. No independent-human certification is claimed.

## Coverage

| Area | Learning | Separate reference |
| --- | --- | --- |
| Hiragana | 46 basic, 25 voiced/semi-voiced, 33 common contracted, 9 small/geminate, 7 long-vowel patterns, 3 particle contexts | 12 including the 3 conditional contracted spellings |
| Katakana | 46 basic, 25 voiced/semi-voiced, 33 contracted, 33 extended, 9 small/geminate | 17 rare/historical/alternative forms |
| Shared | 2 voicing marks and 1 length mark | 0 |

The official modern tables contribute 71 direct/nasal cells and 36 contracted cells, including the conditional ぢゃ/ぢゅ/ぢょ forms. Katakana retains all 107 modern counterpart cells, including ヲ/ヂ/ヅ and conditional ヂャ/ヂュ/ヂョ in reference, without claiming those three are ordinary loanword table cells. The official loanword extensions contribute 13 Table 1 and 20 Table 2 cells. Supplemental usage/reference items have explicit ledger rows. Do not infer completeness from the 57 prototype fixtures.

This is the reviewed standard-Japanese source scope, not every conceivable transcription of a foreign sound or every Unicode script extension. Empty gojuon cells are not sounds to invent. Hentaigana, Ainu extensions and arbitrary expressive spelling are not claimed as enumerated; kana punctuation has no independent syllable. Combining voicing marks are encoding aliases, not extra teaching sounds.

## Context and playback handoff

- `speech.mode=syllable` identifies a reviewed complete syllable/combination; `text` is the glyph. `context` identifies a complete example reading. Never derive a dependent mark's audio by speaking its glyph.
- Examples use the existing segmented Japanese/ruby convention, plus a complete orthographic Hiragana reading. Katakana readings are script-normalized; particle readings preserve spelling. Native speech must handle their contextual pronunciation and be verified in T05/T08.
- `target_relation` distinguishes literal containment, composed voicing, vowel-row patterns, old spelling, expanded repetition/ligatures and explicitly labelled modern equivalents. Rare ゕ/ゖ demonstrate their full-size base in a real word; the inventory does not invent ordinary word spellings containing those small glyphs.
- `phonetic_transcription` examples explicitly teach a sound in the other script; they are not mislabelled as ordinary loanword orthography. Proper names remain when the rare combination lacks an easier everyday example. Conditional ぢ forms normally share the corresponding じ sounds in modern standard Japanese.
- English/Vietnamese guidance distinguishes modern speech from historical spelling; no reconstructed historical accent is asserted. All examples are fixed basic contexts, independent of learned prefixes. No new kana favorite type or learned state is introduced.
- The context list supports at most three examples per target. Each example retains its own UUID. Future native clients must consume this data and preserve the approved UI grouping; T03 does not modify the runtime format or install app resources.

## Maintain and verify

After an editorial change, perform a real primary content review before updating `review.json`. Recompute the affected item/input digests only for content actually reviewed. The validator never creates review approval; `--write` writes a validation report only.

```sh
python3 scripts/validate_kana.py --complete --self-test --write
python3 scripts/render_authoring_content.py
python3 scripts/sync_project_review.py
python3 scripts/validate_kana.py --complete --self-test --check
python3 scripts/render_authoring_content.py --check
python3 scripts/sync_project_review.py --check
python3 scripts/audit_project_docs.py
```

The 25 negative fixtures exercise missing/duplicate IDs, wrong source coverage, reading mismatch, unsupported language/learned/romaji fields, isolated marks, a wrong simple-sound example, the example cap and stale/incomplete self-review. Semantic fixtures run without review hashes, so an unrelated stale-hash failure cannot stand in for a semantic check.

The other 17 languages, voice listening, native rendering/playback, runtime integration, device/performance and release gates remain separate. Existing lesson/Kanji historical evidence is not rewritten as a kana review.
