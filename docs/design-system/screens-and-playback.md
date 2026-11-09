> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Lesson screen, adaptive navigation and playback

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Confirmed requirements and delegated navigation decisions are implemented by the bindings below. Historical proposal disposition is retained for traceability.

## Confirmed lesson composition

The lesson is one continuous document, not mutually exclusive content tabs:

1. Lesson topic, preserving its level and original lesson number.
2. Vocabulary.
3. Grammar explanations with their related examples.
4. Sentence patterns and complete examples.
5. Dialogues.

Place a speaker to the right of each vocabulary item and complete sentence-pattern example. A dialogue title includes a whole-dialogue speaker; each speaker turn includes its own speaker to the right. One turn is one segment even if it contains multiple sentences. Abstract formulas are displayed as text; their complete Japanese examples are spoken. RTL follows DS-U-49 and native placement, with Japanese blocks retaining correct LTR order.

Provide a section-jump menu for vocabulary, grammar, sentence patterns and dialogues without replacing the continuous reading model. Highlight the currently playing dialogue turn; do not follow it with automatic scrolling.

The lesson toolbar contains the section-jump menu, an app-wide furigana toggle and the separate stop action while playing (DS-U-17). The learned-state control is at the start of the lesson; lesson-list status indicators reflect the persisted per-level prefix. Range confirmation follows [entry and learning state](entry-and-learning-state.md). Favorite actions use context menus (DS-U-20).

The owner selected balanced reading density, system fonts and Teal. Use the approved styles, color/geometry roles and scalable ruby contract in foundations.md/tokens.json; HTML pixels remain illustrative. Do not create separate fixed-height rows that clip long translations or furigana.

Apply the [performance and footprint constraints](performance-and-footprint.md) under DS-U-31: read detail locally on demand, bound offscreen row/ruby construction, and keep section-jump/search targets accessible before they are rendered. The continuous document must preserve complete content, Dynamic Type and complete content access. Starting navigation or playback must not decode unrelated lessons.

Sentence-example selection follows DS-U-26–29/33 across lesson vocabulary/grammar/pattern example surfaces as well as Kanji. Use reviewed bundled candidates and actual marked N5/N4 lessons. Prioritize learned supporting grammar, then fewer unfamiliar words, then simpler/shorter sentences, allowing the taught target to be new. Fall back to the simplest corresponding sentence. Dialogue scripts remain unchanged under DS-U-34; accompanying examples can adapt. The total display cap is three without expansion; reselect on opening and retain visible/speaking identities. Deterministic ranking bindings are in [example selection](example-selection.md). Current HTML excerpts are static authored content and do not implement this selection rule.

## Adaptive navigation — owner override DS-U-50

DS-U-50 supersedes the optional third column previously allowed under DS-D-01. Use native adaptive navigation for the four B-U-32 destinations: Lessons, Kanji, Favorites and Settings. Keep this information architecture stable across sizes.

- **Compact:** native tab navigation, with hierarchical navigation inside each destination. Opening a lesson replaces the lesson-list presentation in that hierarchy.
- **Sufficient/ample width:** use exactly two columns, sidebar and detail. Place the four destination controls and the current lesson/unit collection in the same sidebar. Open the selected lesson, unit grid or character in detail; deeper routes remain within that column. Favorites, Search and Settings reuse the existing detail area. No separate middle content/collection column is permitted at any width.
- **Native binding:** use the two-column `NavigationSplitView { sidebar } detail: { detail }` initializer. Top-level adaptive tab/sidebar controls must share or replace the existing sidebar, never add another navigation column.
- **Narrow windows/large text:** collapse columns according to available geometry and content readability. Device name alone does not determine a layout.
- Preserve current destination, selection and search across resize/rotation/pose changes. Do not stop playback merely because the same logical screen changes column presentation. Existing screen-departure/background stopping remains required.
- No new relaunch reading-position restoration, progress dashboard, autoplay-on-entry or new navigation destination is implied.

Implementation should use native navigation APIs available in the selected SDK and verify actual behavior. HTML breakpoints only illustrate the intended hierarchy; they are not approved iOS point thresholds or proof of native behavior.

This application-specific choice is informed by [Apple Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [Apple Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars) and [Elevate the design of your iPad app](https://developer.apple.com/videos/play/wwdc2025/208/). Apple describes adaptive navigation and nondestructive resizing; the two-column ProjectBeta structure is explicitly required by the owner under DS-U-50.

## Existing playback invariants

These remain binding under B-U-22/29/47:

- Use the offline Japanese system voice; no substitution with another spoken language when Japanese voice assets are unavailable.
- One playback request at a time. Selecting another word, example, dialogue or segment replaces the previous request.
- Provide a stop control. Stop on logical screen departure and app backgrounding.
- The speaker icon remains a speaker: no waves when idle, sound waves when playing. Tapping it always starts its target from the beginning, including a tap during playback. The owner approved the separate stop control in the lesson toolbar while playing under DS-U-17.
- Missing suitable voice preserves all reading and presents explanatory setup guidance.
- No speed adjustment, recording, recognition, pronunciation scoring or AI conversation in the current phase.
- DS-U-46 confirms explicit playback follows media volume even in silent mode; phone/audio interruptions and headphone disconnection stop playback with no automatic resume. This learning-content pronunciation is distinct from the Accessibility work deferred under DS-U-47.

For whole-dialogue playback, the selected dialogue is the playback request; its internal segments are not unrelated competing user requests. Segments must retain author-defined contextual Japanese readings. Furigana visibility does not alter pronunciation. Stop/replacement must invalidate callbacks from the earlier request, so an old completion cannot advance a stopped dialogue or highlight a stale segment.

No translated-language voice, speaker-specific voice, pause/resume, looping, background player or vocabulary playlist is authorized by this addition. Suggestions for these, if any, require a new explicit product decision.

## Disposition of reviewed suggestions

| ID | Status | Result | Authority |
| --- | --- | --- | --- |
| DS-P-01 | ACCEPTED | One turn is one segment; full dialogue plays from the beginning through all turns; solo turn playback ends after that turn. | DS-U-12. |
| DS-P-02 | REPLACED | The active speaker has sound waves; tapping restarts from the beginning. It does not become a stop icon. Retain stop separately under B-U-47. | DS-U-13. |
| DS-P-03 | ACCEPTED | Highlight the active turn only. Exact Teal fill and marker styling remain review geometry. | DS-U-14. |
| DS-P-04 | REJECTED | No automatic playback-follow scrolling or follow/resume control. Manual scrolling remains available. | DS-U-14. |
| DS-P-05 | ACCEPTED | Provide the section-jump menu without splitting the lesson. | DS-U-15. |
| DS-P-06 | ACCEPTED | Display the abstract formula and speak its complete Japanese examples. Do not send placeholder labels to Japanese TTS. | DS-U-16. |

The HTML now silently simulates these confirmed interactions. It does not implement an iOS TTS pipeline or verify native accessibility. See [component contracts](components.md) for state transitions and acceptance cases. Timing in the sketch is illustrative and is not an approved pause duration or speech rate.

## Implementation evidence and dependencies

- Use foundations/tokens, localized semantic labels and the state/component contract for pending/playing/error display.
- Verify the approved media-volume, interruption/disconnection-stop and no-auto-resume behavior on native devices. Dedicated Accessibility is deferred.
- Complete the content-bank, native family/ruby and performance evidence listed in acceptance.md; these are not unresolved UI preferences.


## T01 execution evidence — 2026-11-09

The bounded DEBUG proof and its reproduction/evidence boundaries are documented in [engineering handoff](../engineering-contract.md) and [native validation](../audit/t05-native-validation.json). T01.01 has native renderer acceptance within that fixture; T01.02 retains offline/real-audio verification in development under DOC-PLAN-02; this evidence is not required for current documentation completion. Existing product invariants above remain unchanged. This proof does not integrate the T02/T04 learning screens or persist the shared furigana preference.


## Offline listening/audio scheduling — DOC-PLAN-02, 2026-11-09

Under owner decision DOC-PLAN-02 (2026-11-09), offline listening and real-audio verification belong to development and are not required for the current documentation phase. Preserve the product requirements, unperformed cases and existing evidence; phase scheduling is not acceptance. T01.02 remains in_progress as a development task. This decision changes the execution phase only; offline Japanese speech, media-volume behavior, interruption/headset stopping and no automatic resume remain the approved product contract. No additional native/audio test is performed or claimed by this documentation update.
