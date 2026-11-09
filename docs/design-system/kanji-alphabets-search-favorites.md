> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Kanji, kana, search and favorites

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Product behavior below is confirmed. Read implementation-guide.md for deterministic session/presentation bindings; editorial inventory and native evidence remain dependencies.

All journeys follow DS-U-31 in [performance and footprint](performance-and-footprint.md): local on-demand details, bounded favorites/example resolution, reusable offline search representations and bounded widget projections. Optimization must preserve approved search coverage, learned/favorites eligibility, contextual readings, Dynamic Type and RTL.

## Kanji

Authority: B-U-18/41/58 and DS-U-21/22.

1. Show the available Kanji units for the applicable level.
2. Open a unit to a character grid.
3. Open a character to its detail: meanings, Sino-Vietnamese readings, On/Kun readings, concrete words/compounds and corresponding sentence examples.

Sentence examples must prioritize vocabulary and grammar already learned according to the union of manually marked N5/N4 lessons, while preserving independent learned prefixes. Use the simplest corresponding sentence if no fully familiar supporting-language candidate exists. This applies to example surfaces throughout the app, except kana. It is example selection for reading, not a quiz or a new mastery score. See [example selection](example-selection.md) before implementing ranking/count details.

Keep contextual readings attached to the appropriate word/example. A bare Kanji has no universally selected pronunciation: do not invent a default reading because the detail displays multiple On/Kun values. Provide pronunciation on reviewed contextual word/sentence targets; no new standalone On/Kun playback action is selected.

Do not add radicals, stroke count, stroke order or a separate Kanji-unit learned switch. Learned-source widget eligibility still uses each unit's explicit lesson/level milestone. Kanji browsing and favorites are not locked by learned status.

On wider layouts the selected detail may appear alongside its collection according to the delegated adaptive-navigation contract. Native compact navigation preserves the same hierarchy. Context-menu favorite targets are the unit or character whose surface is held; a word example is not implicitly a new favorite type without an existing supported vocabulary identity.

DS-U-45 limits visible Sino-Vietnamese readings to the Vietnamese shared-language selection, including optional widget detail. Keep the underlying data and approved search fields intact. Other languages retain Japanese On/Kun, localized meanings and examples.

Remaining detail implementation includes grid/character metrics, word-versus-sentence organization and contextual pronunciation. No separate previous/next shortcut or isolated-reading playback feature has been selected.

## Hiragana and Katakana

Authority: B-U-16/27/32 and DS-U-25.

Place the alphabet area within Lessons. Use tables with tap-to-hear cells and corresponding examples. Include basic sounds, voiced/semi-voiced sounds, combined sounds and extended Katakana combinations used for loanwords. Coverage must be comprehensive rather than an arbitrary small sample. Do not display romaji; it remains a search input under the existing search contract.

DS-U-26 exempts this area from learned-aware example selection. Use the most basic suitable words/sentences regardless of learned-prefix state. The owner identifies the alphabet as the beginner's starting material; do not turn that rationale into locked lessons, mandatory completion or a separate alphabet-learned state.

DS-U-43 confirms the main groups: basic, voiced/semi-voiced, combined/extended, and special uses including small kana, gemination and long vowels. Put historical/rare forms in a separate reference area. The fullest-coverage requirement still needs a reviewed editorial inventory; do not claim an unverified finite list is exhaustive. Some symbols do not have a useful isolated pronunciation; their spoken examples must not be invented by treating every glyph as an independent syllable.

Each reviewed entry needs its glyph/combination, script/category, valid Japanese pronunciation context, example(s), translated meaning where applicable and any required usage guidance. These fields describe the authoring evidence needed. Display no more than three sentence examples per target; context-dependent marks use a reviewed word context rather than an invented isolated sound. Do not add stroke/radical content or a kana-specific favorite type automatically.

H03 now supplies a [301-entry authored inventory](../content-authoring/kana/inventory.md), [source-cell ledger](../content-authoring/kana/source-inventory.json) and [revision-bound primary review](../content-authoring/kana/review.json). It covers the cited standard-Japanese tables, dependent uses and a separate 29-entry reference group. Primary self-review under B-U-51 is authoring evidence, not independent-human, native voice or release certification. See [the scope and maintenance guide](../content-authoring/kana/README.md) for rare-context mappings and explicit coverage boundaries. The 57 prototype fixtures remain illustrative; T04.04 consumes the canonical inventory for native UI/playback.

## Favorites

Authority: B-U-25/43/46/49 and DS-U-20/23.

- Default view: all saved content types, newest saved first.
- Filters: content type and N5/N4.
- Existing targets: vocabulary, grammar points, sentence patterns, dialogues, individual Kanji, lessons and Kanji units.
- Add/remove actions: touch-and-hold context menu, with native equivalent pointer access; specialized Accessibility is deferred.
- Preserve the exact saved parent/item identities. A favorited lesson/unit is one saved parent; widget expansion does not create direct child favorites.
- Favorites remain independent of learned status. Do not filter an item out merely because its lesson is not learned.
- DS-U-44 confirms that the app lists directly saved parents/items only, without expanding saved lessons/units into all their children. Remove immediately, with brief committed-success feedback; failed saves preserve the last committed state and offer retry.

Deterministic presentation details (equal-timestamp tie-breaks, remove/re-add order, multi-level matching and opening a saved target) are resolved in implementation-guide.md. Empty/error presentation follows the approved native state contract. Parent listing and removal confirmation are resolved by DS-U-44.

## Search

Authority: B-U-24/27 and DS-U-24/42.

- Main-screen magnifying glass: global search across the app.
- Lesson-screen magnifying glass: search within that lesson.
- Group results by content type.
- Activate a result to open the containing lesson/unit at the matching content location. This is an explicit navigation action, not restoration of a past reading position across relaunch.
- Preserve the approved fields: Japanese Kanji/kana, meanings in the selected language, Sino-Vietnamese and romaji input. Search scope covers vocabulary, grammar, sentence patterns, dialogues and Kanji.
- Keep the four main destinations; search is an entry/presentation within the approved navigation, not an unapproved fifth permanent destination.
- Search as the user types, with a 500 ms trailing debounce after the latest committed query change. Supersede obsolete pending/running work; only the current query/scope/language request may publish results.
- Matching ignores case and Vietnamese diacritics and treats corresponding Hiragana/Katakana kana as equivalent for lookup. Preserve the original text, reviewed readings and translation in displayed results.
- Within each type group rank exact matches first, then prefix matches, then containing matches. Approved romaji aliases remain searchable; do not display them in learning content.
- Clearing to an empty query cancels pending work immediately and restores the unqueried state; do not wait 500 ms to clear stale results or present unqueried text as a completed no-results search.

Use stable content IDs and explicit location references for result navigation, not list indices or guessed text offsets. Geometry changes preserve the current query/selection under the adaptive-navigation decision. Actual old-screen departure still stops playback.

Use the final group/session/return/location bindings in implementation-guide.md. Native snippets preserve original Japanese/ruby and selected-language fallback; normalized strings are lookup-only. Fuzzy/typo matching and a new kana-table search scope are not approved by DS-U-42. Native composition handling and normalized-to-original highlight mapping need focused implementation evidence; do not corrupt Japanese IME input or highlight the wrong source span.

## Primary references for kana authoring

Use the reviewed source inventory plus [Agency for Cultural Affairs modern kana guidance](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/gendaikana/honbun_dai1.html) and [loanword kana tables/guidance](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/gairai/) to build and verify the complete inventory. These references support the approved group structure; the revision-bound H03 inventory supplies the assigned authored teaching scope. Native integration and pronunciation acceptance remain separate. Do not mistake an old historical proposal for current loanword guidance.
