> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Offline content, performance and footprint

Status: **NORMATIVE CONSTRAINTS — DS-U-31.** The owner accepted the offline-content assessment and requested these constraints in the design system. They apply to all learning screens, search, favorites, playback and widgets. The package/index implementation design is specified in ../engineering-contract.md. Cache limits and numeric performance budgets still require measured evidence.

Phase-scope refinement: DS-U-47 defers dedicated Accessibility work/acceptance. Specialized VoiceOver/accessibility evidence mentioned below is future reference rather than a current delivery gate; ordinary rendering correctness and the performance constraints remain applicable. DS-U-48/49 confirms system text sizing, RTL/localization and ordinary rendering correctness remain current requirements; read [the design-system record](decisions.md).

## Offline availability and package size

- Bundle the approved curriculum so browsing and search work offline. Opening a lesson must read local content without a network download prerequisite.
- Keep one canonical read-only runtime curriculum. Persist mutable favorites, learned state and preferences separately. Do not import a writable copy of the entire curriculum into SwiftData on first launch.
- Generate a production package from the authored content. Include required runtime fields, stable identities, version information, contextual readings, translations/fallback and explicit lesson/unit relationships. Keep reference PDFs, OCR outputs, Markdown duplicates, editorial reports and development fixtures outside production target resources.
- Avoid duplicating Japanese text and shared content across lessons, units and languages where stable references can preserve the approved meaning and contextual readings. Share invariant content and select the requested translation with English fallback; do not decode every language for each displayed item.
- Continue using system fonts and Japanese system TTS. Do not add custom fonts, per-item audio recordings or rendered page images as a performance shortcut. Keep missing-voice guidance under the existing playback contract.
- Account separately for curriculum resources, indexes, app/extension resources and generated caches. Any derived index or widget projection must justify its storage cost and avoid copying the complete curriculum into multiple writable locations or targets. Widgets must still work when the app is not running.

## Loading and memory lifetime

- App/service initialization and first usable navigation must not wait for decoding all lesson and Kanji details, importing the full curriculum or building a full search index. Read lightweight collection metadata for list entry.
- Read and decode lesson, unit or character detail on demand for the requested stable ID. Opening one lesson must not decode all other lessons. Favorites resolve the requested items/visible batch instead of materializing every saved parent and all descendants.
- Keep file reads, decoding, indexing, text normalization and example selection outside repeated SwiftUI body/layout evaluation. Run substantial CPU/I/O work away from the UI actor where the selected API permits. An asynchronous function alone is not evidence that work runs off the UI actor.
- Deduplicate concurrent reads of the same content. Use explicitly bounded caches with documented ownership, eviction and memory-pressure handling; allow them to release inactive decoded content and text-layout results. Bound prefetching to a measured navigation need. A normal browsing session must not eventually retain every opened lesson indefinitely.
- Account for multiple scenes and visible iPad columns when defining the active working set. Cache eviction must preserve navigation identity, valid playback ownership and persisted user state. It must not introduce reading-position restoration across relaunch.
- Cancel obsolete loading/search work when its request is replaced or its owning screen leaves. Check request identity before applying late results so an earlier request cannot replace the current selection. Geometry changes alone preserve the logical screen and its active request.

## Rendering and interaction

- Preserve the approved continuous lesson document while creating expensive rows and Japanese/ruby layout as needed for the visible area. Avoid constructing offscreen detail views for the entire curriculum. Use stable item IDs and bounded reusable layout work where measurement shows benefit.
- Section jump and search-result navigation must locate and materialize their target even when it has not been rendered. Lazy rendering must preserve Dynamic Type, access to all content, keyboard navigation and contextual readings.
- Furigana, language, appearance and geometry changes should invalidate the affected presentation work. A learned/favorite write should update relevant state and derived eligibility without decoding the whole curriculum again.
- Playback preparation uses the selected word, example, turn or dialogue. Starting TTS must not require loading unrelated lessons. Preserve stop, replacement and background/screen-departure behavior.
- Local loading must keep navigation and controls responsive. If a loading or failure state is visible, scope it to the requested content and preserve the existing selection context. Exact indicator/error copy follows the screen-state specification.

## Search, learned-aware examples and widgets

- Global search must cover all approved content and selected-language/English-fallback fields offline. Use a compact searchable representation or a queryable local store; do not decode every lesson or rebuild the corpus index for each query. Use the manifest/shard/prebuilt-index design in ../engineering-contract.md; verify measured size and search behavior.
- Prepare reusable static indexes during content packaging where practical. If runtime derivation is necessary, version it, reuse it and perform it outside the launch-critical path with bounded work. Do not present incomplete index coverage as a complete empty result.
- Query changes must supersede obsolete work. Bound result materialization and snippet/ruby generation to the requested result batch while preserving the approved result scope and navigation. Live 500 ms search and matching/ranking are selected in implementation-guide.md and the owner HTML.
- Learned-aware example selection should use explicit candidate/dependency references and the current saved learned state. Avoid scanning and decoding all lesson bodies whenever a character detail opens or learned state changes. Eligibility and fallback rules remain governed by the separate example-selection contract.
- Widgets consume compact, versioned eligible-item data or indexed local content with bounded reads and timeline generation. Do not decode the full curriculum on each timeline request or embed an unbounded eligible pool in every timeline entry.
- Preserve learned/favorites source rules, parent expansion, random selection and empty-source behavior. Publish only committed user-state revisions; stale derived work must not overwrite newer widget data. Limit refresh work to relevant committed changes and system scheduling.

## Evidence and acceptance

Current corpus counts and byte sizes are recomputed in ../audit/report.md and the owner HTML. These are editorial VI/EN drafts, not installed-app measurements or release size budgets. They are not a complete production package with all required locales and integrated kana/candidate resources. Recompute after runtime packaging and translation changes.

Before claiming performance/footprint acceptance, record a Release build, exact device/OS, dataset/language coverage, cold/warm conditions, method, baseline and results. Use representative physical devices across supported iPhone/iPad classes, including the least capable supported hardware available for acceptance. Simulator observations may support diagnosis but do not establish physical-device performance.

| Scenario | Required evidence |
| --- | --- |
| Fresh install and cold/warm launch, offline | Time to usable level/list navigation; content reads/decodes and peak memory. Confirm there is no full-curriculum import/decode/index build on the launch-critical path. |
| Open a lesson/unit/character; jump to an unrendered target | Local detail latency, decoded scope and visible content correctness. Compare first access with cache reuse. |
| Repeated browsing, back navigation and multiple scenes | Memory over repeated cycles, documented cache bound/eviction and memory-pressure recovery. Demonstrate that retained content does not grow with total browsing history. |
| Long lessons, large text, furigana/language changes and scrolling | Main-thread stalls, layout/scroll responsiveness and accessibility correctness with complete content. |
| Global/scoped search, query replacement and result navigation | Query/result latency, peak memory, full scope/fallback coverage and stale-result suppression without per-query full-corpus decoding. |
| Mark/unmark, favorite parent/item and Kanji example selection | Bounded affected work, unchanged eligibility rules and correct results from committed state. |
| Widget timeline with large learned/favorites pools and an empty source | Extension peak memory, read volume, generation time and projection size; valid source/random/empty behavior with the app closed. |
| Release package and persistent data after repeated use | Installed size, curriculum/index/extension contributions, writable data and cache growth; compare the complete intended language inventory. Measure download size separately when distribution tooling is available. |

Choose and document measurable latency, memory, cache and size limits with the implementation baseline before accepting the feature. Compare relevant changes against that baseline and investigate regressions. Passing architectural checks alone does not prove that scrolling, launch or extension memory is acceptable. No numeric limits or runtime pass are claimed in this documentation round.
