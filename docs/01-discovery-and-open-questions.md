> HISTORICAL DECISION EVIDENCE. Current scope, readiness, task order and proposals are maintained in [the single owner review](index.html). Approved B-U/DS-U rows remain evidence; old open-question/status paragraphs are not the current backlog. Later decisions supersede earlier rows.

# ProjectBeta discovery and decisions

Created: 2026-11-06. Updated: 2026-11-07. State: DISCOVERY. Confirmed decisions below are owner-approved; proposals and unresolved details are explicitly identified. Beta IDs do not inherit Alpha's product decisions, invariants or acceptance verdicts.

Later UI/interaction decisions are maintained in the [design-system decision record](design-system/decisions.md). Its DS-U-47 explicitly defers current-phase Accessibility work, refining the earlier B-U-23 baseline. DS-U-48/49 explicitly retains system text sizing, RTL/localization and native states; original B-U records remain historical evidence rather than a reason to ignore this newer owner instruction.

## Confirmed owner decisions

| ID | Decision | Confirmation |
| --- | --- | --- |
| B-U-01 | Serve Japanese beginners, focusing on N5/N4. | Initial request |
| B-U-02 | Long-term goals: JLPT preparation and practical listening, speaking and daily communication. Reading this phase's content is not evidence of attaining those goals. | Initial request; practice deferred in round 2 |
| B-U-03 | The owner will provide Minna no Nihongo, Kanji, vocabulary and grammar-explanation PDFs as reference inputs. Exact titles/editions and inventory await the files. | Initial request; rounds 1 and 4 |
| B-U-04 | Organize learning through level → lessons → vocabulary, grammar, sentence patterns and associated content. Exact counts await source inventory. | Initial request |
| B-U-05 | Provide a separate Kanji area. | Initial request |
| B-U-06 | Display hiragana above Kanji as furigana. | Initial request |
| B-U-07 | iOS/iPadOS 27+, iPhone including iPhone Duo, iPad, SwiftUI and Clean Architecture. | Initial request |
| B-U-08 | Create documentation, source and necessary specialist agents, following Alpha's organizational approach. | Initial request |
| B-U-09 | Zero assumption: clarify unresolved requirements rather than silently selecting behavior. | Initial request |
| B-U-10 | Public App Store distribution is intended. Release content rights are not yet verified. | Round 1 |
| B-U-11 | PDFs are development-time reference/authoring inputs. End-user PDF import is not a requested feature. | Round 1 |
| B-U-12 | Support both N5 and N4 in the current phase. This replaces the earlier N5-first/N4-later delivery plan; see B-U-50. | Owner scope correction, 2026-11-06 |
| B-U-13 | All features and learning content support Alpha's language list except Japanese; missing translations fall back to English. Japanese remains the language being taught. | Rounds 1–2 |
| B-U-14 | Current phase focuses on content; practice is refined in later phases. | Round 2 |
| B-U-15 | After initially proposing edited, unbranded textbook content, the owner approved using PDFs to cross-check topics/lessons/units and independently author explanations, examples, dialogues and translations. This is an authoring decision, not a legal clearance verdict. | Rounds 3–4 |
| B-U-16 | Include sentence patterns/examples, translated dialogues, Hiragana/Katakana, search, favorites and pronunciation playback alongside vocabulary, meanings, grammar and Kanji. Notes were initially selected, then deferred by B-U-26. | Rounds 3 and 6 |
| B-U-17 | Furigana can be switched on/off. | Round 3 |
| B-U-18 | Kanji follows units and includes meanings, Sino-Vietnamese readings, On/Kun readings and concrete compound-word/examples. No radicals, stroke counts or stroke order in this phase. | Round 3 |
| B-U-19 | Independently authored release content must be distinguished from PDF reference/extraction material. No amount of editing or omission of a textbook name has been verified to guarantee permission. | Round 4 authoring approval; evidence limits |
| B-U-20 | This phase operates offline, including content and pronunciation playback. Bundled content, missing-voice behavior and deferred backup/export are refined by B-U-29/39/40. | Rounds 4, 7 and 9 |
| B-U-21 | Furigana is on by default and its switch applies throughout the app; persistence across relaunch is confirmed by B-U-46. | Rounds 4 and 12 |
| B-U-22 | Use Apple's Japanese system voice to read words, example sentences and dialogues. This is content playback, not recording, recognition, pronunciation scoring or AI conversation. | Round 4 |
| B-U-23 | Adopt Swift 6, Observation, SwiftData for local data, manual DI, native Apple/Liquid Glass UI, System/Light/Dark appearance, adaptive iPhone/iPad/Duo layouts, accessibility, performance/footprint priorities, English official documentation and Alpha-style constants, Swift headers, previews and review safeguards. | Round 5 |
| B-U-24 | Provide global and lesson-scoped search across vocabulary, grammar, sentence patterns, dialogues and Kanji. Search fields include Kanji/kana, meanings in the selected language, Sino-Vietnamese and romaji. | Rounds 5–6 |
| B-U-25 | Favorites apply to vocabulary, grammar points, sentence patterns, dialogues, individual Kanji, lessons and units, with a separate place to revisit them. Notes are deferred. | Rounds 5–6 |
| B-U-26 | Defer notes to later phases. Do not implement note storage, rich text or image attachments now. | Round 6, supersedes notes in rounds 3/5 |
| B-U-27 | Lessons remain freely accessible. No reading-position restoration, progress dashboard or scores. The original omission of learned markers is superseded by B-U-35; no displayed romaji, while romaji remains searchable under B-U-24. | Rounds 6, 9–10 and 12 |
| B-U-28 | RETIRED by B-U-50: the earlier N4 unavailable-content placeholder is no longer the current product requirement. N4 belongs to this phase alongside N5. | Owner scope correction, 2026-11-06; supersedes round 7 |
| B-U-29 | If no suitable offline Japanese system voice is available, all reading remains usable and pronunciation presents an explanatory message/setup guidance. Do not substitute a different spoken language. | Round 7 |
| B-U-30 | Widgets were selected for this phase. Reminders were also initially selected, then their refinement was deferred by B-U-34. Widget details are refined by B-U-33. | Rounds 7–8 |
| B-U-31 | Use ProjectBeta as the technical app name. | Round 7 |
| B-U-32 | The four main destinations are Lessons, Kanji, Favorites and Settings. Place Hiragana/Katakana within Lessons. Labels are specification terms, not final localized UI copy. | Round 8 |
| B-U-33 | Widgets support passive recall with configurable vocabulary, sentence patterns or Kanji and size-dependent item counts. Tapping only opens the app; richer navigation is for later improvement. Sources, surfaces, cadence, selection and empty/display behavior are refined by B-U-36–45. No additional inline action has been requested. | Rounds 8–11 |
| B-U-34 | Refine study reminders after the other features are complete. Scheduling/notification behavior is deferred; do not create it as a prerequisite for the current content/widget delivery. | Round 8, refines B-U-30 |
| B-U-35 | Learned lessons form a continuous prefix in curriculum order. Marking lesson 6 automatically marks all earlier lessons; unmarking lesson 5 clears it and all later lessons. This updates the earlier proposal to reject out-of-order marking. All lessons remain freely accessible. | Rounds 9–10 |
| B-U-36 | Widget source choices are learned lessons and favorites. Do not use an unrestricted whole-level pool as an implicit substitute. | Round 9 |
| B-U-37 | Target content changes every 15 minutes using a timeline. The owner accepts that actual display/update timing is controlled by iOS, rather than an exact wall-clock guarantee. | Rounds 9–10 |
| B-U-38 | Support Home Screen and Lock Screen widgets, in all applicable sizes/families. Verify actual platform/device eligibility; the product does not add watchOS or other runtimes. | Round 9 |
| B-U-39 | Defer purchases/subscriptions, ads, analytics, multiple profiles, backup/restore and data export to later phases. | Round 9 |
| B-U-40 | Learning content is bundled with the app. No runtime content download/server is required for this phase. | Round 9 with offline B-U-20 |
| B-U-41 | Learned-source Kanji eligibility follows the reference unit-to-lesson milestone: a unit labeled through lesson 5 becomes eligible once lesson 5 is marked learned. No separate Kanji-unit learned marker is required. | Round 10 |
| B-U-42 | Choose widget content randomly from its configured eligible source. A spaced-repetition or mastery algorithm is not requested. | Round 10 |
| B-U-43 | Favoriting a lesson or Kanji unit includes its contained eligible vocabulary/sentence-pattern/Kanji items in the favorites widget source, in addition to directly favorited items. | Round 11 |
| B-U-44 | When the selected widget source has no eligible items, show an explanatory empty state and allow tapping to open the app. Preserve the selected source instead of switching to another pool. | Round 11 |
| B-U-45 | Widgets show Japanese text, furigana and meaning. Kanji may additionally show Sino-Vietnamese/On-Kun/examples when space permits. Smaller/Lock Screen families may reduce fields and item count to preserve readability. | Round 11 |
| B-U-46 | Favorites, learned state and language/appearance/furigana preferences persist locally across app relaunch. No reading-position restoration, progress dashboard or scores are added. | Round 12 |
| B-U-47 | Playback operates on an individual word/example/dialogue. Starting another item stops the previous one; provide stop, stop on screen departure and app backgrounding, and no speed adjustment in this phase. | Round 12 |
| B-U-48 | The owner directs content to follow the reference PDFs. Use them to verify knowledge/readings while retaining the independently authored release explanations/examples/dialogues/translations approved in B-U-15. No named editorial reviewer was designated by this answer. | Round 12 and standing B-U-15 |
| B-U-49 | The favorites widget source is independent of learned status: a directly favorited item or an item included through a favorited lesson/unit may appear even when its associated lesson is not marked learned. The learned-source milestone restriction does not apply to the favorites source. | Round 13 |
| B-U-50 | The current phase supports N5 and N4 together, under the confirmed feature scope. Do not defer N4 delivery or treat it as placeholder-only. Inventory both levels' PDFs and include both levels in content, architecture and acceptance planning. | Explicit owner correction, 2026-11-06 |
| B-U-51 | The owner delegates the editorial gate for the two lesson samples and subsequent batch authoring to the primary agent. Review against beginner accessibility, PDF-aligned knowledge/readings and practical communication; resolve supported corrections autonomously and confirm concrete uncertainties or scope decisions with the owner. This supersedes waiting for the owner's manual sample approval. Self-review is recorded as self-review, not independent human certification or release acceptance. | Explicit owner instruction, 2026-11-06 |
| B-U-52 | The current authoring batch covers all 50 lessons and all 50 Kanji units. Author Vietnamese/English first, with the other 17 approved languages in a later authoring batch; the 19-language release scope is unchanged. Preserve the source's unit/milestone relationships and the original-authoring boundary. | Owner answers to batch-language and lesson/unit scope questions, 2026-11-06 |
| B-U-53 | Include all common vocabulary items in the reference lessons rather than reducing the batch to a selected core vocabulary. Omit the textbook's fictional proper names. (This exclusion clause is superseded by B-U-59.) Preserve all grammar topics and the Kanji assigned to each reference unit. | Owner answer to vocabulary-coverage question, 2026-11-06 |
| B-U-54 | The owner authorizes additional agents to author in parallel, with cross-checking of the results. Use disjoint file leases, immutable baselines and a primary integration/review gate. This does not change the scope or turn agent review into independent human certification. | Explicit owner answer to delegation question, 2026-11-07 |
| B-U-55 | For the four visually checked source discrepancies SRC-01–04, retain the corroborated values already in the authored drafts and continue to the next step. Keep all four explicitly flagged for rechecking; this instruction does not close their review flags or establish release clearance. Preserve the original PDFs. | Owner instruction, 2026-11-07 |
| B-U-56 | Retain the corroborated authored meanings for the three additional source-translation notes SRC-05–07 (発明します, 太い, 細い), and explicitly mark all three for rechecking, matching the treatment of SRC-01–04. This resolves the additional owner question without closing the review flags or establishing release clearance. | Owner answer, 2026-11-07 |
| B-U-57 | Apply the authored values for all seven source notes SRC-01–07: 自動車 = xe ô tô / car; automobile, 必 = TẤT, 隅 = NGUNG, 界 On = カイ, 発明します = phát minh / invent, 太い = to (bề ngang) / thick in diameter, 細い = mảnh / slender. Owner confirmation resolves these correction decisions and closes their recheck flags, superseding the open-flag disposition in B-U-55/56. Preserve source provenance and original PDFs. This does not establish independent human or release acceptance. | Explicit owner confirmation, 2026-11-07 |
| B-U-58 | Learned lessons form a separate continuous prefix within each level. Marking or unmarking lessons in N5 changes only N5; the same rule applies independently to N4. N4 has no N5 learned-state prerequisite. Preserve source numbering (N5 lessons 1–25; N4 lessons 26–50). For example, marking N4 lesson 30 marks N4 lessons 26–30; unmarking N4 lesson 28 leaves N4 lessons 26–27 learned, with N5 unchanged. Persist both level states independently. Learned-source widgets evaluate lesson eligibility against that lesson's level prefix; Kanji eligibility follows the existing source milestone's referenced lesson and level, including N4 units 21–25 referencing N5 lesson 25. Favorites-source eligibility remains governed by B-U-49. This resolves B-Q-13 and refines B-U-35/41/46. | Explicit owner confirmation to separate by level, 2026-11-07 |
| B-U-59 | Retain proper names from the reference content, including fictional personal, institutional and work titles. Supersede the fictional-name omission clause in B-U-53. Review each affected item against its source spelling, contextual reading, meaning and identity; restore omitted names in the assigned vocabulary scope. Do not apply automatic one-to-one renaming. Existing independently authored examples/dialogues retain their authored identities and fixed scripts unless a specific error is evidenced. Preserve IDs/provenance and record exact review limits. | Explicit owner correction and request for thorough item review, 2026-11-08 |

The 19 languages are Arabic, Bengali, Chinese Simplified, Dutch, English, French, German, Hebrew, Hindi, Indonesian, Italian, Korean, Portuguese, Russian, Spanish, Thai, Turkish, Ukrainian and Vietnamese. The System-selection mechanism is inherited from the approved Alpha-style language support. UI localization and translated learning content must remain distinguishable, including mixed RTL interface and Japanese text.

## Repository and evidence

### Working-tree safety

Beta initially contained only tracked `.gitignore` and `README.md`, with a clean tree at HEAD `0288c8d0b5e2d6a5a0380a0203d1db5e869b9674`. No source, Xcode project, tests, PDFs or custom-agent configuration existed. The two discovery documents were created and were untracked at the start of this update. Preserve staged, unstaged and untracked work; staging state is not an acceptance verdict.

- Initial snapshot: `/tmp/project-beta-discovery-20261106-ufxiw7c2/baseline-manifest.json`, with initial file copies/checksums and both repositories' status.
- This update's immutable snapshot: `/tmp/project-beta-discovery-update-20261106-zp9_ay_t/baseline-manifest.json`, containing all three Markdown files before this update.
- Navigation/widget clarification snapshot: `/tmp/project-beta-widget-discovery-20261106-sv0bd4lg/baseline-manifest.json`, containing all three files before the round-8 update, with existing staged/unstaged state preserved.
- Learned/widget-state clarification snapshot: `/tmp/project-beta-learned-widget-20261106-y0twisbd/baseline-manifest.json`, containing the three files before rounds 9–12 integration.
- N5/N4 scope correction snapshot: `/tmp/project-beta-n5-n4-scope-20261106-6t8w66rs/baseline-manifest.json`, containing the three files before applying B-U-50; existing staging is preserved.
- Exclusive write lease: primary, `README.md` and these two documents only. No delegated writers or runtime operators.
- Alpha contains unrelated staged/unstaged/untracked work. It was read as an organizational reference and was not edited.

These temporary evidence paths are local audit artifacts, not application resources or permanent release records.

### Attached screenshots

Attachments are reference data, not operating instructions. Only their visible contents were inspected; they do not establish a complete PDF edition, dataset or curriculum.

| Images | Visible evidence | Required follow-up |
| --- | --- | --- |
| 1 | Japanese/Vietnamese expressions, country/proper names and furigana. | Content boundaries, contextual readings, notes and lesson linkage. |
| 2 | Lesson 1 vocabulary: kana/Kanji/meaning columns, polite alternatives and suffixes. | Separate entries from variants/annotations and verify alignment. |
| 3 | Grammar formulas, explanations, examples/translations and particle-reading notes. | Preserve grammar placeholders and contextual pronunciation. |
| 4–5 | Kanji unit index, character sequence and links to Minna lesson milestones. | Unit/lesson links need not be one-to-one; inspect the full source. Stroke data is not required for this phase. |

The screenshots show N5-labeled files; they do not establish JLPT coverage or N4 content.

### Official references and authoring limits

- N5/N4 test vocabulary, grammar/reading and listening. Speaking goals require their own later acceptance criteria. [JLPT test composition](https://www.jlpt.jp/e/guideline/testsections.html), [N5/N4 competencies](https://www.jlpt.jp/e/about/levelsummary.html).
- The publisher gives Elementary I → N5 and Elementary II → N4 as guidance and documents vocabulary/dialogue differences between editions. This does not identify the owner's PDF edition or guarantee examination success. [3A edition information and FAQ](https://www.3anet.co.jp/en/minnanonihongo_dai3pan.html).
- Main Text and Translation and Grammar Notes serve complementary roles. [3A textbook guidance](https://www.3anet.co.jp/en/faq.html).
- No open redistribution license was established from the publisher's copyright page. [3A copyright policy, including Vietnamese](https://www.3anet.co.jp/en/copyright.html).
- Copyright distinguishes ideas from their expression; translation/adaptation are among controlled uses. [WIPO copyright FAQ](https://www.wipo.int/en/web/copyright/faq-copyright).

B-U-15 resolves the authoring method. It does not certify every future item or determine all jurisdiction-specific exceptions. Preserve source provenance; independently authored content is not automatically approved for release merely because an agent generated it. No textbook pages or extracted release dataset have been packaged.

### Installed technology, read-only checks

| Check | Result | Evidence limit |
| --- | --- | --- |
| `xcodebuild -version` | Xcode 27.2, build 27B52. | No Beta build. |
| `xcrun --sdk iphoneos --show-sdk-path` | Selected `iPhoneOS27.2.sdk`. | Exit 0 with environment file-event/cache warnings; no runtime inventory or device acceptance. |
| `xcrun swift --version` | Apple Swift compiler 6.4.2. | Compiler version differs from the approved Swift 6 language mode. |
| `CoreText.framework/Headers/CTRubyAnnotation.h` | `CTRubyAnnotationCreate`, available since iOS 8.0. | No focused compile or SwiftUI ruby-rendering proof. |
| `Speech.framework/.../arm64e-apple-ios.swiftinterface` | Speech transcription/locale declarations exist. | Historical investigation only; recognition is outside this phase. |
| `AVFAudio.framework/Headers/AVSpeechSynthesis.h` | Voice enumeration and nullable language-based voice lookup exist. | No runtime Japanese-voice/offline/quality evidence; do not assume voice availability. |
| `WidgetKit.framework/.../arm64e-apple-ios.swiftinterface` | `WidgetFamily` declares system Small/Medium/Large/ExtraLarge, `systemExtraLargePortrait` (iOS 27+), and accessory Circular/Rectangular/Inline on iOS. `accessoryCorner` is unavailable on iOS. | Declaration inventory only: no focused compile, per-device eligibility, gallery or actual layout verification. It does not resolve the owner's requested surfaces. |

Selected SDK root: `/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS27.2.sdk`. Version/SDK logs are in the initial evidence directory. Alpha's historical Xcode 27.0 limitations are not current Beta toolchain conclusions.

Apple's [WidgetKit foundations transcript](https://developer.apple.com/videos/play/wwdc2026/277/) describes multi-entry timelines, system update budgets and variable reload frequency. B-U-37 records the accepted distinction between a 15-minute content timeline target and guaranteed execution/display time. Candidate implementation: prepare offline entries in advance and replenish a bounded timeline, rather than require the extension to execute every 15 minutes. This is not a tested implementation.

Apple web pages for Core Text/Speech/synthesis returned JavaScript shells; Markdown fetches were unsupported by the web reader. Declaration claims above rely on local SDK evidence. Prototype compilation and runtime checks remain outstanding.

## Remaining questions and disposition

Resolved requirements are not repeatedly presented for approval. Rows marked PARTIAL contain specific unanswered details. Deferred practice questions do not block this content phase.

| ID | State and remaining question | Impact |
| --- | --- | --- |
| B-Q-01 | METHOD RESOLVED: independently author content while referencing topics/lessons/units. Item-level provenance/rights remain unverified. | Source inventory and release content review. |
| B-Q-02 | INVENTORY RESOLVED: six reference PDFs, Elementary I/II second edition, 1,451 pages, lessons 1–50 and Kanji units 1–50 with 536 indexed characters. Source findings and supplementary sections are recorded in the reference inventory. | Use the catalog for source bounds and milestone relationships; this does not certify release rights or JLPT item classification. |
| B-Q-03 | AUTHORING GATE RESOLVED by B-U-51: primary-agent self-review permits batch authoring; confirm concrete uncertainties with the owner. The owner initially volunteered to review, then delegated this gate. Independent human review and release quality are not claimed by self-review. | Continue authoring under the delegated gate; preserve item-level evidence and unresolved issues. |
| B-Q-04 | RESOLVED: 19 languages, English fallback, throughout features/content. | Translation coverage and RTL verification. |
| B-Q-05 | PARTIAL: Hiragana/Katakana included, displayed romaji excluded. Need detailed scope for combined/voiced sounds and pronunciation guidance. | Beginner content inventory. |
| B-Q-06 | PARTIAL: lesson contents/free access, both N5 and N4 in this phase, four main destinations and alphabet placement approved. The N4-placeholder requirement is retired. The source inventory records 50 lessons and 50 units; milestone links need not be one-to-one. | Information architecture is confirmed at destination level; detailed journeys/data inventory remain. |
| B-Q-07 | RESOLVED: default on, app-wide and persisted locally across relaunch. | Renderer consistency and preference integration. |
| B-Q-08 | RESOLVED: Kanji units, meaning/Han-Viet/On-Kun/compound/examples; no radicals/stroke count/order. | Source inventory is recorded; authored content review remains separate. |
| B-Q-09 | RESOLVED behavior: Apple Japanese TTS for words/examples/dialogues, offline, missing-voice guidance, one item at a time, stop/replacement/screen-departure/background behavior, no speed adjustment. Recording/recognition/scoring/AI remain DEFERRED. | Actual voice availability/pronunciation/offline/lifecycle evidence still required. |
| B-Q-10 | DEFERRED for practice audio/recordings. Current content playback follows B-U-47; do not add background playback, speed controls or a full audio-player scope. | Focused playback lifecycle verification. |
| B-Q-11 | DEFERRED: flashcards/SRS/error notebook/quizzes/typed-answer practice. | No scheduling or scoring engine now. |
| B-Q-12 | DEFERRED: JLPT mock examinations and question/answer banks. | Content phase does not claim examination readiness. |
| B-Q-13 | RESOLVED by B-U-58: persist a separate continuous learned prefix for each level. Mark/unmark affects only the selected level, using its own ordered lessons and preserving source numbering. N4 has no N5 learned-state prerequisite. No reading position, progress dashboard or scores. | Design level-scoped state and widget eligibility against explicit milestone lesson references. Mastery/exam readiness remains DEFERRED. |
| B-Q-14 | RESOLVED current scope: global + lesson search and all B-U-24 fields/types; favorites for all B-U-25 types and a separate review place. Notes are DEFERRED. Fine search matching/order and favorite ordering still need behavior specifications. | Search index, favorite identity and UI. |
| B-Q-15 | RESOLVED packaging: bundled content, offline operation and missing-voice fallback. Content-version compatibility and update integrity need engineering design against real PDFs. | No runtime content-server dependency or unapproved user import. |
| B-Q-16 | RESOLVED phase scope: local persistence, no cross-device online operation; backup/restore/export and multiple profiles DEFERRED. | Local favorites/learned/preferences ownership. |
| B-Q-17 | PARTIAL: purchases/subscriptions, ads and analytics DEFERRED. Age audience and release markets remain open release inputs. | No commercial/analytics dependencies in the current feature scope. |
| B-Q-18 | RESOLVED product behavior: Home/Lock Screen and applicable sizes, configurable vocabulary/sentence-pattern/Kanji, learned/favorites sources, unit milestone mapping for learned content, parent-favorite expansion with no learned restriction for favorites, random selection, target 15-minute timeline under system scheduling, adaptive fields/count, empty state and app-opening tap. Reminders remain DEFERRED. | Actual family/layout/timeline/snapshot evidence pending; no implied Siri/Shortcuts/Spotlight/Live Activity scope or detailed item routing. |
| B-Q-19 | PARTIAL: English official documents, Alpha-style source/review rules and ProjectBeta technical name approved. Final branding/bundle identifier/publisher remain open. | Scaffold and release identifiers. |
| B-Q-20 | RESOLVED: B-U-23 technical baseline. Exact storage schema/module boundaries still require design against confirmed features. | No need to reapprove the listed technologies. |
| B-Q-21 | PARTIAL: primary-agent editorial authority and the current batch scope are confirmed in B-U-51/52. Phase deadline, independent release-acceptance participants and physical/Duo device access remain open. | Authoring can proceed; unavailable release/device evidence remains explicit. |

## Investigation work

| ID | Work and reviewable output | Dependencies |
| --- | --- | --- |
| B-I-01 | INVENTORY COMPLETE: six PDFs, manifest/checksums and lesson/unit maps for both levels are recorded. Release-content rights remain a separate review item. Distinguish references from release materials. | See the reference inventory and B-Q-01/02. |
| B-I-02 | VI/EN DRAFT BATCH COMPLETE: 50 lessons and 50 Kanji units with traceable coverage and delegated primary self-review/cross-agent checks under B-U-51/54. The other 17 languages and independent human/release review remain outstanding. Reference OCR/extraction stays separate from release content. | See the content index and batch review. |
| B-I-03 | Design stable level/content identity/versioning, contextual reading/ruby segments, translations, unit milestones, favorite targets and separate per-level learned-prefix state for N5 and N4. No notes, mastery or quiz-score schema. | Both levels' authored data and approved learned/widget behavior, including B-U-58. |
| B-I-04 | Prototype ruby rendering with verified APIs; compile and test wrapping, punctuation, mixed scripts, Dynamic Type, VoiceOver and RTL. | Renderer requirements and UI/SDK skills. |
| B-I-05 | Verify Apple Japanese TTS offline, missing voices, contextual pronunciation, single-item replacement/stop, screen/background stopping, interruptions and route changes. No mic/Speech permission for playback-only functionality. | B-U-22/29/47 and reviewed readings. |
| B-I-06 | Specify open lesson reading, learned-prefix marking/unmarking, alphabet/Kanji browsing, search, favorites and audio journeys with empty/error states. Practice/assessment remains deferred. | Confirmed behavior, sample content and remaining search/favorite UX detail. |
| B-I-07 | Design atomic local favorite/learned/preference persistence and consistent content updates. Publish learned/favorite changes for widgets after successful persistence; reject stale derived widget state. Backup/export are deferred. | Stable identity/version design and B-U-35–46. |
| B-I-08 | Specify adaptive/native/Liquid Glass UI and full localization; preserve current selection/search across resize/pose changes, without adding rejected reading-position restoration. | Approved baseline and navigation. |
| B-I-09 | Configure governance/agent ownership and create a bounded scaffold with deterministic fixtures and targeted tests after requirements for that slice are clear. | Approved contracts, baselines, file leases. |
| B-I-10 | Define content-quality, behavioral, automated, adaptive/input/accessibility and performance/size evidence. Defer exam/speaking outcome acceptance to later phases. | Assigned criteria and resources. |
| B-I-11 | Implementable design for learned/favorites sources, milestone eligibility, parent-favorite expansion, random selection, target 15-minute timelines, localized ruby/meaning/adaptive fields, source-empty behavior and generic app opening. Verify snapshot consistency, extension embedding and selected families. | B-U-33/36–45, content identity, persistence and app entry contract. |
| B-I-12 | DEFERRED: refine local study reminder permissions/schedules/timezones/editing/cancellation/tap behavior after the other features. Later verification needs deterministic calendar/notification seams and actual permission/device cases. | Future reminder refinement; not a current delivery gate. |

The six-PDF source inventory and development-time editorial authoring artifacts now exist; see `docs/reference-inventory/` and `docs/content-authoring/`. The existing iOS tree is outside this content task’s verification. No application build, runtime, Duo, accessibility, learning-outcome, performance, size or release pass is claimed. Unavailable evidence remains explicit while authoring continues.

## Current editorial evidence

The Vietnamese/English batch contains 50 lesson drafts and 50 Kanji units with 536 character definitions. The content index, final structural checks, source coverage and bounded cross-agent review are maintained under [content authoring](content-authoring/README.md). All seven source notes are resolved under B-U-57: the owner confirmed applying the authored values and their recheck flags are closed. B-U-57 supersedes the earlier B-U-55/56 open-flag disposition. The original six PDFs are unchanged. The owner separately resolved the learned-prefix boundary under B-U-58: each level has independent state. Runtime schema design and independent human/release/device acceptance remain outstanding.
