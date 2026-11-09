> GENERATED from [the owner HTML](index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Engineering handoff contract

Status: implementation design for the owner-approved feature scope. Content migration and form-scoped pronunciation rules are normative below. H01 foundations are implemented in ios/ProjectBeta/Runtime and tested on macOS; the iOS application has not integrated or accepted them. See runtime-data-contract.md for the executable v1 boundary and evidence.

## Boundaries and ownership

Domain owns stable content identifiers, ordered lesson IDs per level, independent learned-prefix mutation, direct favorite identity, candidate ranking and widget eligibility. It imports no SwiftUI/SwiftData/audio APIs. Data owns package reading, prebuilt lookup, SwiftData writes and TTS/widget adapters. Presentation owns MainActor scene state, routes and localized display. App composes dependencies manually with cheap factories.

App-scoped: immutable content repository, serialized user-state writer and single playback coordinator. Scene-scoped: selected logical route, active search request and visible candidate snapshot. A new playback request from any scene cancels the old token. Backgrounding the app stops audio; departure by the owning scene stops its request. Geometry alone does not end the logical screen. Do not add multi-profile or cross-device state.

## Bundled package v1 implementation design

Use a generated read-only manifest plus UTF-8 JSON detail shards per lesson/unit and character groups, and a prebuilt SQLite search index. SQLite is a derived implementation choice, not new user scope. Keep authoring JSON, PDFs, OCR, Markdown and review assets outside app resources. Use stable authored UUIDs, never array offsets or display titles, as runtime IDs. Do not rename existing IDs to normalize content.

Manifest fields: schemaVersion, contentVersion, generatorVersion, sourceInputHashes, authoredLanguages, requiredLanguages, ordered lesson IDs per level, entity ID/type/location map, shard paths/checksums, explicit unit milestone lesson IDs, candidate/target index and search index versions. A release builder fails for missing mandatory references, language coverage, dependency bank, speech contexts or failed editorial gates. A development package is explicitly draft and cannot be promoted by changing a label alone.

Opening a collection reads lightweight metadata. Opening a detail reads its shard and bounded dependencies. Unknown package versions/checksum failures yield a scoped unavailable state. No complete curriculum import into SwiftData or launch-time search-index build. Cache ownership, limits and memory-pressure eviction are recorded with T07 measurements before acceptance.

Search rows link stable result/target/lesson/unit IDs to original display fields and normalized lookup fields. Precompute all approved Japanese/kana/romaji/Han-Viet and locale-specific meaning fields. Requested-language missing fields resolve to English before indexing/display; do not mix unrelated locale matches. Group and rank according to F09. A search session carries query/scope/language/request token; stale completions never publish. IME marked input is not committed input. Search-selected examples occupy one of the three available slots; include that candidate, then fill remaining slots by the shared ranking.

## Mutable local state and transactions

Persist selected level, shared language preference, appearance, furigana, per-level learned endpoint IDs, direct favorites (target type/ID and committed timestamp), contentVersion and monotonic revision. Missing prefix endpoint means no learned lessons; no synthetic N4 lesson 0/25 runtime entity. Determine eligible lessons from the level's ordered IDs. A write serializes against the current revision, validates, saves, then publishes the new immutable snapshot. Failure keeps the last committed revision. Disable/deduplicate an in-flight action rather than interleave overlapping writes.

Range confirmation captures the revision and exact changed IDs. If another scene changes that revision before confirmation, recompute and present the new changed range before applying; never silently apply a different multi-lesson range. Cancellation makes no write. Preferences use the same successful-save rule. Equal favorite timestamps sort by stable target ID. Parent expansion only occurs for widgets and deduplicates target IDs.

## Content upgrades

Validate the new package before adopting it. Additive updates retain existing IDs, favorite identity and learned endpoints. Removed or otherwise unavailable targets retain their original favorite ID and save time; show an unavailable row with an explicit remove action. Do not silently delete or redirect favorites. Search contains only the current package; widget pools include only favorites whose target ID and kind resolve in that package. Lesson reordering/removal/replacement requires a version-bound, owner-reviewed lesson mapping. Transfer a learned prefix only when the mapped set exactly equals a prefix in the new order; otherwise reject adoption and keep the old package and committed state. Never infer equivalence from text, add learned lessons, or use lesson mappings to redirect favorites. Migration executes transactionally and can fail without destroying old state.

## Candidate and speech authoring interfaces

Each candidate needs a stable sentence ID; target IDs plus form/sense link; Japanese segments with contextual reading; translated meanings; supporting vocabulary/form IDs and grammar IDs; taught-target exceptions; lesson/level introductions; editorial simplicity order; review state and provenance. Knowing a grammar ID alone does not imply knowing its vocabulary. Candidate fallback must still match the target/sense. Empty banks are content defects, not permission to invent runtime text. Dialogue turns remain fixed.

Each displayed vocabulary form has its own speaker bound to that exact form and its linked sense/meaning. Resolve the selected form to a reviewed Japanese speech target; do not select a default form for a multi-form entry. Bound forms containing 〜 or ～ require a visible context label and a complete, reviewed Japanese word or sentence target. If that context is missing, keep the form/meaning readable and show an item-scoped pronunciation-unavailable state. Never pass 〜/～, slot labels or translations to TTS, or concatenate displayed ruby with its base. H04 now supplies 155 reviewed authoring contexts: 114 bound vocabulary entries / 120 forms plus 35 Kanji lexical occurrences. The earlier count of 53 missed U+FF5E and marker-free N4 readings. Its 5,616 speech records include 466 separate dictionary forms. These are content/reading evidence, not native voice or UI acceptance; see content-authoring/sentence-bank/README.md. Explicitly resolve particle pronunciations and Latin abbreviations. Stop remains available on every playback-capable logical screen, including Kanji and kana, while pending/playing; it uses the same separate action as the lesson toolbar.

## Widget publication

Use one committed revision containing contentVersion, state revision, resolved shared language/furigana and compact eligible target references. Write a new projection atomically in the shared container; a stale producer cannot replace a newer revision. If projection publication fails after the user-state save, retain the saved user state and retry/rebuild from that revision; never report the save as rolled back. The extension validates compatibility, can read bundled content without the app, and never consumes a partially written projection.

Learned pools use both level endpoints; Kanji milestone level is resolved from the milestone lesson, not the source volume. Units 21–25 reference N5 lesson 25. Favorite pools expand saved parents independently of learned state. Sample distinct eligible IDs per entry, with deterministic clock/random seams in tests. Pattern examples follow the shared candidate rule. System schedules actual timeline display. Empty/unconfigured/unavailable/fitting-fallback states remain distinct.

## Verification before integration

Tests must exercise meaningful failure boundaries: stale search/audio callback, concurrent range confirmation, save failure, publication failure after save, stale widget projection, missing voice, malformed package and unsupported migration. Verify per-level examples from F03, no-learned/N4-only candidate ranking and unit 21–25 eligibility. Native proofs cover ruby, Dynamic Type/RTL, media-volume/interruption behavior, applicable WidgetKit families and physical performance. Do not count the scaffold's placeholder tests as feature acceptance.


## Proper names — B-U-59 (2026-11-08)

Retain reference proper names, including fictional names and titles, within the approved content scope. Preserve the referent, spelling and contextual reading; label fictional entities in the authored meaning/context when needed. Do not filter source rows by fictional-name status or infer identity mappings from similar names. Restore the previously excluded vocabulary with new stable IDs and source locators. Existing independently authored dialogue characters are not mapped to textbook characters; original scripts remain fixed unless a specific evidenced content correction requires editing. See content-authoring/source-reconciliation/proper-name-review.json for the item-level review and limits.


## H04 authoring handoff — 2026-11-08

H04.01–03 are complete as content-authoring tasks under B-U-51 primary self-review. The sidecar preserves all source curriculum IDs, original Japanese/translations/context/dialogue objects and PDF provenance. Its 3,275 reviewed complete candidates cover all 6,126 form/sense/variant targets, including 466 dictionary forms; the gap ledger is empty. Every candidate has complete lexical/form/sense and grammar dependencies, target-scoped exceptions and reviewed editorial simplicity.

Source-word bindings are explicit semantic review records; character correspondence additionally requires a curated parent-word UUID relation and visible source character. The 122 reviewed bare-character pairs exempt only the actual character meaning being taught, never compound vocabulary or unrelated grammar. Context-only support remains unfamiliar. The 60 exact reviewed repeated-lexeme groups share actual introductions without changing entity IDs or independent level endpoints. Duplicate suppression does not certify semantic matching.

All 5,616 speech records are authored and revision-bound. The 155 bound contexts cover 114 vocabulary entries / 120 forms and 35 Kanji lexical occurrences. Exact per-form/sense resolution rejects missing/stale contexts, including a changed reviewed-context digest; labels, translations, slot markers and duplicated ruby/base never enter speech. Source orthographic readings inherit the pinned H02 primary review. No system-voice listening is claimed.

Run `python3 scripts/validate_sentence_bank.py --complete --self-test --check`: 27 invalid fixtures are rejected and 24 offline reference checks cover independent prefixes, ordered ranking, scoped exceptions, fallback, cap/search/dedup, exact speech and unavailable paths. These are authoring tools, not native application tests. T04.05 owns native selection/snapshots; T01 owns ruby/playback. H01's draft candidate/speech index versions remain zero and no authoring sidecar is bundled into the app. Other 17-language, independent-human, device/performance and release evidence remain separate.


## T01 bounded native handoff — 2026-11-09

T01.01 is complete for the bounded renderer proof. T01.02 and the group retain in-progress development work. Offline listening and real-audio verification are scheduled in development under DOC-PLAN-02 and are not required to complete the current documentation phase. See [revision-bound evidence](audit/t05-native-validation.json). Fourteen native tests pass on iPhone 18 Pro Simulator / iOS 27.2 (eight deterministic component tests, two real-system adapter integration tests and four UI tests). Debug compilation has no Swift compiler warnings; raw App Intents metadata-tool notices remain recorded in the evidence. A fresh Release Simulator build passes after the media-reset fix; the executable contains no DEBUG proof type or fixture payload markers. Compilation is not release acceptance.

The reusable Core Text renderer keeps each authored ruby base on one line, sizes through system Dynamic Type and preserves Japanese LTR in RTL UI. At a width narrower than an indivisible ruby run, native horizontal scrolling keeps the font/reading intact. Tests cover 34 fixture rows/turns, 180/280/640 pt text widths, three system categories through accessibility XXXL, ruby on/off and exact text coverage. Inspected native UI captures cover Light/Dark, forced RTL, a narrow accessibility-size viewport and landscape playback. Forced RTL is not an Arabic/Hebrew translation acceptance pass. No iPad/Duo or physical typography acceptance is claimed.

One app-owned MainActor playback coordinator replaces/restarts requests and uses a fresh token for every utterance. Only actual start callbacks publish playing waves/turn highlights; stale/duplicate/cancelled callbacks cannot advance a later request. Audio-session operations run on a private serial queue. The system adapter selects available Apple Japanese voices only, configures media playback and stops on background, logical-screen departure, system deactivation, route loss and media-service reset. Notification delivery is marshalled to MainActor; the app's own deactivation is ignored so it cannot cancel a replacement request. No notification resumes speech.

The DEBUG-only `-native-proof` route is an isolated harness. `scripts/build_native_proof.py` exports 26 rows plus the unchanged eight-turn lesson-1 dialogue from lessons 1/5/10/16/26/50 and reviewed H04 speech records, retaining entity/form/turn keys and source hashes. It checks selected input pins against the complete H04 report. Source lessons/dialogues/PDFs remain unchanged. Latin ATM/JR readings, は/へ particles, polite variants and bound contexts come from that reviewed handoff. This is a bounded fixture, not native candidate selection or a release runtime package. Its generated Swift data and screen are compiled out of Release; no authoring JSON is bundled as a resource.

Reproduce by running `python3 scripts/build_native_proof.py --check`, then the ProjectBeta scheme's tests on the recorded simulator using Xcode MCP. Launch Debug with `-native-proof`; optional harness arguments are `-proof-renderer`, `-proof-rtl`, `-proof-large`, `-proof-narrow`, `-proof-dark`, `-proof-dialogue`, and `-proof-missing-voice`. Only the last flag injects an unavailable-voice driver. The fixture uses English meanings and a local ruby toggle; T02 still owns committed app preferences/localization and runtime integration.

Real system-speech start/stop, full-dialogue restart, rotation without stopping, app Home/background/foreground and logical departure were exercised through native UI. Missing-voice UI and interruption/headphone notifications use injected driver/events, not removal of installed assets, a real call or a disconnected headset. There was no network-disabled playback/listening, silent-switch/media-volume test, actual phone/audio interruption or headset-removal listening. These remain required for T01.02 development closure, not for current documentation completion, under DOC-PLAN-02. Per-turn sequencing and stale-callback cases are deterministic native component tests, not independent pronunciation/listening approval. Screenshots/logs/xcresult stay outside the repository and are indexed by the evidence report; no browser simulation is counted as an app test.


### T01.02 continuation — real system completion

The integration test wraps the real SystemSpeechDriver without generating callbacks. It requires an installed Japanese Apple voice, submits all eight unchanged fixture turns, and verifies one actual started/finished pair per token in exact source order. It then replaces an active dialogue with one selected turn, waits for actual completion, checks that no former dialogue turn is submitted, and verifies that explicit Stop stays idle after late callbacks. The deterministic notification test also verifies that new-device/category/override route changes and a resumption recommendation do not replace an active request. These are simulator callback assertions, not listening acceptance.

All component/integration cases share a serialized suite because injected global audio notifications would otherwise interfere with the real system test. Reproduce with XcodeBuildMCP test_sim and extraArgs ["-parallel-testing-enabled", "NO"]. The prior evidence is retained in [the pre-continuation report](audit/t05-native-validation-before-continuation.json). Current evidence pins are refreshed only after running the final sources; captures and raw results remain outside the repository.

During development, for the scheduled T01.02 device/audio verification under DOC-PLAN-02, use the existing DEBUG -native-proof route. Record the actual device/OS, Japanese voice, exact fixture target and observed outcome for each case: download the voice then disable network access and listen to the reviewed particles, ATM/JR, form variants and bound contexts; play with silent mode enabled at a known audible media volume; interrupt an active dialogue with a real call/audio interruption; disconnect the active headset. After each interruption/disconnection, verify that the app stays idle until a new explicit speaker tap. Listen to the entire fixed dialogue and a solo turn as well. Record unperformed cases explicitly; a simulator notification or successful delegate callback cannot close them.


### T01.02 media-service recovery correction

The earlier adapter stopped on media reset but retained its synthesizer. Apple requires rebuilding app audio objects after a [media-service reset](https://developer.apple.com/documentation/avfaudio/avaudiosession/mediaserviceswereresetnotification). The adapter now detaches the old delegate and creates/configures a fresh AVSpeechSynthesizer after invalidating the request. Media-service loss also stops playback. The existing serial audio-session adapter reapplies playback category, spokenAudio mode and empty options on the next explicit speaker action; neither reset nor a resumption recommendation starts audio. Late activation completions and delegate events retain their invalidated tokens.

One new deterministic regression covers loss, reset without preceding loss and reset during pending activation. One integration regression posts loss/reset notifications around the real system driver, verifies two distinct synthesizers with the old delegate detached, observes no submission during a 750 ms idle window, then receives actual start/finish callbacks for an explicit solo-turn retry. This proves the adapter response to injected notifications; no actual OS media-server restart or physical interruption is claimed. The previous twelve-test evidence is retained in [the pre-reset report](audit/t05-native-validation-before-media-reset.json).

The earlier Mac-only continuation retained all physical/offline evidence gaps. The latest owner instruction DOC-PLAN-02 now schedules offline listening and real-audio verification in development, outside the current documentation phase; the product behavior and unperformed evidence remain unchanged.


## T05.01 localization infrastructure — 2026-11-09

The technical child is complete within the [pinned execution scope](audit/t09-01-localization-validation.json). [Localization handoff](localization/README.md) describes the APIs and [coverage ledger](localization/coverage.json). Five localization tests join the nineteen H01 regression tests on macOS. One native UI test on iPhone 18 Pro Simulator / iOS 27.2 launches EN/Arabic/Hebrew probes, verifies the compiled count resource, conditional English label and Japanese LTR environment, and supplies three inspected captures. Native rendering receives supplied field metadata; it is separate from runtime resolver execution. This does not establish translation semantics or integrated curriculum-reader acceptance.

Resolve the shared committed language once through `ContentLanguage.resolve`, using nil for System, then pass the same result to content lookup and search. Requested nonblank field text wins, otherwise nonblank English, otherwise unavailable. The result identifies actual language/fallback explicitly. Japanese base/readings and stable IDs remain unchanged. Arabic/Hebrew layout and Japanese subtrees use their own appropriate directions. Sino-Vietnamese display is enabled only for Vietnamese. T02 owns committed Settings/application wiring; T03 owns native search sessions.

VI/EN remains canonical in authored JSON. Remaining locales use revision-bound `docs/localization/content/<locale>.json` sidecars following `docs/localization/content.schema.json`; exact field pointers, owner IDs and owner hashes prevent stale translation adoption. Each review verdict additionally pins the exact locale, text, reviewer and source revision; editing text invalidates the recorded review. Only reviewed rows project into existing detail fields and requested-locale index fields. Draft rows are separately inventoried and never enter the runtime index. Original source files and earlier editorial review pins are unchanged. Kana/candidate/context sidecars can be inventoried but those datasets are not newly bundled. Runtime generator 1.1.0 retains schema/index v1 and all 6,059 IDs; authored-language presence never establishes full reviewed coverage or bypasses release gates.

The six-key Interface String Catalog covers the four implemented scaffold titles, English fallback label and a plural count resource. Future screens add their own resources; DEBUG proof diagnostics are outside product translation coverage. Current source-copy inventory has 15,002 nonempty localized fields plus 2,018 entirely empty optional usage notes. Empty notes stay in the field ledger but outside translation denominators. UI source state, actual translations, pending sidecars and English fallback remain distinct. T05.02 owns VI/EN UI/content review; all seventeen remaining translation tasks stay open.

Run `python3 scripts/validate_localization.py --self-test --check` and the H01 verifier after changes to their owning inputs. Seven invalid catalog fixtures and fourteen invalid sidecars are rejected; synthetic plural shapes cover all nineteen locales, while actual compiled runtime plural evidence here covers the English fallback resource only. Sparse-locale package tests check exact field display/search, sibling fallback, unchanged IDs, absent unrelated-locale matches and draft exclusion. No full 19-language, iPad/Duo, physical-device, listening, specialized-accessibility, performance or release pass is claimed.


## Phase boundary — DOC-PLAN-01, 2026-11-09

Read the documentation gate in the owner HTML before selecting development work. All documentation checklist tasks must be done and synchronization/audit checks must pass. Translation authoring/review (T05.02–19) belongs to development by explicit owner confirmation. Retain all existing delivery statuses/evidence; phase readiness is not completion of H01–T08. T07 measured baselines/budgets and T08 release decisions remain their own acceptance gates.


## Offline listening/audio scheduling — DOC-PLAN-02, 2026-11-09

Under owner decision DOC-PLAN-02 (2026-11-09), offline listening and real-audio verification belong to development and are not required for the current documentation phase. Preserve the product requirements, unperformed cases and existing evidence; phase scheduling is not acceptance. T01.02 remains in_progress as a development task. This decision changes the execution phase only; offline Japanese speech, media-volume behavior, interruption/headset stopping and no automatic resume remain the approved product contract. No additional native/audio test is performed or claimed by this documentation update.


## Documentation handoff — DOC-PLAN-03, 2026-11-09

Completed documentation is retained as product, design, content and engineering handoff material. Completed documentation tasks remain historical evidence and are no longer listed in the checklist or roadmap. T01.02 belongs to development; its in-progress status and unperformed E2E cases are preserved. The approved documentation remains in the existing design, content and engineering contracts; no duplicate specification is introduced. Historical task IDs and evidence remain available for provenance and dependency checks. Open documentation work must still be shown and must block development readiness.


## Current review and P1 execution — DOC-PLAN-04, 2026-11-09

Completed P0 foundation groups are retained as handoff documentation and omitted from the execution roadmap. T01 and its children now inherit P1; open work continues in development. P1 translation/audio work belongs to development, app/performance acceptance to acceptance, and sign-off to release. Track these in their owning tasks rather than duplicate them as current documentation issues. Preserve open finding status, dependencies and execution evidence; hiding a scheduled issue does not resolve it. P0/P1 are priorities, distinct from execution phases. Existing native evidence retains the historical P0-T01 label from its execution baseline; this is not the current planning priority. Do not relabel or refresh historical evidence for a planning change.


## T01.02 development revalidation — 2026-11-09

The owner requested execution of T01.02. The unchanged bounded native proof was rerun on iPhone 18 Pro Simulator / iOS 27.2: 14 passed, zero failed/skipped (eight component, two real-adapter integration and four UI tests). Four playback captures were actually inspected. See the [development execution report](audit/t01-02-development-validation.json) for exact hashes, results, diagnostics and capture scope. The MCP request timed out after 300 seconds; the same Xcode run continued to successful completion, confirmed directly by xcresult. No duplicate run, implementation change or historical evidence-pin refresh was performed. Release compilation was not rerun.

The completed former T01.02 is documented in the native/audio handoff; its recorded physical E2E cases passed. The owner previously confirmed no physical iPhone. Network-disabled pronunciation listening, silent/media-volume output, actual interruption and active-headset removal cannot be closed by these Simulator results. Native background/departure and real-synthesizer callback passes remain supporting evidence only. Product requirements and the existing physical-audio E2E fixtures are unchanged.


## Completed former T01 task handoff — DOC-PLAN-06

The completed native/audio proof has been removed from the current execution roadmap. Its roadmap-era IDs were T01, T01.01 and T01.02; the earlier DOC-PLAN-05 crosswalk IDs were T05, T05.01 and T05.02. See this engineering handoff and the linked historical reports. The current owner HTML migration table maps both identifier sets to this document and maps the remaining groups in order to T01–T07.
