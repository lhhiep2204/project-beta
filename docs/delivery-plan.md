# Delivery plan (generated)

Source: [owner HTML](index.html#roadmap). Edit its project-contract, never this export. P0 foundations and P1 delivery remain in the same N5+N4 product scope. The documentation gate applies before new development; task readiness also requires its own dependencies. Ready does not mean completed.

## DEV-PLAN-01: development user stories and E2E

Create development-phase tasks in the owner HTML as user stories, each testable end to end.

The current E2E index contains 47 tasks under T01–T07, each retaining its fixture, two scenarios and closure prerequisites.

- Deliver each story from user action through actual services/packages/state to native output. Technical work stays inside the story; unit tests or mocked UI alone cannot close it.
- Execution prerequisites remain on each task. Additional E2E prerequisites gate closure: content/translation preparation may start earlier, but done requires integrated surfaces and both passing scenarios. Validate the union dependency DAG.
- Fixtures specify development work, not already implemented tests. Pin package/content/review revisions and stable target IDs; reset a separate sandbox per case without changing source PDFs/identities/content for tests.
- Use XCUITest on the installed app/Simulator and native WidgetKit. Inject clock/random/failures only at boundaries, not a fully mocked repository/writer/selector. Physical audio behavior requires actual listening on suitable hardware; the owner has no physical iPhone, so keep missing cases explicit and do not ask again merely to close this plan.
- Record scenario ID, revision/build, OS/device/family, fixture/target IDs, steps, expected/actual and logs/xcresult/captures. Classify pass/fail/not_run/blocked; a screenshot/callback cannot prove listening.
- All new E2E plans start not_run. Preserve historical done scope/evidence without treating it as E2E acceptance or reopening H01/H02/H03/H04/T01.01/T04.01. T01–T05 verify integration of those foundations.
- T06/T07 remain separate system/performance/language/rights/release gates. Story passes do not authorize release or extend F01–F15.

## Documentation handoff — DOC-PLAN-03

Completed documentation is retained as product, design, content and engineering handoff material. Completed documentation tasks remain historical evidence and are no longer listed in the checklist or roadmap. T01.02 belongs to development; its in-progress status and unperformed E2E cases are preserved.

Documentation covers scope/requirements, flows/states, design, content/engineering contracts, task dependencies/acceptance, and synchronized final HTML. Translation production/review is development work by explicit owner instruction. Offline listening and real-audio verification are development work under DOC-PLAN-02, outside execution of the current documentation phase.

Development may proceed only when all DOC tasks and H00 are done, no product proposal or documentation finding is open, and synchronization/audit checks pass. Individual task dependencies still apply; ready does not mean done. T01.02 offline listening/audio checks do not block documentation completion and remain required development work.

Current documentation gate: ready for development.

Read: [acceptance.md](design-system/acceptance.md), [implementation-guide.md](design-system/implementation-guide.md), [engineering-contract.md](engineering-contract.md), [runtime-data-contract.md](runtime-data-contract.md).

## DOC-PLAN-04: current review and P1 execution

Completed P0 foundation groups are retained as handoff documentation and omitted from the execution roadmap. The completed former T01 proof is retained as a handoff; remaining development groups use the current IDs. P1 translation/audio work belongs to development, app/performance acceptance to acceptance, and sign-off to release. Track these in their owning tasks rather than duplicate them as current documentation issues. Preserve open finding status, dependencies and execution evidence; hiding a scheduled issue does not resolve it. P0/P1 are priorities, distinct from execution phases. Current task IDs follow DOC-PLAN-06; the completed native/audio group is no longer an execution task.

Foundation handoff: [docs/runtime-data-contract.md](runtime-data-contract.md), [source-reconciliation/ledger.md](content-authoring/source-reconciliation/ledger.md), [kana/README.md](content-authoring/kana/README.md), [sentence-bank/README.md](content-authoring/sentence-bank/README.md).

## DOC-PLAN-06: task ID migration

Remove completed T01 from the execution roadmap and retain its completed native/audio proof in docs/engineering-contract.md. Keep the remaining order and shift groups T02–T08 to T01–T07, with their story IDs following the new group numbers. Update active dependencies, E2E IDs, roadmap links and the migration crosswalk. Historical reports and evidence keep their original labels.

| Previous ID | Current ID |
| --- | --- |
| T01.01 | H01.01 |
| T01.02 | H01.02 |
| T01.03 | H01.03 |
| T01.04 | H01.04 |
| T02.01 | H02.01 |
| T02.02 | H02.02 |
| T02.03 | H02.03 |
| T02.04 | H02.04 |
| T03.01 | H03.01 |
| T03.02 | H03.02 |
| T03.03 | H03.03 |
| T04.01 | H04.01 |
| T04.02 | H04.02 |
| T04.03 | H04.03 |
| T06.01 | T01.01 |
| T06.02 | T01.02 |
| T06.03 | T01.03 |
| T06.04 | T01.04 |
| T06.05 | T01.05 |
| T06.06 | T01.06 |
| T06.07 | T01.07 |
| T06.08 | T01.08 |
| T06.09 | T01.09 |
| T06.10 | T01.10 |
| T06.11 | T01.11 |
| T06.12 | T01.12 |
| T07.01 | T02.01 |
| T07.02 | T02.02 |
| T07.03 | T02.03 |
| T07.04 | T02.04 |
| T07.05 | T02.05 |
| T08.01 | T03.01 |
| T08.02 | T03.02 |
| T08.03 | T03.03 |
| T08.04 | T03.04 |
| T08.05 | T03.05 |
| T09.01 | T04.01 |
| T09.02 | T04.02 |
| T09.03 | T04.03 |
| T09.04 | T04.04 |
| T09.05 | T04.05 |
| T09.06 | T04.06 |
| T09.07 | T04.07 |
| T09.08 | T04.08 |
| T09.09 | T04.09 |
| T09.10 | T04.10 |
| T09.11 | T04.11 |
| T09.12 | T04.12 |
| T09.13 | T04.13 |
| T09.14 | T04.14 |
| T09.15 | T04.15 |
| T09.16 | T04.16 |
| T09.17 | T04.17 |
| T09.18 | T04.18 |
| T09.19 | T04.19 |
| T10.01 | T05.01 |
| T10.02 | T05.02 |
| T10.03 | T05.03 |
| T10.04 | T05.04 |
| T10.05 | T05.05 |
| T10.06 | T05.06 |
| T10.07 | T05.07 |
| T11.01 | T06.01 |
| T11.02 | T06.02 |
| T11.03 | T06.03 |
| T11.04 | T06.04 |
| T12.01 | T07.01 |
| T12.02 | T07.02 |
| T12.03 | T07.03 |
| T12.04 | T07.04 |
| T00 | H00 |
| T01 | H01 |
| T02 | H02 |
| T03 | H03 |
| T04 | H04 |
| T06 | T01 |
| T07 | T02 |
| T08 | T03 |
| T09 | T04 |
| T10 | T05 |
| T11 | T06 |
| T12 | T07 |

Active group renumbering (previous current roadmap → current):
| Previous group | Current group |
| --- | --- |
| T02 | T01 |
| T03 | T02 |
| T04 | T03 |
| T05 | T04 |
| T06 | T05 |
| T07 | T06 |
| T08 | T07 |

Retired IDs from the previous current roadmap:
- T01: [engineering-contract.md](engineering-contract.md)
- T01.01: [engineering-contract.md](engineering-contract.md)
- T01.02: [engineering-contract.md](engineering-contract.md)

Earlier retired IDs:
- T05: [engineering-contract.md](engineering-contract.md)
- T05.01: [engineering-contract.md](engineering-contract.md)
- T05.02: [engineering-contract.md](engineering-contract.md)


## PLAN-02: owner-approved decomposition (2026-11-09)

Decompose the entire roadmap, including content, localization and acceptance, into feature/screen groups, independently acceptable behavior tasks and internal technical checklists. T01 was being executed when the owner requested this change; preserve that delivery. DOC-PLAN-06 later retires that completed group and renumbers the remaining groups.

The execution roadmap keeps its order. Under DOC-PLAN-06, the completed native/audio proof moves to the engineering handoff; remaining groups now use T01–T07. Dependencies and historical evidence remain traceable.

- Execute child tasks; never assign the same work simultaneously through its parent and children. Keep one integration owner and do not automatically spawn agents.
- Parent dependencies remain roadmap traceability. Child dependencies are the execution prerequisites. A dependency on a parent requires evidenced closure of that entire group.
- Preserve H01 status, output, acceptance and existing evidence. H01.01–04 are inherited coverage views, not new execution assignments.
- ready: dependencies complete; todo: unstarted/not confirmed ready; in_progress: executing; blocked: specific impediment; done: criteria met with evidence. Checklists or browser simulations alone cannot establish native completion.
- Children inherit parent role and priority. Do not invent individual assignments, estimates or completion percentages. Record evidence revision/scope and ask the owner for new product decisions.
- Content and locale batches require item-level coverage ledgers. Do not duplicate identical reader UI tasks for 50 lessons. Keep a shared behavior together even when it spans screens.
- Close a group only after every child and group integration acceptance pass. Reconcile status conflicts against evidence without resetting existing work.

## Group and task index

| Group | Scope | Recorded status | Children |
| --- | --- | --- | --- |
| [T01](index.html#T01) | Lessons, level selection and Settings | todo | [T01.01](index.html#T01.01), [T01.02](index.html#T01.02), [T01.03](index.html#T01.03), [T01.04](index.html#T01.04), [T01.05](index.html#T01.05), [T01.06](index.html#T01.06), [T01.07](index.html#T01.07), [T01.08](index.html#T01.08), [T01.09](index.html#T01.09), [T01.10](index.html#T01.10), [T01.11](index.html#T01.11), [T01.12](index.html#T01.12) |
| [T02](index.html#T02) | Corpus search and favorites | todo | [T02.01](index.html#T02.01), [T02.02](index.html#T02.02), [T02.03](index.html#T02.03), [T02.04](index.html#T02.04), [T02.05](index.html#T02.05) |
| [T03](index.html#T03) | Kanji, kana and learned-aware examples | todo | [T03.01](index.html#T03.01), [T03.02](index.html#T03.02), [T03.03](index.html#T03.03), [T03.04](index.html#T03.04), [T03.05](index.html#T03.05) |
| [T04](index.html#T04) | Remaining localization | in_progress | [T04.01](index.html#T04.01), [T04.02](index.html#T04.02), [T04.03](index.html#T04.03), [T04.04](index.html#T04.04), [T04.05](index.html#T04.05), [T04.06](index.html#T04.06), [T04.07](index.html#T04.07), [T04.08](index.html#T04.08), [T04.09](index.html#T04.09), [T04.10](index.html#T04.10), [T04.11](index.html#T04.11), [T04.12](index.html#T04.12), [T04.13](index.html#T04.13), [T04.14](index.html#T04.14), [T04.15](index.html#T04.15), [T04.16](index.html#T04.16), [T04.17](index.html#T04.17), [T04.18](index.html#T04.18), [T04.19](index.html#T04.19) |
| [T05](index.html#T05) | Widget extension | todo | [T05.01](index.html#T05.01), [T05.02](index.html#T05.02), [T05.03](index.html#T05.03), [T05.04](index.html#T05.04), [T05.05](index.html#T05.05), [T05.06](index.html#T05.06), [T05.07](index.html#T05.07) |
| [T06](index.html#T06) | UX and performance acceptance | todo | [T06.01](index.html#T06.01), [T06.02](index.html#T06.02), [T06.03](index.html#T06.03), [T06.04](index.html#T06.04) |
| [T07](index.html#T07) | Content and release acceptance | todo | [T07.01](index.html#T07.01), [T07.02](index.html#T07.02), [T07.03](index.html#T07.03), [T07.04](index.html#T07.04) |

## T01 / P1 / todo: Lessons, level selection and Settings
Phase: development. Owner role: iOS. Parent dependency traceability: H01.
Existing integration output: Entry, continuous lesson, persisted state, furigana and playback.
Existing integration acceptance: Relaunch retains approved state only; range confirmation and failed writes behave correctly.

### T01.01 / todo: Implement the main navigation shell

Need: Learners need to move between the four areas on iPhone and iPad.
Type: native. Role: iOS. Priority: P1.
Output: Compact tabs; a two-column sidebar–detail NavigationSplitView at sufficient width, with logical-screen routes (DS-U-50).
Execution dependencies: H01.
Feature contracts: F01, F13.
Read: [implementation-guide.md](design-system/implementation-guide.md).

Acceptance:

- At sufficient width show only sidebar and detail; top-level navigation and lesson/unit lists share the sidebar. Never add a middle content column. Resizing retains route/query without creating a new playback owner.
- Relaunch opens Lessons at the saved level without restoring a reader/scroll position.

Implementation / handoff checklist:

- Compose services and scene routes.
- Verify four-area switching, compact/wide/ample widths, large text, resize/rotation and relaunch; no third column appears.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to switch among four areas on iPhone/iPad so I keep context when the window changes.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Native app with a valid draft package, saved N4 level, compact iPhone and wide iPad.

#### T01.01-E2E-01 / happy

Given: The app is terminated with N4 saved.
When: Launch, visit Lessons/Kanji/Favorites/Settings and return to Lessons.
Then: Launch opens N4 Lessons; all four areas have native states and correct routes.

#### T01.01-E2E-02 / edge

Given: Kanji or Settings is selected in compact layout with its destination route recorded.
When: Resize/rotate compact ↔ wide, switch destinations, terminate and relaunch.
Then: Resizing retains the selected destination with exactly sidebar–detail columns at width; relaunch opens N4 Lessons.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.02 / todo: Choose N5/N4 on first launch

Need: As a learner, I want to choose a level to start in the appropriate lesson list.
Type: native. Role: iOS. Priority: P1.
Output: Level selection screen to persistence to Lessons.
Execution dependencies: T01.01.
Feature contracts: F01, F11.
Read: [entry-and-learning-state.md](design-system/entry-and-learning-state.md).

Acceptance:

- Do not preselect N5; N4 has no learned-N5 prerequisite.
- Leave only after successful save; failure retains selection with retry; relaunch remembers the level.

Implementation / handoff checklist:

- Connect selection to the existing H01 writer.
- Verify fresh install, save failure, retry and relaunch.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a new learner, I want to choose N5 or N4 so I start at my level without a prerequisite lock.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Two empty state sandboxes; one save failure at the real writer through a test seam.

#### T01.02-E2E-01 / happy

Given: First launch has no preference.
When: Choose N4, save, terminate and relaunch; repeat with N5 in a separate sandbox.
Then: Nothing is preselected; N4 opens 26–50 with no N5 learning; relaunch skips selection and remembers the choice.

#### T01.02-E2E-02 / edge

Given: The first save fails after choosing N4.
When: Confirm, then Retry.
Then: Failure retains the screen and selection without navigation/publication; only successful retry opens Lessons.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.03 / todo: Switch the shared Lessons/Kanji level

Need: Learners need to switch N5/N4 without changing learned lessons.
Type: native. Role: iOS. Priority: P1.
Output: Lessons/Kanji level switch and shared Settings binding.
Execution dependencies: T01.02.
Feature contracts: F01, F03, F11.
Read: [entry-and-learning-state.md](design-system/entry-and-learning-state.md), [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Both areas use the same committed preference and preserve source numbering.
- Switching never mutates either learned prefix; failures preserve the saved level.

Implementation / handoff checklist:

- Use one shared level action/binding.
- Verify switching from each entry point and write failures.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want one shared level so Lessons and Kanji use the saved selection.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T03.01.
Fixture: N5 learned 1–3, N4 learned 26–27, selected N5; save-failure seam.

#### T01.03-E2E-01 / happy

Given: Lessons shows N5.
When: Switch to N4, open Kanji and relaunch.
Then: Both areas use N4; both prefixes and source numbering remain intact.

#### T01.03-E2E-02 / edge

Given: N4 is saved and the next switch to N5 will fail.
When: Change level, visit the other area and Retry.
Then: Both remain N4 before successful retry and switch to N5 together after commit.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.04 / todo: Implement the level-specific lesson list

Need: Learners need to browse and open every lesson in the selected level.
Type: native. Role: iOS. Priority: P1.
Output: Metadata list, learned indicators and alphabet entry.
Execution dependencies: T01.03.
Feature contracts: F01, F03, F07, F14.
Read: [entry-and-learning-state.md](design-system/entry-and-learning-state.md), [implementation-guide.md](design-system/implementation-guide.md).

Acceptance:

- N5 1–25/N4 26–50 are all open; indicators reflect committed prefixes.
- Provide scoped loading/error states; do not decode the whole curriculum to build the list.

Implementation / handoff checklist:

- Read metadata and route by ID.
- Verify lesson inventory, indicators and package-unavailable states.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to browse and open every lesson in my level so I can choose what to study.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Full 50-lesson manifest; endpoints N5=3/N4=27; manifest failure and retry.

#### T01.04-E2E-01 / happy

Given: The list has loaded from the offline package.
When: Browse N5 1–25 and N4 26–50 and select the first/last lesson in each.
Then: Order, learned state and route IDs match; unlearned lessons remain accessible.

#### T01.04-E2E-02 / edge

Given: The manifest is delayed or fails to load.
When: Open the list, cause failure and Retry.
Then: Scoped loading/error replaces false emptiness; retry restores the list.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.05 / todo: Implement the continuous lesson reader and section jump

Need: Learners need to read the complete lesson and jump to a section.
Type: native. Role: iOS. Priority: P1.
Output: Reader for lessons 1/26 first, ordered topic to vocabulary to grammar to patterns/examples to dialogue.
Execution dependencies: T01.04.
Feature contracts: F02, F05.
Read: [screens-and-playback.md](design-system/screens-and-playback.md), [implementation-guide.md](design-system/implementation-guide.md).

Acceptance:

- No mutually exclusive content tabs; all content stays reachable under lazy rendering.
- Jump materializes unrendered targets; each form retains its own meaning/reading.

Implementation / handoff checklist:

- Render shards with stable IDs and section anchors.
- Verify both representative lessons, long content and offscreen jumps.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want one continuous lesson with section jumps so I can reach the material I need.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Complete lessons 1 and 26; final section not yet materialized; one checksum-invalid detail shard.

#### T01.05-E2E-01 / happy

Given: Open lesson 1 or 26 offline.
When: Read from the start, jump to the final dialogue and return to vocabulary.
Then: One document contains topic/vocabulary/grammar/patterns/examples/dialogue; jumps resolve exact IDs before rendering, preserving per-form meaning/readings.

#### T01.05-E2E-02 / edge

Given: The selected lesson shard fails while other lessons remain valid.
When: Open the failed lesson, restore the fixture and Retry, then open another lesson.
Then: Only that detail is unavailable; retry preserves the target and other lessons still open without substituted content.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.06 / todo: Mark/unmark learned lessons with range confirmation

Need: Learners need manual learned marking with the exact affected lessons explained.
Type: native. Role: iOS. Priority: P1.
Output: Lesson-header action, range confirmation and success/failure/retry.
Execution dependencies: T01.05.
Feature contracts: F03.
Read: [entry-and-learning-state.md](design-system/entry-and-learning-state.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- A single change saves immediately; multiple changes confirm the exact range; N5/N4 are independent.
- Cancel/failure preserves the snapshot; revision changes require recomputation and reconfirmation; publish after commit.

Implementation / handoff checklist:

- Connect range planning/writer and list indicators.
- Exercise N5 6/5, N4 30/28, stale confirmation and save failure.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want explicit learned-range changes so I can manage both levels independently.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: N5=3/N4=30; another scene changes the revision; one save failure.

#### T01.06-E2E-01 / happy

Given: N5 learned 1–3 and N4 26–30.
When: Mark N5 lesson 6, confirm 4–6, unmark N4 lesson 28, confirm 28–30 and relaunch.
Then: Persist N5=6/N4=27; a single-lesson change saves immediately; list and reader agree after commit.

#### T01.06-E2E-02 / edge

Given: The range dialog is open at revision R.
When: Cancel; repeat with a save failure; repeat after another scene changes the prefix before Confirm.
Then: Cancel/failure retains state with retry; a new revision recomputes the changed range and requires confirmation again without a silent write.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.07 / todo: Play lesson words, examples and dialogues

Need: Learners need item or full-dialogue playback and an explicit stop.
Type: native. Role: iOS. Priority: P1.
Output: Item speakers, full-dialogue/turn playback, highlight and toolbar stop.
Execution dependencies: T01.05.
Feature contracts: F04, F05.
Read: [screens-and-playback.md](design-system/screens-and-playback.md).

Acceptance:

- Highlight only the active turn without auto-scroll; speaker taps always restart.
- Leaving the logical reader stops playback; geometry/furigana changes do not; each visible form has its correctly scoped speech action, and a bound form with missing context remains readable with pronunciation unavailable.

Implementation / handoff checklist:

- Bind controls to the coordinator and speech IDs.
- Verify request replacement, stop, missing voice and full-dialogue/solo-turn behavior.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to hear the selected form, sentence or turn so speech matches what I read.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T01.11.
Fixture: Lessons 1/26, multiple forms in one entry and bound forms with/without context; system Japanese voice.

#### T01.07-E2E-01 / happy

Given: The native reader is open with revision-matched speech data.
When: Tap each form/sentence speaker, play the full dialogue, choose one turn and Stop.
Then: Speech uses the exact form target, full dialogue follows the fixed script, only the active turn highlights, restart/Stop work and no auto-scroll occurs.

#### T01.07-E2E-02 / edge

Given: One bound form lacks context and an old request is superseded.
When: Tap that bound form, play another item, rotate/toggle furigana and leave the logical reader.
Then: The form stays readable with scoped unavailable speech and no marker spoken; stale callbacks do not revive it; geometry/toggle retains playback, departure stops it.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.08 / todo: Implement Settings and its level control

Need: Learners need learning and appearance preferences in one place.
Type: native. Role: iOS. Priority: P1.
Output: Native grouped Settings for level/language/furigana and appearance.
Execution dependencies: T01.03.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Level uses the same action as Lessons/Kanji; controls use saved state.
- No custom font-size or out-of-scope controls; failed saves cannot report success.

Implementation / handoff checklist:

- Build Settings groups and preference bindings.
- Verify level actions, failure states and native layout.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want preferences in Settings so I can find the approved controls.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: App with default committed preferences and a save-failure seam.

#### T01.08-E2E-01 / happy

Given: Initial level selection is complete.
When: Open Settings, inspect learning/appearance groups, change level and return to Lessons.
Then: Approved level/language/furigana/appearance controls reflect committed state and use the shared level action.

#### T01.08-E2E-02 / edge

Given: A preference save will fail.
When: Change level in Settings, leave/return and Retry.
Then: No success precedes commit; old state remains and retry is available, without a separate font-size or out-of-scope control.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.09 / todo: Change the shared UI/content language

Need: Learners need one choice for both interface and translated learning content.
Type: native. Role: iOS. Priority: P1.
Output: System plus 19-locale picker and resolution/fallback.
Execution dependencies: T01.08, T04.01.
Feature contracts: F06, F11.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Default to System; Japanese is not a UI locale; missing translations use labeled English fallback.
- Language changes retain IDs/visible examples; Sino-Vietnamese displays only for resolved Vietnamese.

Implementation / handoff checklist:

- Connect locale resolution, resource lookup and writer.
- Verify System, fallback, write failure and stable example IDs; fallback does not certify translation completion.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want one language preference so the interface and translated learning content agree.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T03.03.
Fixture: VI/EN, sparse ar/he sidecars for fallback tests only, pinned target/candidate IDs, supported/unsupported System locale.

#### T01.09-E2E-01 / happy

Given: Reader and Settings share one committed snapshot.
When: Change VI → EN → System, revisit the same item/sentence and open Kanji.
Then: UI/meanings share the resolved locale, IDs/sentences remain stable, and Sino-Vietnamese appears only for resolved VI.

#### T01.09-E2E-02 / edge

Given: A locale fixture lacks one translated field or System is unsupported.
When: Select that locale, open the missing field and attempt a language change with save failure.
Then: A missing field falls back to labelled English without counting as translated; unsupported System resolves EN; failed save keeps the committed locale and Japanese stays LTR.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.10 / todo: Change System/Light/Dark appearance

Need: Learners need a preferred appearance retained across app launches.
Type: native. Role: iOS. Priority: P1.
Output: Appearance picker, semantic theme and preference persistence.
Execution dependencies: T01.08.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Default to System; Light/Dark use approved tokens across app screens.
- Save failure retains committed choice; relaunch restores it without overriding system widget rendering.

Implementation / handoff checklist:

- Bind theme to the committed preference.
- Verify all three modes, system-theme changes and relaunch.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want System/Light/Dark so my appearance preference survives relaunch.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: System Light/Dark modes, app default System and a save-failure seam.

#### T01.10-E2E-01 / happy

Given: The app uses System.
When: Change system theme, select app Light then Dark and relaunch for each choice.
Then: System follows the OS; explicit choices persist with approved tokens across the four areas.

#### T01.10-E2E-02 / edge

Given: Dark is saved and changing to Light will fail.
When: Choose Light, Retry and relaunch.
Then: Failure retains Dark; success applies Light; widgets still follow system rendering mode.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.11 / todo: Toggle shared furigana

Need: Learners need one furigana preference from either the reader or Settings.
Type: native. Role: iOS. Priority: P1.
Output: Settings toggle and reader toolbar sharing state.
Execution dependencies: T01.05, T01.08.
Feature contracts: F05, F11, F12.
Read: [settings-and-localization.md](design-system/settings-and-localization.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Default on; persist across relaunch; reader and Settings share committed state.
- Do not alter pronunciation or visible examples; widgets receive the preference through post-save publication.

Implementation / handoff checklist:

- Use the shared writer and renderer binding.
- Verify both entry points, save failure and active playback.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to toggle furigana in the reader or Settings so I have one shared choice.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Furigana on by default; recorded visible/playing sentence IDs; save-failure seam.

#### T01.11-E2E-01 / happy

Given: The reader shows a sentence with ruby.
When: Disable from the toolbar, open Settings, enable again and relaunch.
Then: Both controls agree after commit; ruby changes app-wide and persists while candidate/speech targets stay unchanged.

#### T01.11-E2E-02 / edge

Given: Furigana is enabled and saving disabled will fail.
When: Disable while speech plays and Retry.
Then: Failure retains committed ruby/state without publication; toggle does not stop/change the speech target; retry applies it.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T01.12 / todo: Open all 50 N5/N4 lessons through the shared reader

Need: Learners need the same experience throughout both levels.
Type: native. Role: iOS. Priority: P1.
Output: Full-corpus integration and reachable lesson/section/target report.
Execution dependencies: T01.06, T01.07, T01.09, T01.10, T01.11, H02, H04.
Feature contracts: F01, F02, F14.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- All 50 lessons use canonical data; lessons 1/26 fixtures do not limit product scope.
- No integration-broken targets; unapproved content/translations remain separate gates.

Implementation / handoff checklist:

- Build an updated development package and integrate the full corpus.
- Check screen/target coverage and distinguish data defects from UI defects.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want the reader to support all 50 lessons offline so I can study N5 and N4.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T02.04, T03.05.
Fixture: Package from all 50 lesson JSON files plus revision-matched H04 speech/candidates; per-lesson/target ledger.

#### T01.12-E2E-01 / happy

Given: The installed build has the full package and networking disabled.
When: Open all lessons 1–50 from the list, jump every section, inspect forms/sentences, play representative targets and relaunch.
Then: The ledger covers 50/50 with IDs/counts matched to the package; reader scope exceeds fixtures 1/26 and learned/favorite/preferences persist.

#### T01.12-E2E-02 / edge

Given: A separate test package omits a shard/speech/candidate.
When: Open the failing target, open another valid lesson and Retry.
Then: Unavailable stays scoped without crash/substitution; incomplete ledger never counts as a full-corpus pass.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

## T02 / P1 / todo: Corpus search and favorites
Phase: development. Owner role: iOS + Data. Parent dependency traceability: H02, T01.
Existing integration output: Complete offline index, scope/filter support and target navigation.
Existing integration acceptance: Debounce/IME/normalization/ranking and direct parent/child semantics verified.

### T02.01 / todo: Implement offline normalized and ranked queries

Need: Learners need relevant matches by Japanese, reading or meaning.
Type: technical. Role: iOS + Data. Priority: P1.
Output: Query service over the prebuilt index with locale fallback and grouping/ranking. Include a minimal native global search entry using the real index for query-to-result E2E; T02.02 completes session lifecycle.
Execution dependencies: H01, H02, T01.01.
Feature contracts: F09, F14.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Exact to prefix to contains to order/ID; normalize case/Vietnamese accents/equivalent kana while preserving voiced distinctions.
- Cover approved corpus/fields; index failure is unavailable, never zero results.

Implementation / handoff checklist:

- Connect SQLite queries, scope and requested-language fields.
- Test ranking, fallback and malformed/unavailable indexes.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: none; completion not established.

User story: As a learner, I want offline lookup by Japanese, reading or meaning so I can find the correct item.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Full package/index; pinned query → expected ID/group/order corpus including Vietnamese accents, case, kana, voicing, romaji and Sino-Vietnamese.

#### T02.01-E2E-01 / happy

Given: Open the native global search entry with networking disabled.
When: Enter each ledger query and inspect results.
Then: IDs/order follow exact → prefix → contains then order/ID within groups; approved fields/locales work with original display/ruby and preserved voicing distinctions.

#### T02.01-E2E-02 / edge

Given: The index is missing or has an invalid checksum/version.
When: Search a known nonempty query, restore the fixture and Retry.
Then: Show unavailable/retry rather than zero results; recovery returns package-matched IDs.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T02.02 / todo: Implement global search

Need: Learners need one screen to search across content types.
Type: native. Role: iOS + Data. Priority: P1.
Output: Search input, grouped results and loading/empty/error states.
Execution dependencies: T02.01, T01.01.
Feature contracts: F09.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Debounce 500 ms after committed input; ignore marked IME text; clear cancels immediately.
- Request tokens suppress stale results; retain approved groups and error context.

Implementation / handoff checklist:

- Connect session/query tokens and grouped UI.
- Exercise IME, clear, fast typing and out-of-order completions.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want results for my latest input so I do not select stale results.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Japanese IME; scheduler/request seams at native adapters; slow query A, fast B and one failed request.

#### T02.02-E2E-01 / happy

Given: Global search is open.
When: Compose with IME, commit, wait for debounce, change A → B quickly and resize/rotate the search screen.
Then: No marked-text query; search starts after 500 ms from final commit; only B publishes and groups/query remain correct. Resize retains query/scope without reviving an old request.

#### T02.02-E2E-02 / edge

Given: A remains in flight and B may fail.
When: Clear immediately, then search failing B and Retry.
Then: Clear immediately cancels into unqueried; A cannot revive results; failure keeps query/retry without false no-results.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T02.03 / todo: Search within a lesson and navigate to exact results

Need: Learners need scoped lesson search and return navigation without retyping.
Type: native. Role: iOS + Data. Priority: P1.
Output: Lesson scope, target routing and search-session preservation on Back.
Execution dependencies: T02.02, T01.05, T03.05.
Feature contracts: F02, F08, F09.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md), [implementation-guide.md](design-system/implementation-guide.md).

Acceptance:

- Results open exact unrendered items/sections; a selected example uses one of at most three slots.
- Back retains query/scope; Close/relaunch ends the session; unavailable targets retain context.

Implementation / handoff checklist:

- Connect stable target routes and lazy materialization.
- Verify each result group, Back/Close and example slot cap.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want results to open their exact location and return to search so I can keep looking.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Global/scoped queries with a lazy final-section target, a candidate outside the normal top three and an unresolved target.

#### T02.03-E2E-01 / happy

Given: Search globally or within a lesson.
When: Select a final-section result or out-of-top-three sentence and go Back.
Then: Navigate to the exact stable ID/section; the selected sentence occupies one of three slots; Back preserves query/scope/results.

#### T02.03-E2E-02 / edge

Given: One result targets an unresolved fixture entity.
When: Select it, return, Close/reopen search and relaunch.
Then: Failure retains context without substitution; Close/relaunch ends the session.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T02.04 / todo: Save/remove exact favorites through context menus

Need: Learners need to save an exact item or an entire lesson/unit.
Type: native. Role: iOS + Data. Priority: P1.
Output: Native context menus and direct favorite writes.
Execution dependencies: T01.05, H01.
Feature contracts: F10.
Read: [entry-and-learning-state.md](design-system/entry-and-learning-state.md), [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Support approved targets; no favorite types for examples/turns/kana.
- Success follows commit; failure preserves state with retry; removing a parent retains independently saved children.

Implementation / handoff checklist:

- Bind menus by target type/ID to the committed writer.
- Verify save/remove, parent/child and secondary-click behavior where supported.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to save an item or lesson/unit so I can retrieve it without automatically saving children.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T03.02.
Fixture: Seven approved favorite kinds; separately saved parent/child and one failed save.

#### T02.04-E2E-01 / happy

Given: Native reader/unit has a valid target.
When: Hold the exact surface, save parent and child separately, remove parent and relaunch.
Then: The menu uses the exact target; independently saved child remains; no example/turn/kana favorite type appears.

#### T02.04-E2E-02 / edge

Given: The writer rejects the next Save or Remove.
When: Perform the action, inspect feedback and Retry.
Then: No success precedes commit; failure retains favorites; retry persists exactly one identity.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T02.05 / todo: Implement the favorites list, filters and navigation

Need: Learners need to browse, filter and reopen saved items.
Type: native. Role: iOS + Data. Priority: P1.
Output: Direct-favorites list, type/level filters, empty/error and target navigation.
Execution dependencies: T02.04, T02.03.
Feature contracts: F10.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Default to all types, newest first; equal timestamps sort by ID; parents remain one row.
- Open the exact target and retain filters on Back; removed/unresolvable targets remain unavailable favorites with their old IDs and an explicit remove action; never silently delete or redirect them.

Implementation / handoff checklist:

- Connect bounded target resolution and filters.
- Try empty list, parent/child, ordering, unavailable saved targets, explicit removal and retry.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want to filter and reopen saved items so I can resume at the correct target.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Seven direct favorite kinds across N5/N4, tied timestamps, parent/child and a removed test-package target.

#### T02.05-E2E-01 / happy

Given: The list contains multiple saved kinds.
When: Open Favorites, filter type/level, open an item, go Back, remove and re-add it.
Then: Default is all/newest, ties use IDs, parents occupy one row, targets open exactly, Back retains filters and re-add has a new commit time.

#### T02.05-E2E-02 / edge

Given: One old favorite is unresolved and one removal will fail.
When: Open the unavailable row, fail removal, Retry and relaunch.
Then: Retain old ID/time with explicit removal; never auto-delete/redirect; failure retains the row until successful retry.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

## T03 / P1 / todo: Kanji, kana and learned-aware examples
Phase: development. Owner role: iOS. Parent dependency traceability: H03, H04, T01.
Existing integration output: Unit/grid/detail/alphabet screens and deterministic candidate selection.
Existing integration acceptance: Cross-level milestones, cap three, fixed dialogue and visible-candidate stability.

### T03.01 / todo: Implement the level-specific Kanji unit list

Need: Learners need to choose a Kanji unit in the current level.
Type: native. Role: iOS. Priority: P1.
Output: Unit metadata list with shared level and stable routes.
Execution dependencies: T01.02, H02.04.
Feature contracts: F06.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Lists follow source level; widget milestones do not relabel units.
- Scoped loading/error; no separate learned-Kanji state.

Implementation / handoff checklist:

- Connect unit metadata and navigation.
- Verify both levels and units 21–25.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want Kanji units grouped by source level so I can choose the unit I need.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: 50 units with separate source level/milestone; units 21–25 mandatory; manifest failure.

#### T03.01-E2E-01 / happy

Given: N4 is the saved level.
When: Open Kanji and browse/select N4 units; repeat in a separate sandbox initialized with N5.
Then: List/routes follow source level; units 21–25 are not relabelled by their N5 milestone; no independent learned-Kanji state exists.

#### T03.01-E2E-02 / edge

Given: The unit manifest fails or is loading.
When: Open Kanji and Retry after fixture recovery.
Then: Scoped loading/error avoids false emptiness and retry returns the correct unit IDs.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T03.02 / todo: Implement the unit screen and character grid

Need: Learners need to view a unit grid and choose a character.
Type: native. Role: iOS. Priority: P1.
Output: Unit character grid/content with target context menus and detail routes.
Execution dependencies: T03.01.
Feature contracts: F06, F13.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Correct master IDs/word links; open the exact character and retain the unit on Back.
- Grid reflows for width/text size; no radicals/stroke count/stroke-order additions.

Implementation / handoff checklist:

- Render the metadata grid and resolve detail by ID.
- Verify large-text layout and routing.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want a unit character grid so I can open the correct Kanji detail.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: Units 1/21/26 with packaged master character IDs; compact/wide/large text.

#### T03.02-E2E-01 / happy

Given: Open a unit offline.
When: Select characters, go Back, resize/rotate and change system text size.
Then: Master IDs/word links match; Back retains the unit; grid reflows with width/text size without losing selection.

#### T03.02-E2E-02 / edge

Given: One master link is unresolved in the test package.
When: Select it, go Back and select a valid character.
Then: Only that target is unavailable; the unit remains usable without substitution or added radical/stroke content.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T03.03 / todo: Implement Kanji character detail

Need: Learners need meanings, On/Kun, compounds and matching sentences for the selected character.
Type: native. Role: iOS. Priority: P1.
Output: Character detail, contextual speech, favorites and learned-aware examples.
Execution dependencies: T03.02, T03.05, T01.07, T04.01.
Feature contracts: F04, F06, F08.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Do not choose an arbitrary standalone character reading; provide separate stop while pending/playing.
- Sino-Vietnamese displays only in Vietnamese; ruby/audio/translation retain matching target IDs.

Implementation / handoff checklist:

- Connect masters/compounds/examples and playback coordinator.
- Verify locale, missing voice, Back and stop lifecycle.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want meanings, On/Kun, words and contextual sentences so I understand the selected Kanji.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: 536 master IDs; 日 with per-word readings; VI/EN and an invalid bound context.

#### T03.03-E2E-01 / happy

Given: Open a character from a unit with VI selected.
When: Inspect fields/words/sentences, play a context, go Back/reopen; repeat with a separate EN-initialized sandbox.
Then: ID/meaning/ruby/speech align, Sino-Vietnamese is VI-only, examples cap at three and bare Kanji has no invented default pronunciation.

#### T03.03-E2E-02 / edge

Given: One word speech context is missing or digest-invalid.
When: Tap that speaker, play a valid target, Stop and leave.
Then: Text remains with scoped unavailable speech and no substituted On/Kun; Stop works pending/playing and departure stops playback.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T03.04 / todo: Implement alphabet tables and cell playback

Need: Learners need alphabet lookup and valid isolated/contextual speech.
Type: native. Role: iOS. Priority: P1.
Output: Lessons entry, modern/extended/special/reference groups and selected-cell detail.
Execution dependencies: H03, T01.04.
Feature contracts: F04, F07.
Read: [kanji-alphabets-search-favorites.md](design-system/kanji-alphabets-search-favorites.md).

Acceptance:

- Render the complete authored inventory with separate rare/reference groups.
- Basic examples ignore learned prefixes; dependent marks are not spoken alone; provide separate stop.

Implementation / handoff checklist:

- Connect kana inventory and reviewed speech contexts.
- Verify groups/cells, special-mark contexts and layout changes.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a beginner, I want complete kana tables with contextual playback so I can learn sounds and usage.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: none.
Fixture: 301-entry inventory with 29 references; basic/voiced/combined/extended/special groups, dependent marks and none/N4-only learned states.

#### T03.04-E2E-01 / happy

Given: Lessons provides the alphabet entry and the app is offline.
When: Open Hiragana/Katakana groups/reference, select cells/speakers, change learned state and reopen.
Then: The ledger covers all 301 entries in correct groups; basic examples ignore prefixes, no romaji displays, context/translation align.

#### T03.04-E2E-02 / edge

Given: Select a dependent mark and a target missing voice/context.
When: Play the reviewed context, attempt the failed target, Retry/Stop and go Back.
Then: No invented isolated mark sound; scoped failure retains content, Stop remains available and Back stops audio.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T03.05 / todo: Select up to three examples from independent learned prefixes

Need: Learners need familiar examples that do not change unexpectedly during reading.
Type: technical. Role: iOS. Priority: P1.
Output: Shared deterministic selector and scene-visible candidate snapshot.
Execution dependencies: H04, T01.06.
Feature contracts: F03, F08.
Read: [example-selection.md](design-system/example-selection.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Rank unfamiliar grammar then vocabulary then simplicity/length then order/ID; fallback still matches the target.
- Total cap three without expansion; preserve visible/playing candidates, fixed dialogues and the kana basic rule.

Implementation / handoff checklist:

- Build the shared selector from explicit dependency IDs.
- Test none/N5/N4/both, target exceptions, fallback and stable visible snapshots.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: none; completion not established.

User story: As a learner, I want at most three examples matching saved knowledge so examples remain understandable and stable.

E2E status: not_run. Surface: app.
Additional E2E closure prerequisites: T01.07.
Fixture: Revision-matched H04 bank/oracle; targets for grammar/word exceptions, fallback, dedup and two 一日 readings; none/N5-only/N4-only/both states.

#### T03.05-E2E-01 / happy

Given: The reader uses the native selector with the actual candidate package.
When: Open the target in all four learned states against the oracle, change prefixes with the page open and reopen.
Then: Order/cap/dedup match, N4 does not imply N5, fallback matches the target, visible/playing IDs persist until reopening and dialogue stays fixed.

#### T03.05-E2E-02 / edge

Given: A prefix change is cancelled/fails to save and another target has a missing/corrupt bank.
When: Reopen the target, open the invalid-bank target and Retry.
Then: Uncommitted prefixes are unused; invalid targets show scoped unavailable without padding/expansion or unrelated sentences.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

## T04 / P1 / in_progress: Remaining localization
Phase: development. Owner role: Localization. Parent dependency traceability: H02, H03, H04.
Existing integration output: Content and UI resources for all 19 languages.
Existing integration acceptance: Coverage, reviewed translation, placeholders, RTL/Japanese and fallback verified.

### T04.01 / done: Implement UI strings and content localization infrastructure

Need: Learners need offline UI/meanings/explanations in one resolved language.
Type: technical. Role: Localization. Priority: P1.
Output: Implemented scoped UI catalog, 19-locale System resolution, per-field lookup/fallback, revision-bound locale sidecars and package/index projection. Coverage separates 15,002 authored fields from 2,018 empty optional usage notes. Evidence: 24 macOS runtime tests and one native UI test across EN/Arabic/Hebrew with three inspected captures; not translation review or full app integration.
Execution dependencies: H01.
Feature contracts: F09, F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md), [engineering-contract.md](engineering-contract.md), [runtime-data-contract.md](runtime-data-contract.md).

Acceptance:

- Resolve System and English fallback per field; do not match unrelated-locale meanings.
- Check placeholders/plurals and Japanese LTR in RTL; fallback is not translation coverage.

Implementation / handoff checklist:

- Externalize UI strings and connect locale-aware package/index.
- Build coverage reports and fallback/placeholder/RTL fixtures.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: [t09-01-localization-validation.json](audit/t09-01-localization-validation.json), [coverage.json](localization/coverage.json), [README.md](localization/README.md)

### T04.02 / ready: Review and complete Vietnamese/English

Need: Learners need accurate VI/EN; English is also the fallback for other locales.
Type: locale. Role: Localization. Priority: P1.
Output: VI/EN content/UI with separate coverage and review; drafts are not approved translations.
Execution dependencies: T04.01, H02, H03, H04.
Feature contracts: F11.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Review lessons/Kanji/kana/candidates/UI against a dataset revision, preserving IDs/provenance.
- Check semantics, contextual reading alignment, placeholders and long strings in the app.

Implementation / handoff checklist:

- Complete/review both locales across the dataset.
- Record reviewer, coverage and outstanding entries.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using vi/en, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched vi/en dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.02-E2E-01 / happy

Given: The package contains reviewed vi/en resources and the app is offline.
When: Select vi/en in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.02-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.03 / todo: Complete and review Arabic (ar)

Need: Arabic-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Arabic UI, lesson/Kanji/kana/candidate meanings and explanations; separate ar coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native RTL, Japanese LTR and long strings.

Implementation / handoff checklist:

- Author and review ar resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using ar, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched ar dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.03-E2E-01 / happy

Given: The package contains reviewed ar resources and the app is offline.
When: Select ar in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.03-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.04 / todo: Complete and review Bengali (bn)

Need: Bengali-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Bengali UI, lesson/Kanji/kana/candidate meanings and explanations; separate bn coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review bn resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using bn, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched bn dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.04-E2E-01 / happy

Given: The package contains reviewed bn resources and the app is offline.
When: Select bn in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.04-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.05 / todo: Complete and review Chinese Simplified (zh-Hans)

Need: Chinese Simplified-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Chinese Simplified UI, lesson/Kanji/kana/candidate meanings and explanations; separate zh-Hans coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review zh-Hans resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using zh-Hans, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched zh-Hans dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.05-E2E-01 / happy

Given: The package contains reviewed zh-Hans resources and the app is offline.
When: Select zh-Hans in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.05-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.06 / todo: Complete and review Dutch (nl)

Need: Dutch-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Dutch UI, lesson/Kanji/kana/candidate meanings and explanations; separate nl coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review nl resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using nl, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched nl dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.06-E2E-01 / happy

Given: The package contains reviewed nl resources and the app is offline.
When: Select nl in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.06-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.07 / todo: Complete and review French (fr)

Need: French-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: French UI, lesson/Kanji/kana/candidate meanings and explanations; separate fr coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review fr resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using fr, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched fr dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.07-E2E-01 / happy

Given: The package contains reviewed fr resources and the app is offline.
When: Select fr in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.07-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.08 / todo: Complete and review German (de)

Need: German-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: German UI, lesson/Kanji/kana/candidate meanings and explanations; separate de coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review de resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using de, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched de dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.08-E2E-01 / happy

Given: The package contains reviewed de resources and the app is offline.
When: Select de in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.08-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.09 / todo: Complete and review Hebrew (he)

Need: Hebrew-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Hebrew UI, lesson/Kanji/kana/candidate meanings and explanations; separate he coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native RTL, Japanese LTR and long strings.

Implementation / handoff checklist:

- Author and review he resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using he, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched he dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.09-E2E-01 / happy

Given: The package contains reviewed he resources and the app is offline.
When: Select he in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.09-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.10 / todo: Complete and review Hindi (hi)

Need: Hindi-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Hindi UI, lesson/Kanji/kana/candidate meanings and explanations; separate hi coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review hi resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using hi, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched hi dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.10-E2E-01 / happy

Given: The package contains reviewed hi resources and the app is offline.
When: Select hi in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.10-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.11 / todo: Complete and review Indonesian (id)

Need: Indonesian-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Indonesian UI, lesson/Kanji/kana/candidate meanings and explanations; separate id coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review id resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using id, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched id dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.11-E2E-01 / happy

Given: The package contains reviewed id resources and the app is offline.
When: Select id in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.11-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.12 / todo: Complete and review Italian (it)

Need: Italian-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Italian UI, lesson/Kanji/kana/candidate meanings and explanations; separate it coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review it resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using it, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched it dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.12-E2E-01 / happy

Given: The package contains reviewed it resources and the app is offline.
When: Select it in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.12-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.13 / todo: Complete and review Korean (ko)

Need: Korean-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Korean UI, lesson/Kanji/kana/candidate meanings and explanations; separate ko coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review ko resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using ko, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched ko dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.13-E2E-01 / happy

Given: The package contains reviewed ko resources and the app is offline.
When: Select ko in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.13-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.14 / todo: Complete and review Portuguese (pt)

Need: Portuguese-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Portuguese UI, lesson/Kanji/kana/candidate meanings and explanations; separate pt coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review pt resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using pt, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched pt dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.14-E2E-01 / happy

Given: The package contains reviewed pt resources and the app is offline.
When: Select pt in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.14-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.15 / todo: Complete and review Russian (ru)

Need: Russian-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Russian UI, lesson/Kanji/kana/candidate meanings and explanations; separate ru coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review ru resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using ru, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched ru dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.15-E2E-01 / happy

Given: The package contains reviewed ru resources and the app is offline.
When: Select ru in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.15-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.16 / todo: Complete and review Spanish (es)

Need: Spanish-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Spanish UI, lesson/Kanji/kana/candidate meanings and explanations; separate es coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review es resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using es, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched es dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.16-E2E-01 / happy

Given: The package contains reviewed es resources and the app is offline.
When: Select es in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.16-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.17 / todo: Complete and review Thai (th)

Need: Thai-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Thai UI, lesson/Kanji/kana/candidate meanings and explanations; separate th coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review th resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using th, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched th dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.17-E2E-01 / happy

Given: The package contains reviewed th resources and the app is offline.
When: Select th in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.17-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.18 / todo: Complete and review Turkish (tr)

Need: Turkish-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Turkish UI, lesson/Kanji/kana/candidate meanings and explanations; separate tr coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review tr resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using tr, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched tr dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.18-E2E-01 / happy

Given: The package contains reviewed tr resources and the app is offline.
When: Select tr in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.18-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T04.19 / todo: Complete and review Ukrainian (uk)

Need: Ukrainian-speaking learners need consistent, natural offline UI and learning content.
Type: locale. Role: Localization. Priority: P1.
Output: Ukrainian UI, lesson/Kanji/kana/candidate meanings and explanations; separate uk coverage.
Execution dependencies: T04.02.
Feature contracts: F11, F13.
Read: [settings-and-localization.md](design-system/settings-and-localization.md).

Acceptance:

- Cover required fields of the pinned dataset; preserve IDs and Japanese/readings; English fallback is not translated coverage.
- Review semantics/placeholders/plurals and native layout with long strings/system fonts.

Implementation / handoff checklist:

- Author and review uk resources; record reviewer and revision.
- Run coverage, rebuild package/index and verify the app in this locale.

Required evidence: Per-locale coverage, translation review evidence and app captures for long strings/RTL where applicable; identify fallback fields.
Recorded evidence: none; completion not established.

User story: As a learner using uk, I want reviewed UI and learning translations in the same language so I can study accurately offline.

E2E status: not_run. Surface: localized_app_widget.
Additional E2E closure prerequisites: T01.12, T02.05, T03.03, T03.04, T05.05, T05.07.
Fixture: Revision-matched uk dataset/review; required lesson/Kanji/kana/candidate/UI field ledger; long strings and an invalid sidecar in a separate test package.

#### T04.19-E2E-01 / happy

Given: The package contains reviewed uk resources and the app is offline.
When: Select uk in Settings; visit content types through lists/search/favorites and widgets; execute the full field ledger and open long-string targets.
Then: UI/meanings match the locale by stable ID; Japanese/readings are unchanged, placeholders/plurals are correct, required fields are covered, ar/he use RTL with LTR Japanese and Sino-Vietnamese is VI-only.

#### T04.19-E2E-02 / edge

Given: A separate test package contains a stale/draft sidecar or missing translation, not the release candidate.
When: Build/validate the package; in a valid sparse fixture select the locale, open a missing field, switch languages and relaunch.
Then: Draft/stale resources are rejected; missing fields use labelled English without translated coverage or a release pass; IDs/candidates/favorites/prefixes stay unchanged.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

## T05 / P1 / todo: Widget extension
Phase: development. Owner role: iOS. Parent dependency traceability: H01, H04, T01.
Existing integration output: Native configuration, versioned projections, timelines and eligible families.
Existing integration acceptance: App-closed operation, dedup/expansion, revision ordering and readable counts.

### T05.01 / todo: Configure widget type and source

Need: Learners need to choose a content type and source for each widget.
Type: native. Role: iOS. Priority: P1.
Output: Extension and native vocabulary/pattern/Kanji by learned/favorites configuration. Include a minimal native widget reading real data and displaying one complete target for configuration-to-entry E2E; T05.05–07 complete families/layouts. Include baseline atomic projection publication after actual committed changes for T05.02/03; T05.04 completes race/failure/retry and timeline lifecycle rather than owning the first working publication path.
Execution dependencies: H01, H04, T01.
Feature contracts: F12.
Read: [widgets.md](design-system/widgets.md).

Acceptance:

- Unconfigured differs from configured-empty; empty sources retain configuration without switching pools.
- Taps only open normal app entry; no item deep links or inline playback/favorites.

Implementation / handoff checklist:

- Create extension/configuration for the project platform.
- Verify configuration, unconfigured and empty sources in the native gallery.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want a type and source per widget so it displays the content I choose.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: A minimal native WidgetKit extension with real bundle/projection entries; three types × two sources; empty and nonempty pools.

#### T05.01-E2E-01 / happy

Given: The app has committed learned/favorites and the widget is unconfigured.
When: Add a Home widget, choose each type/source, terminate the app and tap the widget.
Then: Native entries use the correct actual pool with the app closed; tapping opens normal app entry without a deep link/audio.

#### T05.01-E2E-02 / edge

Given: One widget is unconfigured and another has a configured empty pool.
When: Inspect/edit both and launch the app from the widget.
Then: The two states/guidance differ; empty configuration is retained without borrowing another source/type.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.02 / todo: Build learned widget pools from both levels and Kanji milestones

Need: Learners need widgets to use the actual learned content of each level.
Type: technical. Role: iOS. Priority: P1.
Output: Eligibility pools for all three content types from committed prefixes.
Execution dependencies: T05.01, T03.05.
Feature contracts: F03, F08, F12.
Read: [widgets.md](design-system/widgets.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- N5/N4 remain independent; units 21–25 use N5 lesson 25; selected app level does not replace the pool.
- Patterns use the shared example selector; empty learned sources never borrow favorites.

Implementation / handoff checklist:

- Build pool lookup from milestone lesson IDs.
- Test none/N5/N4/both and unit boundary milestones.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: none; completion not established.

User story: As a learner, I want widgets to use both saved prefixes so they show learned material.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: None/N5-only/N4-only/both; N5=24/25; units 21–25 tied to N5=25; deterministic adapter clock/random.

#### T05.02-E2E-01 / happy

Given: A learned-source widget has one of the three types configured.
When: Mark prefixes in the app, close it and receive a new entry; change selected app level and repeat.
Then: IDs follow the learned union/milestones; 21–25 require N5=25; selected level does not change the pool and patterns use the shared selector.

#### T05.02-E2E-02 / edge

Given: No lessons are learned but favorites exist, or a prefix save fails.
When: Inspect the learned widget, fail marking, request an entry and Retry.
Then: It remains learned-empty until commit without borrowing favorites or using unsaved prefixes.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.03 / todo: Build favorite widget pools with lesson/unit expansion

Need: Learners need widgets to use favorites regardless of learned status.
Type: technical. Role: iOS. Priority: P1.
Output: Per-content-type parent expansion and target-ID deduplication.
Execution dependencies: T05.01, T02.04.
Feature contracts: F10, F12.
Read: [widgets.md](design-system/widgets.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Expansion occurs only for widgets without creating direct child favorites in the app.
- Parent plus child does not duplicate pool IDs and is independent of prefixes; unavailable targets are excluded without switching pool/source.

Implementation / handoff checklist:

- Connect favorite references to bounded parent expansion.
- Connect favorite references to bounded parent expansion; try independent parent/child saves, deduplication, unavailable targets and empty pools.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: none; completion not established.

User story: As a learner, I want widgets to use favorites including unlearned lessons so I can review my choices.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: T03.02, T02.05.
Fixture: Separately saved lesson/unit parents and children; no learned lessons; unavailable favorite; deterministic sampling.

#### T05.03-E2E-01 / happy

Given: A favorites widget is configured for the target type.
When: Save parent and child, close the app, receive an entry, remove the parent and receive another.
Then: Expansion occurs only in the widget pool with ID dedup and no learned prerequisite; app direct favorites gain no children and separately saved children remain.

#### T05.03-E2E-02 / edge

Given: A saved favorite is unresolved or the selected-type pool is empty.
When: Receive an entry and open app Favorites.
Then: The widget excludes unavailable targets without changing source/type; the app retains the unavailable row and original ID.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.04 / todo: Publish post-commit projections and build timelines

Need: Learners need widgets to reflect saved data and work with the app closed.
Type: technical. Role: iOS. Priority: P1.
Output: Atomic shared projections, version/revision validation and randomized timelines.
Execution dependencies: T05.02, T05.03, T01.11.
Feature contracts: F12, F14.
Read: [widgets.md](design-system/widgets.md), [engineering-contract.md](engineering-contract.md).

Acceptance:

- Stale producers cannot overwrite newer revisions; publication failure after save does not roll back user state and supports rebuild/retry.
- No duplicate IDs per entry; target 15 minutes subject to system scheduling; extension reads bundles with the app closed.

Implementation / handoff checklist:

- Build projection publication and timeline clock/random seams.
- Verify publication failure, stale revisions, app-closed and incompatible projections.

Required evidence: Reproduction fixtures, failure-boundary test results and input/implementation revision; no implied app acceptance.
Recorded evidence: none; completion not established.

User story: As a learner, I want widgets to update after saves and work with the app closed so they reflect committed state.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: Revisions R/R+1; failed save, post-save publication failure, late producer and corrupt projection; clock seam.

#### T05.04-E2E-01 / happy

Given: The widget is displaying projection R.
When: Change learned/favorites/language/furigana, commit R+1, terminate the app and receive a timeline.
Then: Entries use one consistent R+1 snapshot and distinct IDs without a running app; the timeline requests 15 minutes without promising exact OS refresh.

#### T05.04-E2E-02 / edge

Given: Producer R is delayed and publishing R+1 may fail after save.
When: Fail publication, reopen app state, retry/rebuild R+1, release producer R and test a corrupt projection.
Then: Saved state never rolls back, R cannot overwrite R+1, partial projections are not consumed, unavailable/rebuild is scoped and failed saves never publish.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.05 / todo: Render Home Small/Medium/Large widgets

Need: Learners need readable learning content in each Home widget size.
Type: native. Role: iOS. Priority: P1.
Output: Native layouts for three content types and three families.
Execution dependencies: T05.04.
Feature contracts: F05, F11, F12.
Read: [widgets.md](design-system/widgets.md).

Acceptance:

- Vocabulary/pattern/Kanji ceilings: Small 1/1/1, Medium 2/1/1, Large 4/2/2.
- Reduce fields/items for long/large text; keep Japanese/ruby intact and share language/furigana.

Implementation / handoff checklist:

- Render by geometry/family and native surface.
- Capture each type/family with long/large text and empty/error states.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want readable Small/Medium/Large Home widgets so I can review complete content quickly.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: Three types × three families; full/small/empty pools; long text, ruby on/off, system text sizes and VI/EN.

#### T05.05-E2E-01 / happy

Given: The native gallery supports the selected family.
When: Add each family/type, change shared language/furigana, receive an entry and tap.
Then: Ceilings S=1/1/1, M=2/1/1, L=4/2/2; Japanese/ruby/meanings remain complete with distinct IDs; tap opens normal app entry.

#### T05.05-E2E-02 / edge

Given: Text is long/large or the pool is smaller than the ceiling.
When: Capture each native family at large system text size, Light/Dark and tinted where supported.
Then: Reduce fields/items without broken ruby or duplicate padding; do not force app theme and distinguish empty/unavailable.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.06 / todo: Render Extra Large and supported variants

Need: iPad learners need readable additional items on larger surfaces.
Type: native. Role: iOS. Priority: P1.
Output: Two-column XL, variant reflow and family-eligibility evidence.
Execution dependencies: T05.05.
Feature contracts: F12, F13.
Read: [widgets.md](design-system/widgets.md).

Acceptance:

- Ceilings of 8 words/4 patterns/4 Kanji, reduced to fit; no rotated fixed canvas.
- Claim only SDK/device-supported families; record missing gallery/device evidence.

Implementation / handoff checklist:

- Check family availability and adaptive XL layouts.
- Capture gallery/snapshots on supported iPad and difficult locales.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As an iPad learner, I want adaptive Extra Large widgets so I can read more items clearly.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: iPad/SDK with verified gallery eligibility; three types, long/large text; Extra Large Portrait only if actually supported.

#### T05.06-E2E-01 / happy

Given: Extra Large is present in the recorded device/simulator gallery.
When: Add the widget and try vocabulary/pattern/Kanji in supported sizes/orientations.
Then: Ceilings are 8/4/4 in adaptive two-column layouts with aligned targets/meanings/ruby and normal app opening.

#### T05.06-E2E-02 / edge

Given: Text is too long or Portrait is absent from the gallery.
When: Increase system text size and inspect each family eligibility.
Then: Reduce items/fields without rotating a fixed canvas; record unsupported/unperformed families, never treating SDK declarations as gallery proof.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

### T05.07 / todo: Render compact Lock Screen widgets

Need: Learners need an intact short item or app-opening cue on the Lock Screen.
Type: native. Role: iOS. Priority: P1.
Output: Actually supported rectangular/circular/inline layouts.
Execution dependencies: T05.04.
Feature contracts: F12.
Read: [widgets.md](design-system/widgets.md).

Acceptance:

- If no complete item fits, show an app-opening cue rather than a false empty-source state.
- Distinguish unconfigured/empty/unavailable/fitting fallback; add no inline actions.

Implementation / handoff checklist:

- Render compact families with approved field order and fitting policy.
- Verify snapshots/tint/taps and long text on supported families.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

User story: As a learner, I want a short Lock Screen item or app-opening cue so content stays readable.

E2E status: not_run. Surface: widget.
Additional E2E closure prerequisites: none.
Fixture: Actually supported compact families; a short term, long sentence and Kanji; unconfigured/empty/unavailable/fitting-fallback states.

#### T05.07-E2E-01 / happy

Given: The native Lock Screen widget has a configured pool with a fitting target.
When: Add each compact family/type, inspect the snapshot and tap.
Then: Show a complete target with geometry-appropriate fields; tap opens the app without inline playback/favorite actions.

#### T05.07-E2E-02 / edge

Given: The pool is nonempty but its sentence cannot fit, alongside separate empty/error fixtures.
When: Run each state on the same family and capture native output.
Then: Non-fitting content uses an app-opening cue rather than false emptiness; all four states stay distinct and retain type/source.

E2E completion evidence: Case ID; repository/build/content/package/review revision; OS/device/family/voice where applicable; fixture and stable target IDs; expected/actual; logs/xcresult and captures/video; per-case status, failures and unperformed scope.

## T06 / P1 / todo: UX and performance acceptance
Phase: acceptance. Owner role: QA. Parent dependency traceability: T02, T03, T04, T05.
Existing integration output: Full corpus, large text/RTL, adaptive devices and Release benchmarks.
Existing integration acceptance: Record device/OS/dataset/baseline/budgets/results; no clipping or unbounded memory.

### T06.01 / todo: Accept complete journeys over the full corpus

Need: Learners need features to work together over the complete content.
Type: native. Role: QA. Priority: P1.
Output: Native end-to-end matrix across F01–F14 and defect/evidence ledger.
Execution dependencies: T02, T03, T04, T05, T01.12.
Feature contracts: F01, F02, F03, F04, F09, F10, F12.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- Exercise entry to read/listen to learned state to search/favorites to widgets, offline and relaunch.
- Save failure, stale callbacks/projections and multiple scenes preserve committed state.

Implementation / handoff checklist:

- Pin build/dataset and execute the acceptance matrix.
- Record expected/actual behavior, evidence and defect retests.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

### T06.02 / todo: Accept large text, RTL and adaptive device layouts

Need: Learners need complete readable content across languages, text sizes and window sizes.
Type: native. Role: QA. Priority: P1.
Output: Screen/widget by locale/text-size/width matrix on supported devices.
Execution dependencies: T06.01.
Feature contracts: F05, F11, F12, F13.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- No clipping/overlapping hit targets; Japanese/ruby LTR in Arabic/Hebrew; resizing retains logical routes.
- Identify evidenced or missing iPhone/iPad/Duo coverage; do not reopen deferred VoiceOver scope.

Implementation / handoff checklist:

- Execute the matrix with long strings and system text sizes.
- Save native captures/evidence and untested device inventory.

Required evidence: Native app evidence: build/OS/device or simulator, reproduction steps and results; list untested cases separately.
Recorded evidence: none; completion not established.

### T06.03 / todo: Measure launch, reading, search and audio performance

Need: Learners need fast launch and interactions with the complete dataset.
Type: performance. Role: QA. Priority: P1.
Output: Latency/CPU/RAM/cache baseline and budgets with cold/warm results.
Execution dependencies: T06.01.
Feature contracts: F14.
Read: [performance-and-footprint.md](design-system/performance-and-footprint.md).

Acceptance:

- No whole-corpus decode/import at launch/query; measure detail open/jump.
- Repeated browsing/multiple scenes/memory pressure demonstrate bounded caching; unagreed budgets remain pending.

Implementation / handoff checklist:

- Record method, device/OS and Release dataset.
- Measure contract scenarios, investigate regressions and record limits.

Required evidence: Release build plus physical device/OS/dataset/method/baseline/budgets/results; record unavailable device evidence.
Recorded evidence: none; completion not established.

### T06.04 / todo: Measure widget performance and installed footprint

Need: Learners need stable widgets and bounded installed/cache growth.
Type: performance. Role: QA. Priority: P1.
Output: Extension memory/timeline cost, projection size and app/content/index/cache sizes.
Execution dependencies: T06.01, T05.
Feature contracts: F12, F14.
Read: [performance-and-footprint.md](design-system/performance-and-footprint.md).

Acceptance:

- Measure large/empty pools with the app closed on devices; simulator results do not establish physical performance.
- Separate installed/download/resources/writable cache; include all 19 locales and baseline/budget/results.

Implementation / handoff checklist:

- Measure timelines/projections with large data and failure cases.
- Record size breakdown and cache growth under repeated use.

Required evidence: Release build plus physical device/OS/dataset/method/baseline/budgets/results; record unavailable device evidence.
Recorded evidence: none; completion not established.

## T07 / P1 / todo: Content and release acceptance
Phase: release. Owner role: Owner + QA. Parent dependency traceability: H02, H04, T04, T06.
Existing integration output: Editorial/source review, rights evidence, branding/IDs/markets/age and release checklist.
Existing integration acceptance: Close blockers with evidence; no claim of release from structural validation alone.

### T07.01 / todo: Accept source fidelity, language and pronunciation

Need: Learners need accurate, natural content and correct pronunciation.
Type: release. Role: Owner + QA. Priority: P1.
Output: Editorial/source/locale/pronunciation sign-off on a pinned dataset.
Execution dependencies: H02, H03, H04, T04, T06.
Feature contracts: F02, F04, F06, F07, F08, F11.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- Evidence covers H02/H03/H04/T04 gates; counts/validators do not replace content review.
- Record reviewer/scope/gaps; drafts/fallback cannot be called accepted content.

Implementation / handoff checklist:

- Assemble the evidence ledger and review a fixed revision.
- Resolve content defects and record each gate outcome.

Required evidence: Checklist with accountable approval and evidence links per gate; open blockers are not passes.
Recorded evidence: none; completion not established.

### T07.02 / todo: Confirm content rights and distribution scope

Need: The product owner needs evidence of content rights before distribution.
Type: release. Role: Owner + QA. Priority: P1.
Output: Rights/provenance checklist and outstanding owner decisions.
Execution dependencies: H02.
Feature contracts: F15.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- Evidence covers required sources/resources; repository PDFs do not imply distribution rights.
- Missing rights or owner decisions remain blockers; do not silently replace content or scope.

Implementation / handoff checklist:

- Inventory distribution resources and rights evidence.
- Record specific owner questions where evidence is missing.

Required evidence: Checklist with accountable approval and evidence links per gate; open blockers are not passes.
Recorded evidence: none; completion not established.

### T07.03 / todo: Confirm branding, identifiers and store metadata

Need: The product owner needs correct and confirmed distribution metadata.
Type: release. Role: Owner + QA. Priority: P1.
Output: Name/icon/bundle/publisher/markets/age and metadata checklist.
Execution dependencies: T07.02, T06.
Feature contracts: F01, F11, F15.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- Ask the owner for missing choices; do not change project/bundle identifiers by default.
- Metadata claims only evidenced features/locales/devices.

Implementation / handoff checklist:

- Assemble current values, gaps and a concrete review artifact.
- Record received owner decisions in the owner contract and apply the authorized scope.

Required evidence: Checklist with accountable approval and evidence links per gate; open blockers are not passes.
Recorded evidence: none; completion not established.

### T07.04 / todo: Verify the release candidate and release decision

Need: The product owner needs an evidenced candidate for a release decision.
Type: release. Role: Owner + QA. Priority: P1.
Output: Build/dataset-pinned release checklist, blockers and owner sign-off.
Execution dependencies: T07.01, T07.02, T07.03, T06.
Feature contracts: F01, F14, F15.
Read: [acceptance.md](design-system/acceptance.md).

Acceptance:

- Content, migration behavior, rights and native/layout/performance evidence are complete; per-form speech behavior is implemented and required speech-context authoring/review is complete.
- Missing required budgets/devices/evidence keep gates open; decomposition does not authorize publication.

Implementation / handoff checklist:

- Assemble the checklist from each group evidence set.
- Record the owner decision for the exact candidate; structural passes are not release passes.

Required evidence: Checklist with accountable approval and evidence links per gate; open blockers are not passes.
Recorded evidence: none; completion not established.
