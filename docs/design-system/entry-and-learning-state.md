> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# First entry, learned lessons and favorite actions

Status: **NORMATIVE DESIGN CONTRACT v1.0.** UI product behavior is confirmed. HTML geometry is illustrative; content/runtime evidence and version-migration policy remain separate dependencies.

## Level selection

Authority: DS-U-18. First launch presents a level-selection screen with N5 and N4 available. Do not preselect N5 or require N5 learned state before choosing N4. Persist a successfully selected level locally and use it on later launches rather than forcing the selection screen again. This is level preference persistence, not restoration of a lesson or reading position.

DS-U-36 confirms that level selection opens Lessons and that Lessons/Kanji share a remembered preference through a visible level switch. Use the visible level switch and failure/retry behavior in implementation-guide.md and the native state contract. The entry HTML demonstrates the approved lesson-list landing and change-level concept; its geometry is illustrative. No extra onboarding slides or permission prompts are requested.

Preserve source numbering: N5 lessons 1–25 and N4 lessons 26–50. Source counts belong to content data, not UI identity or hard-coded implementation IDs. Both levels remain freely accessible.

## Learned-prefix control

Authority: B-U-35/46/58 and DS-U-19. Show the learned-state action at the start of the lesson, with learned status in the lesson list. This represents a manual continuous prefix within that lesson's level; it is not a score, assessment, lock or mastery indicator.

| Operation | Result | Other level |
| --- | --- | --- |
| Mark N5 lesson 6 | N5 lessons 1–6 are learned. | Unchanged. |
| Unmark N5 lesson 5 | N5 lessons 5 and later become unlearned; N5 lessons 1–4 remain learned. | Unchanged. |
| Mark N4 lesson 30 | N4 lessons 26–30 are learned. | Unchanged; N5 is not a prerequisite. |
| Unmark N4 lesson 28 | N4 lessons 28 and later become unlearned; N4 lessons 26–27 remain learned. | Unchanged. |

### Range confirmation

Before an operation changes multiple lessons, show a confirmation naming its level, operation and affected range. Compute the actual changed set against the current persisted prefix. Do not imply that already learned/unlearned lessons are being changed. Confirmation examples are illustrative copy, not final localized strings:

- If N5 has no learned lessons, marking lesson 6 changes lessons 1–6: explain this range before applying.
- If N5 currently has lessons 1–3 learned, marking lesson 6 changes lessons 4–6. The resulting learned prefix is 1–6; distinguish the change from the resulting state.
- If N4 currently has lessons 26–30 learned, unmarking lesson 28 changes lessons 28–30. N4 lessons 26–27 stay learned and N5 stays unchanged.

Cancel leaves both prefixes unchanged. Confirm applies the level-scoped mutation atomically through the owning use case. Display success after persistence succeeds; publish widget-derived state only after the same successful change. Failed/canceled changes cannot leak into widget eligibility.

DS-U-44 confirms immediate application for a change affecting only one lesson, with brief success feedback after persistence. Failed writes preserve the last committed state and offer retry; multi-lesson changes still require range confirmation. No extra undo feature is selected. No automatic playback stopping is implied merely by showing the confirmation while the lesson remains the logical screen.

## Favorite interaction

Authority: DS-U-20, B-U-25/43/46/49. Favorite actions live in a touch-and-hold context menu; read [component contracts](components.md). Preserve the distinction between a directly favorited item and a favorited lesson/unit. Parent expansion for the favorites widget remains independent of learned status; favoriting a parent must not silently create direct favorites for every child.

DS-U-23/44 confirms the all-types default, newest-saved-first order, type/N5/N4 filters, directly saved parent/item rows and immediate remove with success/failure/retry feedback. A favorited parent stays one row; it does not create child favorites or remove independently saved children when removed. See [the favorites-screen contract](kanji-alphabets-search-favorites.md). No new favorite type, collection folder or saved search is introduced.

## Evidence and remaining decisions

HTML interactions are review simulations. Browser memory/storage is not application SwiftData evidence. The level-entry sketch may remember only its own browser preference; the learned-prefix and favorites demonstrations must not modify actual app data.

Follow the final [implementation bindings](implementation-guide.md), [state contract](interaction-and-accessibility.md) and [acceptance](acceptance.md). The total example cap is three without expansion; Extra Large and native state/localization are confirmed. Content authoring/runtime proof remains distinct from document completion.
