# T09.01 localization infrastructure

Product authority: [owner review](../index.html#T09.01). This handoff implements offline lookup and validation, not translation or release approval.

`BetaRuntime.ContentLanguage.resolve(preference:preferredLanguages:)` accepts the persisted shared choice, with nil meaning System. Pass its single result to both `ContentPackage.localizedField(id:pointer:language:)` and `SearchIndex.search`. System scans supported language families in device preference order, then English; an explicit unsupported preference fails. Simplified Chinese matches Hans/CN/SG, not Hant/TW/HK/MO. Japanese is the taught language, not a selectable interface locale. Arabic/Hebrew expose RTL; Sino-Vietnamese display is enabled only for Vietnamese.

Lookup reads one entity shard. Each translated field selects nonblank requested text, otherwise nonblank English, otherwise unavailable. `LocalizedContent` returns the actual language and `isEnglishFallback`; do not guess fallback from equal text. It never borrows Vietnamese for another locale. This does not mutate saved state, Japanese text, readings, entity IDs or candidate snapshots. T06 owns committed shared-preference wiring and application runtime integration; T07 owns search sessions/IME/debounce.

## UI resources

The native `Interface.xcstrings` catalog owns the four implemented scaffold titles, the English fallback label and one result-count plural resource. All six have English source values; other locale UI translations remain absent. The catalog is intentionally scoped to implemented UI. Future screens must add their strings here; this is not a six-string denominator for the final app. DEBUG-only T05/T09 harness diagnostics are excluded from product translation coverage.

`LocalizedContentText` renders the resolved field verbatim, wraps long content and shows the concise catalog label only for an actual English fallback. Pass `result.text` and `result.isEnglishFallback` from the same field; handle unavailable content at the owning screen. `JapaneseContentBlock` keeps its Japanese subtree LTR while the surrounding navigation/layout remains RTL. These are reusable presentation seams; they do not add a second language preference. Runtime adoption/Settings persistence remains T06 work.

[Apple's String Catalog guidance](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog) informs the native resource/plural implementation. The validator checks printf argument positions/types, escaped percent, complete cardinal categories and catalog shape. Category inventories were checked against [Unicode CLDR](https://github.com/unicode-org/cldr/blob/main/common/supplemental/plurals.xml) on 2026-11-09. Real locale batches must also compile and test with the selected Apple SDK; synthetic category fixtures are not translated resources.

## Content locale sidecars

VI/EN text remains canonical in the existing authored JSON. Its reviewed schemas and historical review pins are unchanged. For a remaining locale, create `docs/localization/content/<locale>.json` following [content.schema.json](content.schema.json). Each row identifies a canonical path, JSON pointer to an existing translated field, nearest owner ID/key, exact owner `sourceSha256`, text, draft/reviewed state and reviewer. Do not create a second curriculum or replace source IDs. A nonempty English source is required; an empty optional usage note is not permission to invent new copy.

Use `translation_overlays.field_at(document, pointer)` to obtain the field and its nearest owner; `translation_overlays.pin(owner)` computes the required digest (UTF-8, sorted keys, compact JSON, no trailing newline). After an actual translation review, record its reviewer and reviewed state, then set `reviewSha256` with `translation_overlays.review_pin(locale, row)`. This digest binds the exact text, locale, reviewer and source revision. Any later text edit invalidates that verdict. Draft rows use a null review digest. Only reviewed rows project into derived fields and search rows. Draft rows remain outside runtime and count separately. Missing fields use English individually. Duplicate addresses, stale owners/revisions, invalid pointers, unsupported locales, empty text and absent reviewers are rejected. Existing VI/EN corrections still follow their owning canonical authoring/review workflow.

The package builder validates sidecars against base inputs before projecting reviewed text into the same lesson/unit/master shards and locale-specific SQLite fields. Source files remain untouched. Kana/candidate/context sidecars are validated/inventoried but those datasets are not newly bundled by T09.01. `authoredLanguages` records presence, not complete reviewed coverage; release generation remains blocked. Synthetic sparse-Arabic text exists only in temporary verifier fixtures and is never a shipped translation.

## Coverage and reproduction

```sh
python3 scripts/validate_localization.py --self-test --write
python3 scripts/validate_localization.py --self-test --check
python3 scripts/verify_runtime.py --report docs/audit/t01-runtime-validation.json
```

Review changed inputs before regenerating coverage; do not replace execution evidence merely to clear drift. The current [coverage ledger](coverage.json) pins 106 inputs and enumerates 17,020 field addresses: 15,002 fields with authored copy and 2,018 entirely empty optional vocabulary usage notes. Empty optional notes remain listed but are excluded from the translation denominator. Domain/locale totals distinguish present copy, English fallback and unavailable fields. UI catalog state and content field presence do not establish linguistic review. Original T02/T03/T04 editorial evidence retains its own scope.

T09.01 has five macOS runtime tests within the 24-test T01 regression run, seven rejected invalid catalogs, fourteen rejected invalid sidecars and positive synthetic plural fixtures for all 19 locales. The sparse package fixture verifies that reviewed translation is searchable/displayed only for its requested language, an absent sibling field still falls back individually, and a draft never reaches the index. The prior T01 report is retained in [the pre-T09 snapshot](../audit/t01-runtime-validation-before-t09-01.json).

Use Xcode MCP BuildProject, discover the test list, then run `ProjectBetaUITests / LocalizationUITests/testEnglishArabicHebrewInfrastructure()` on iPhone 18 Pro Simulator / iOS 27.2. The DEBUG `-localization-proof` route accepts `-localization-en`, `-localization-ar` or `-localization-he`. The single UI test launches all three, asserts count formatting/fallback visibility/Japanese environment and attaches screenshots. The Arabic/Hebrew snippets are direction probes, not reviewed translations. Captures were inspected for wrapping and order; exact external paths and fingerprints are in [execution evidence](../audit/t09-01-localization-validation.json).

No full 19-language UI/content, committed Settings integration, native curriculum search/reader, iPad/Duo, physical-device, specialized accessibility, listening, performance or release acceptance is claimed.
