> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Implementation bindings and screen map

Status: **NORMATIVE DESIGN SPECIFICATION v1.0.** This binds the confirmed owner decisions to screens/components. Ordinary layout/session details below implement those journeys; they do not add product features or certify the draft corpus. Runtime packaging and ownership are specified in ../engineering-contract.md. H01 implements and tests the data foundations as a separate Swift library; native app integration remains outstanding.

## Authority and boundaries

Read [decisions](decisions.md), [tokens](tokens.json), [foundations](foundations.md), then the relevant feature contract. New owner decisions supersede historical exploration. HTML is an interaction/layout sketch with representative source-authored data, not production SwiftUI or the curriculum package. Use native platform controls in the app; do not copy browser timers, pixels, dialogs, localStorage or document layout into SwiftUI.

Current scope includes system Dynamic Type, RTL/localization, native states and content TTS. VoiceOver/specialized Accessibility support/testing is deferred under DS-U-47/48. Keep the approved 19-language/English-fallback scope; prototype translation coverage does not reduce it.

## Screen map

| Screen | Content and actions | Open/return behavior |
| --- | --- | --- |
| Initial level choice | N5/N4, no preselection or prerequisite. | Commit selection, then open Lessons; later launches use the remembered level. |
| Lessons list | Shared level picker, alphabet entry, original lesson number/topic, learned status. | Tap lesson → continuous lesson. Touch-and-hold row → favorite action. |
| Lesson | Topic first; vocabulary; grammar; sentence patterns/examples; complete dialogues. Learned action at the start; toolbar search, jump, furigana, stop while playing. | Section jumps stay within the logical lesson. Search is lesson-scoped. Leaving the logical lesson stops audio. |
| Alphabet | Hiragana/Katakana tables and approved sound groups; selected sound's basic examples/guidance. | Tap cell selects its details and plays its reviewed pronunciation/context. Keep a single logical alphabet owner for selection and audio. |
| Kanji units | Shared level picker, unit number/title; no separate learned switch. | Tap unit → its character grid. Hold unit → favorite. |
| Kanji unit | Source character order, grid of glyphs; unit title context menu. | Tap glyph → character detail. |
| Kanji character | Glyph, translated meanings, On/Kun, word examples and up to three corresponding sentence examples. Hán-Việt only for Vietnamese. | Word/sentence speakers use their own contextual reading; hold character header → favorite. No invented default bare-character reading. |
| Favorites | Direct saved targets only, newest first, type/level filters. Parent saves remain one row. | Open saved target at its containing content location. Hold → remove immediately. Preserve independent direct child saves. |
| Search | Global entry on main screens; lesson entry scoped to the lesson. Group by existing content types. | Open matching location; returning from the result preserves that search session/query. Closing search ends the session; it is not saved across relaunch. |
| Settings | One shared language, System/Light/Dark, furigana and current level. | Persist locally. No independent font-size, speed, reminders, accounts, purchase or backup controls. |

Under DS-U-50, compact navigation uses native tabs plus hierarchy. Wider geometry uses exactly two navigation columns: sidebar and detail. The sidebar contains the four destination controls and the current Lessons/Kanji collection; the selected lesson, unit grid or character opens in the detail column. Do not add a separate middle content/collection column, even at ample width. Use the two-column `NavigationSplitView { sidebar } detail: { detail }` initializer for native split navigation; keep deeper navigation inside the existing sidebar/detail hierarchy. Collapse when required by geometry/readability without losing selected IDs/query. Do not derive layout solely from a device-model label. Current selection survives geometry changes; relaunch does not restore the lesson/scroll position.

## Component bindings

| Component | Contract |
| --- | --- |
| Lesson/collection row | Stable content identity; primary title + relevant meaning/metadata; wrap naturally. Audio and row navigation/context actions have separate hit regions. |
| Speaker | Idle speaker without waves; active speaker with waves. Every tap starts the target from its beginning. No pause/stop toggle. |
| Stop | Separate action on every playback-capable screen while pending/playing (lesson toolbar, Kanji and kana); cancels active/pending pronunciation and clears indicators. Keep it usable while a request is being prepared. |
| Turn | One complete speaker turn, possibly multiple sentences. Highlight only the currently speaking turn; no automatic scrolling. |
| Formula/example group | Formula is text; speakers belong to complete Japanese example sentences. Favorite identity belongs to the pattern/grammar target, not a newly invented example type. |
| Furigana | Same app-wide persisted preference across toolbar/Settings/widgets. Toggle presentation only; contextual speech stays unchanged. |
| Learned action | Use the current level's prefix; confirm actual affected ranges when more than one lesson changes. Single changes apply immediately. |
| Favorite context menu | Act on the smallest eligible held target. Native touch-and-hold/secondary click; no persistent star/ellipsis substitute. |
| Filter | Type and level conditions both apply. An explicitly linked multi-level target can match either applicable level, without duplicating its row. |
| Native state | Loading/empty/error stays scoped to the requested content/query. Failure preserves committed state/context and offers retry. |

Use SF Symbols/native icon roles for navigation, search, speaker, stop, section menu and learned check. Verify exact symbol availability in the selected SDK; symbol names do not define the underlying action. Use the approved geometry and native shapes/safe areas. Do not add decorative illustrations, custom haptic schemes or a score/progress dashboard.

## Deterministic presentation details

- Favorite order is newest committed save first; equal timestamps use stable target ID. Removing and explicitly re-adding creates a new save time. Saved lesson/unit children are expanded only for the already-approved widget source, not the Favorites list.
- Search group order follows the approved content vocabulary: vocabulary, grammar, sentence patterns, dialogues, Kanji. Within each group apply exact → prefix → contains, then stable authored order/ID. No fuzzy typo engine is implied.
- Use a 500 ms trailing debounce on committed input. Clear immediately cancels pending/running work. Do not normalize Japanese IME marked text back into the editable field.
- Normalize lookup representations, not displayed content. Case/width folding, Vietnamese accent folding (including đ/Đ), and corresponding kana-script folding must preserve Japanese voiced/unvoiced distinctions and original ruby. Do not globally strip combining marks from Japanese.
- Navigation resolves stable content/location IDs. A search-requested example must be materialized at the requested location; if needed include it within that target's three-sentence display cap rather than appending a fourth. This derives from the simultaneous exact-location and max-three requirements.
- Language/appearance/furigana changes preserve target identity and saved state. Translating an already-visible example retains its Japanese/example ID. Opening Settings has already left the reading screen and stopped its playback; a same-screen furigana/geometry update alone does not stop it.

These are implementation bindings of the approved flows. Do not promote them into new analytics, reading-history persistence, a new favorite target type or a content-update migration policy.

## Content contracts and engineering dependencies

Release content needs stable identities/versioning and explicit level/lesson/target links. The existing authoring JSON is a draft source format, not an approved runtime schema. The implementation design for manifest/JSON shards, a prebuilt SQLite index and atomic user-state publication is in [engineering-contract.md](../engineering-contract.md). Cache budgets and implementation evidence remain work under [performance constraints](performance-and-footprint.md).

H04 supplies the primary-reviewed sentence/dependency/speech bank; native adoption remains T04.05/T01. Remaining translation production/review belongs to T05 during development. H03 now supplies the reviewed VI/EN kana authoring inventory; T04.04 still requires native integration and voice verification. The renderer must expose scoped unavailable/error states rather than inventing examples/readings or presenting uncommitted data. Do not auto-delete or remap saved identities from a view. A removed target remains in Favorites under its original ID as unavailable and can be explicitly removed. Resolve availability against the current package; filter unavailable targets out of search and widget pools without switching the configured source.

Physical/runtime evidence remains necessary for Japanese ruby, TTS/voices/routes, supported adaptive layouts, WidgetKit families and measured footprint/performance. Read [acceptance](acceptance.md) for what can and cannot be claimed.
