> HISTORICAL DECISION EVIDENCE. Current scope, readiness, task order and proposals are maintained in [the single owner review](../index.html). Approved B-U/DS-U rows remain evidence; old open-question/status paragraphs are not the current backlog. Later decisions supersede earlier rows.

# Design decisions and open questions

Status: **CURRENT-PHASE DESIGN DECISIONS RECORDED — v1.0.** Owner decisions supplement the B-U requirements. The question table separates resolved UI requirements from deferred scope and implementation/content evidence; chronological notes below remain historical evidence.

## Confirmed in this conversation

| ID | Decision | Evidence |
| --- | --- | --- |
| DS-U-01 | Cover the entire design system, including screen layouts, interaction journeys and widgets. | Owner answer 1: “tất cả”. |
| DS-U-02 | Minimal, modern, distinctly Apple visual direction. | Owner answer 2. |
| DS-U-03 | Use system fonts. | Owner answer 3. |
| DS-U-04 | Present color recommendations for owner selection. The owner subsequently chose Teal under DS-U-07. | Initial answer 3; subsequent color answer. |
| DS-U-05 | Provide agent-friendly implementation documentation and HTML sketches for owner review. | Owner answer 4. |
| DS-U-06 | Clarify unanswered decisions with the owner; zero assumption. | Initial request and B-U-09. |
| DS-U-07 | Use the Teal accent hue. DS-U-41 later approves the concrete visual values in foundations.md and the review. | Owner: “teal”; later visual approval. |
| DS-U-08 | Balanced content density. | Owner: “balance”. |
| DS-U-09 | A lesson opens with its topic, followed by vocabulary, grammar, sentence patterns/examples and dialogues in one continuous page. | Owner lesson-layout description. |
| DS-U-10 | Place a speaker icon to the right of vocabulary, sentence patterns and dialogues. A dialogue has a speaker at its title for whole-dialogue playback and a speaker for each segment for selective playback. DS-U-12/16 resolve segment granularity and template pronunciation. | Owner audio-control description and subsequent answers. |
| DS-U-11 | Select iPad/Duo navigation according to best practice. This delegates the layout decision and does not require another approval for the selected navigation pattern. | Owner: “làm theo best practice”. |
| DS-U-12 | One dialogue segment is one speaker turn, retaining all sentences in that turn. Playing a segment ends after that segment; playing the full dialogue starts at its beginning and proceeds through all turns. | Owner answer 1: “đúng” to the complete proposal. |
| DS-U-13 | Idle playback uses a speaker icon without sound waves. Active playback uses a speaker with sound waves. Tapping the speaker again restarts its target from the beginning, including when already playing. Do not replace the active speaker with a stop icon or turn it into pause/resume. | Owner answer 2, superseding DS-P-02. |
| DS-U-14 | Highlight the playing dialogue turn only; no automatic scrolling to follow playback. | Owner answer 3: “chỉ highlight”. |
| DS-U-15 | Add a “Jump to section” menu for vocabulary, grammar, sentence patterns and dialogue while preserving the continuous lesson document. | Owner answer 4: “ok”. |
| DS-U-16 | Display abstract grammar formulas without literal formula playback; put speakers on their complete Japanese example sentences. | Owner answer 5 accepting DS-P-06. |
| DS-U-17 | Lesson toolbar contains the section-jump menu, an app-wide furigana toggle and a separate stop action while playing. | Owner answer 1: “ok” to the complete toolbar proposal. |
| DS-U-18 | First launch presents a level-selection screen. Later launches remember the selected level rather than requiring selection again. No default N5 selection is approved. | Owner answer 2. |
| DS-U-19 | Provide the learned-state control at the beginning of the lesson and status indicators in lesson lists. Show a confirmation explaining the affected range before a change affects multiple lessons; preserve the B-U-58 independent prefixes. | Owner answer 3: “ok” to placement and range-confirmation proposal. |
| DS-U-20 | Use touch-and-hold to reveal a context menu for favorite actions, rather than visible star/ellipsis controls. Preserve native pointer invocation; the earlier specialized accessibility requirement is deferred under DS-U-47. | Owner context-menu choice and later accessibility-scope correction. |
| DS-U-21 | Kanji navigation follows unit list → unit page with a character grid → character detail showing meaning, Sino-Vietnamese, On/Kun and examples. | Owner answer 1 accepting the proposed hierarchy. |
| DS-U-22 | In Kanji meaning detail, include corresponding sentence examples that prioritize vocabulary and grammar already learned, evaluated from manually marked learned lessons. DS-U-26–29 extend and refine this requirement. | Owner addition in answer 1 and subsequent example-selection answers. |
| DS-U-23 | Favorites defaults to all saved types, newest saved first, with filters by content type and N5/N4. | Owner answer 2 accepting the full proposal. |
| DS-U-24 | A magnifying-glass entry at the main screen searches the app globally; within a lesson it searches that lesson. Group results by content type; activation opens the containing lesson/unit at the matching content location. | Owner answer 3 accepting the full proposal. |
| DS-U-25 | Hiragana/Katakana uses tables covering basic, voiced/semi-voiced and combined sounds, including extended Katakana loanword combinations. Include examples for the sounds and cell-tap pronunciation. The owner requests the fullest practical coverage; exact modern/historical inventory and handling of non-independent sounds still require a concrete inventory. | Owner answer 4 accepting the proposed format and adding full coverage/examples. |
| DS-U-26 | Apply learned-aware selection to sentence examples throughout the app except the alphabet area. Alphabet examples use the most basic words/sentences because the learner studies the alphabet first. This describes beginner suitability, not a mandatory prerequisite or a new lock on lessons. | Owner example-selection answer 1. |
| DS-U-27 | In this phase, prepare and review the sentence candidates in advance, bundle them offline, and select/order them at use time. Do not generate/rewrite sentences in the running app. | Owner example-selection answer 2. |
| DS-U-28 | Permit the target character/word itself to be new. Prefer candidates whose supporting vocabulary/grammar is learned; if none exists, still use the simplest corresponding candidate instead of hiding the example. Exact simplicity/ranking and unfamiliar-content presentation remain open. | Owner answer 3 accepting the target-exception/fallback proposal and explicitly requesting the simplest sentence. |
| DS-U-29 | Determine familiar supporting content from the union of lessons actually marked learned in N5 and N4. Do not infer N5 learning from selecting/learning N4, and do not merge the independent learned prefixes. | Owner example-selection answer 4. |
| DS-U-30 | AI-based content authoring is a possible future direction, not a current in-app generation feature or authorization to add network/API dependencies. Existing development-time authoring approvals are not revoked. | Owner future-phase note in answer 2. |
| DS-U-31 | Keep the curriculum available offline in the app package and load detail on demand. Optimize installed size, launch, memory and rendering through bounded work/caches and efficient search/widget access; require measured acceptance under [performance-and-footprint.md](performance-and-footprint.md). | Owner accepted the local-content assessment: “ok, hãy đưa ràng buộc này vào design system để đảm bảo tối ưu nhất về mặt dung lượng và hiệu năng”. |
| DS-U-32 | The standalone trailing “3” was a typing mistake. It does not specify an example count or select an additional option. | Owner answer 1: “gõ dư”. |
| DS-U-33 | Rank matching examples by learned supporting grammar first, then fewer unfamiliar words, then simpler/shorter sentences. The grammar point currently being taught may itself be new, analogous to the target character/word exception. Exact editorial simplicity encoding and deterministic ties still need specification. | Owner answer 2 accepting the full ranking/target-grammar proposal. |
| DS-U-34 | Keep dialogue scripts unchanged. Learned-aware selection applies to accompanying sentence examples; do not introduce alternative dialogue versions or replace/reorder turns according to learned state. | Owner answer 3: “giữ nguyên”. |
| DS-U-35 | Use one shared language choice for the app interface and translated meanings/explanations. Do not add separate UI/content language pickers. Japanese remains the taught language. | Owner answer 4: “lựa chọn chung”. |
| DS-U-36 | Initial language and appearance follow System. After level selection, open the Lessons list. Lessons and Kanji share the remembered N5/N4 selection through a visible level switch. | Owner answer 1 accepting the initial-settings proposal. |
| DS-U-37 | Use the system's Dynamic Type size, with appropriate type size/weight roles for each content kind. Do not add an independent in-app font-size control. | Owner answer 2, with explicit typography/UX direction. |
| DS-U-38 | Select examples on page opening from the latest saved learned state and do not automatically replace visible/speaking examples. The initial max-three/more ambiguity is resolved by DS-U-40. | Owner answer 3 and later clarification. |
| DS-U-39 | Accept the Small/Medium/Large widget upper-count matrix, reductions for long text/large type, concise Lock Screen content, and shared app language/furigana preferences. Add an Extra Large iPad design; its concrete layout/count is later approved by DS-U-41. | Owner answer 4 and later visual approval. |
| DS-U-40 | At most three example sentences total per target. Do not provide a “more examples” action. This resolves DS-U-38's count ambiguity and supersedes the earlier expansion proposal. | Owner answer 1: “tối đa 3 câu, không cần xem thêm”. |
| DS-U-41 | Approve the concrete Teal, type hierarchy and spacing in foundations.md/the review, plus Extra Large up to eight vocabulary items, four sentence-pattern examples or four Kanji, reducing counts for readability. The approved token contract is tokens.json; native accessibility/layout still requires verification. | Owner answer 2 accepting the complete visual/Extra Large proposal. |
| DS-U-42 | Live search with a 0.5-second debounce; case-insensitive and Vietnamese-diacritic-insensitive matching; equivalent Hiragana/Katakana kana matching; rank within each content group by exact → prefix → contains. | Owner answer 3 accepting the proposal and specifying debounce 0.5s. |
| DS-U-43 | Organize kana into basic, voiced/semi-voiced, combined/extended and special-use groups, with small-kana/gemination/long-vowel guidance. Put historical/rare forms in a separate reference area so the main beginner material focuses on modern Japanese. | Owner answer 4 accepting the complete organization proposal. |
| DS-U-44 | A single-lesson learned-state change and remove-favorite action apply immediately with brief success feedback; multi-lesson changes retain range confirmation. On save failure preserve the last committed state and offer retry. Favorites lists show directly saved parents/items only; a saved lesson/unit remains one entry, without expanding its children into app list entries. | Owner answer 1 accepting the full local-write/favorites proposal. |
| DS-U-45 | Display Sino-Vietnamese readings only when the selected shared language is Vietnamese. Apply this to app detail and optional widget detail. Existing search-field approval is unchanged. | Owner answer 2: “chỉ khi chọn tiếng việt”. |
| DS-U-46 | Explicit speaker activation uses media volume even in device silent mode. Stop on phone/audio interruption or headphone disconnection and do not automatically resume. Playback is never automatic on entry. | Owner answer 3 accepting the full audio proposal. |
| DS-U-47 | Specialized Accessibility support/acceptance is out of the current phase, superseding the earlier broad accessibility scope. DS-U-48/49 explicitly retains system text sizing, supported-language RTL and native state presentation. Learning-content TTS remains approved functionality. | Owner scope correction and subsequent boundary clarification. |
| DS-U-48 | Retain system Dynamic Type and the approved content-specific size/weight hierarchy. Defer VoiceOver and specialized Accessibility support/testing; do not turn that deferral into fixed app text sizing. | Owner answer 1: “đúng” to the precise boundary proposal. |
| DS-U-49 | Retain native RTL for Arabic/Hebrew with correctly ordered Japanese blocks, a concise English fallback-language label, and scoped native loading/empty/error presentation preserving the current context. | Owner answer 2: “đúng” to the complete non-accessibility proposal. |

## Decisions made within the delegated navigation scope

| ID | Decision | Basis |
| --- | --- | --- |
| DS-D-01 | Keep the four approved destinations stable. Use native tabs in compact layouts; native adaptive tab/sidebar presentation in wider environments. For Lessons/Kanji, show collection and selected detail together when usable width permits; an optional third navigation column can appear where it preserves readable content. Collapse into the same logical hierarchy as width decreases. Avoid fixed device-model assumptions and mandatory three-column presentation. | DS-U-11; Apple Tab bars, Sidebars and iPad adaptive-design guidance, linked in screens-and-playback.md. |
| DS-D-02 | Preserve active destination, selected level/lesson and current search through geometry changes. Geometry changes alone do not constitute leaving the logical playback screen. Do not add reading-position restoration across app relaunch. | Existing B-I-08/B-U-27/47 and DS-U-11. |
| DS-D-03 | Map content kinds to scalable system typography roles and weights under the owner's explicit typography direction, detailed in foundations.md. Numerical reference sizes describe the standard-size design sample, not fixed production text size. | DS-U-37; system-font/native-accessibility baseline. |

Official documentation remains English under B-U-23. Existing approved requirements do not need repeated approval.

## Color exploration — Teal values approved under DS-U-41

These are authored sRGB values, not claims about Apple's system color values. Teal and the visual foundation values are approved under DS-U-41; Blue/Indigo remain archived exploration. Neutral HTML backgrounds are review approximations; native semantic background/text/separator/material roles are normative in foundations.md.

| Option | Light accent / on accent | Dark accent / on accent | Recommendation |
| --- | --- | --- | --- |
| A · Blue | `#0066CC` / `#FFFFFF` | `#5AA9FF` / `#000000` | Earlier recommendation; not selected. |
| B · Indigo | `#5856D6` / `#FFFFFF` | `#B0A9FF` / `#000000` | Quieter violet-blue alternative. |
| C · Teal | `#007C78` / `#FFFFFF` | `#64D8CB` / `#000000` | Approved under DS-U-41; see tokens.json for the complete contract. |

Use the approved custom adaptive Teal accent and native semantic neutral roles. Platform rendering/accessibility verification is still required; visual approval is not a device or release pass.

## Clarification queue

Questions are grouped for successive owner rounds, not all asked at once. None of the alternatives below is an approved default.

| ID | Open decision | Dependencies |
| --- | --- | --- |
| DS-Q-01 | RESOLVED: adaptive custom Teal, native semantic neutrals and approved foundation values under DS-U-41; tokens.json is authoritative. Native rendering proof remains implementation work. | Token specification. |
| DS-Q-02 | RESOLVED: balanced density, system-only Dynamic Type and content size/weight roles under DS-U-08/37/41/48 and DS-D-03. | Text styles, spacing, content components. |
| DS-Q-03 | RESOLVED: continuous lesson document with topic first under DS-U-09 and section-jump menu under DS-U-15. | Lesson navigation. |
| DS-Q-04 | RESOLVED: choose level once, remember it, open Lessons and share a visible level switch with Kanji under DS-U-18/36 and DS-D-01/02. | Screen contracts. |
| DS-Q-05 | RESOLVED product behavior: context menu, all-types default/newest-first/type-level filters, directly saved parent/item rows and immediate remove/save feedback under DS-U-20/23/44. Remaining deterministic presentation details are implementation contracts. | Favorites screens and components. |
| DS-Q-06 | RESOLVED UI: global/scoped entry, grouped exact-location results and 500ms live search/matching under DS-U-24/42, with session/group/native-state bindings in implementation-guide.md. | Search screens and states. |
| DS-Q-07 | RESOLVED product behavior: header control/list status/multi-change range confirmation under DS-U-19 and immediate single-change/success/failure/retry under DS-U-44. No additional undo feature is selected. | Existing B-U-58 semantics remain fixed. |
| DS-Q-08 | RESOLVED UI: comprehensive modern/extended tables, special-use groups, examples and separate historical/rare reference under DS-U-25/43. Complete reviewed teaching inventory remains an authoring dependency. | No displayed romaji remains B-U-27. |
| DS-Q-09 | RESOLVED product behavior: unit → grid → character detail and learned-aware examples under DS-U-21/22; Sino-Vietnamese is visible only in Vietnamese under DS-U-45. Exact rendering/content inventory remains implementation/authoring work. | Kanji screens and localization. |
| DS-Q-10 | RESOLVED: native system/ruby/translation hierarchy and shared toggle; retain system text size under DS-U-48. Ruby wrapping is implementation evidence; specialized VoiceOver is deferred. | Text renderer contract. |
| DS-Q-11 | RESOLVED: shared language/System default, Vietnamese-only Sino-Vietnamese, native RTL and English fallback indication under DS-U-35/36/45/49. | Settings and multilingual layouts. |
| DS-Q-12 | RESOLVED: single/restart/turn/highlight/stop plus silent-mode media playback, interruption/disconnection stop and no auto-resume. Native pending/error/setup presentation follows the state contract. | See screens-and-playback.md and components.md. |
| DS-Q-13 | RESOLVED UI: approved counts/XL/readability/shared preferences and compact-family/source/configuration bindings in widgets.md. Actual family eligibility and snapshots remain native evidence. | Existing source/timeline/open-app semantics remain fixed. |
| DS-Q-14 | RESOLVED initial product defaults under DS-U-18/36/37: choose level once, remember it, open Lessons, System language/appearance, system-only text sizing. No additional onboarding. Existing default-on furigana remains. | Entry and empty-state flows. |
| DS-Q-15 | RESOLVED design: approved foundations/tokens, native symbol roles/shapes/feedback/materials and no added custom motion/haptic scheme. No speculative feature is implied. | Review concrete proposals after core journeys. |
| DS-Q-16 | DEFERRED specialized Accessibility under DS-U-47/48. System text sizing and localization remain current requirements under DS-U-48/49. | No VoiceOver/specialized Accessibility acceptance gate this phase. |
| DS-Q-17 | RESOLVED UI: committed-write feedback/failure/retry and scoped unavailable/error states under DS-U-44/49. Content-deletion/replacement migration policy remains a separate domain/release dependency; the UI does not invent one. | Coordinate engineering contracts without inventing recovery policy. |
| DS-Q-18 | DELIVERED v1.0: normative documents, approved tokens, integrated HTML and focused widget/type/lesson/entry sketches; inspect README.md and acceptance.md for checks and explicit browser/native limits. | Complete preceding questions before claiming implementation readiness. |
| DS-Q-19 | RESOLVED design: reviewed offline candidates, learned-prefix union, target exceptions, ordered familiarity/simplicity, total cap three, fixed dialogue, and stable visible examples. Dependency-bank completeness remains authoring evidence. | See example-selection.md. |
| DS-Q-20 | RESOLVED: the standalone trailing “3” was a typing mistake under DS-U-32; it is not a count. | No example-count inference. |
| DS-Q-21 | RESOLVED by DS-U-48: retain system Dynamic Type; defer VoiceOver/specialized Accessibility support/testing. | Typography retained. |
| DS-Q-22 | RESOLVED by DS-U-49: retain RTL localization, English fallback label and scoped native loading/empty/error. | Localization/state retained. |

## Current evidence

The initial round added documentation and a palette review. The next round records Teal/balanced-density/continuous-lesson/audio-placement decisions and adds a lesson sketch using existing authored vocabulary, grammar, examples and dialogue. The sketch is excerpted, not a reduced curriculum requirement. HTML selections are local exploration and must be confirmed in the conversation unless within explicit delegated scope. Color calculations are bounded to specified opaque pairs; they do not establish native accessibility acceptance or dynamic material contrast.

Static checks passed for JavaScript syntax, local Markdown links and the specified opaque accent/on-accent and accent/secondary-surface pairs (all above 4.5:1). Visual/browser interaction checks remain unperformed because local browser use is disabled in Work settings. The temporary localhost server was stopped. No settings were changed.

For the lesson-review round, JavaScript syntax, embedded JSON and local links were checked. The excerpt contains three vocabulary entries, one grammar explanation, its two matching complete examples and all eight turns of the first authored dialogue. Example-to-pattern alignment and full-dialogue inclusion were checked against lesson-01.json. Browser interaction, native audio and device accessibility remain unverified; the prior browser-setting limitation still applies.

The playback-confirmation round replaces the obsolete speaker-to-stop prototype behavior with separate idle/playing speaker glyphs and unconditional restart-on-tap, including a current segment selected during full-dialogue playback. It records the owner's answers without promoting unreviewed geometry or stop-button placement to approved design tokens. See components.md for the interaction contract and acceptance cases.

The entry/context-menu round resolves toolbar stop/furigana placement under DS-U-17, first-entry/remembered level under DS-U-18, multi-lesson confirmation under DS-U-19 and touch-and-hold favorites under DS-U-20. The entry sketch includes an explicitly illustrative lesson-list landing and range-confirmation dialog. The lesson sketch selects aligned excerpts for N5 lesson 1 or N4 lesson 26, mirrors toolbar/review furigana state and offers a browser-only favorite menu on eligible parent/item targets. Embedded audio and menu states remain simulations; no app persistence or native-runtime pass is claimed. The browser-use limitation remains unchanged.

The Kanji/search/favorites/alphabet round records DS-U-21–25. Source inspection confirms that character/unit examples are currently words or compounds; they are not a tagged sentence-candidate bank. Lesson sentence examples include grammar-point references but no complete vocabulary-dependency references. No learned-aware sentence ranking is implemented or claimed. No alphabet authoring inventory was found in the existing docs. These are content/contract gaps to address after clarification, not grounds for inventing example eligibility or a reduced alphabet scope.

The example-selection round records DS-U-26–30: app-wide example scope with a kana exception, reviewed offline candidates, simplest-candidate fallback, and familiarity derived only from actually marked lessons across both levels. AI content authoring is a future consideration. The standalone trailing “3” was later resolved as a typing mistake under DS-U-32. Runtime selection, sentence dependency authoring and content-bank completeness are not claimed.

The ranking/language round records DS-U-32–35: no count inference from the typo, grammar-first example ranking, a target-grammar exception, unchanged dialogue scripts and one shared interface/content language choice. The existing performance/footprint constraint DS-U-31 and its document are preserved. No runtime selection or new localization coverage is claimed.

The defaults/type/widget round records DS-U-36–39: System defaults, Lessons landing/shared level switch, system-only scalable text roles, the max-three example instruction with its expansion ambiguity, stable visible examples and accepted Small/Medium/Large counts. Extra Large is explicitly requested and has a concrete proposed layout in foundations-widgets-review.html. SDK inspection confirmed the selected iOS 27.2 WidgetKit interface declares systemExtraLarge and systemExtraLargePortrait; no device/gallery/rendering eligibility is claimed.

Static checks for that round passed for JavaScript/JSON syntax, local links, unique decision IDs, equality of the review's embedded token snapshot, and the 8/4/4 authored preview item counts. Proposed opaque accent/on-accent contrast ratios are 5.06:1 Light and 12.23:1 Dark; proposed increased-contrast pairs are 7.64:1 and 15.83:1. These calculations do not verify native semantic surfaces or material rendering. Browser/native visual checks remain unperformed under the existing local-browser setting limitation.

The visual/search confirmation round records DS-U-40–43: a total three-example cap without expansion, approved foundation/XL values, live search with 500ms debounce and the approved kana group/reference structure. Token status changes reflect owner design approval only, not implementation or runtime verification. Earlier proposal-stage notes remain historical evidence; the current requirement rows and normative contracts take precedence.

The local-state/audio/scope round records DS-U-44–47: immediate small changes with failure/retry, direct-only favorites rows, Vietnamese-only Sino-Vietnamese display, explicit playback in silent mode with interruption/disconnection stop, and current-phase Accessibility deferral. The system-text-size boundary and remaining localization/state parts are explicitly pending rather than inferred. The new scope does not revoke content pronunciation or the approved 19 languages.

The final scope clarification records DS-U-48/49: retain system text sizing, RTL/localization and native states while deferring VoiceOver/specialized Accessibility support/testing. Remaining data packaging, editorial inventory and physical-runtime evidence are implementation/content dependencies, not permission to reopen resolved owner decisions or invent replacement product behavior. Current bindings are documented in implementation-guide.md and acceptance.md.

Final design completion: the integrated review and widget gallery are present, with local representative data and no external runtime dependency. The native app/package/content-bank and specialized Accessibility pass are not claimed. Normalized lookup, per-level prefix helper and source-fixture checks are documentation/review verification only. The light browser selection tint was made slightly lighter for text legibility without changing the approved Teal accent or native semantic roles.
