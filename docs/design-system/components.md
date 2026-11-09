> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Component contracts

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Core playback/local-write/favorite behavior and foundations are confirmed. Retain system text sizing/RTL under DS-U-48/49; defer VoiceOver/specialized Accessibility under DS-U-47/48. Read [implementation bindings](implementation-guide.md) for remaining component mappings.

## Content speaker action

Authority: B-U-22/29/47 and DS-U-10/12/13/16.

The button is a **play/restart action**, not a mute toggle, stop toggle or pause/resume action.

| State | Visual | Activation |
| --- | --- | --- |
| Idle | Speaker without sound-wave marks. Do not use a slash or an X to represent mute. | Start the target from its beginning. |
| Starting | No claim that sound is playing until the audio service reports playback. Use the scoped native pending state; stop/cancel remains available. | A new tap replaces the previous request and starts from the beginning. |
| Playing | Speaker with sound-wave marks. | Cancel current playback and restart the tapped target from its beginning. |
| Finished/stopped | Return to the idle speaker; clear any active-turn indicator. | Start the target from its beginning. |
| Missing offline Japanese voice | Preserve reading; activation must provide the approved explanatory/setup guidance. Use the approved readable native setup/error presentation. | Never substitute another spoken language. |

Every visible vocabulary form has its own speaker, connected to that form key and its linked sense/meaning. Never infer a first-form default for an entry with variants. A bound form containing 〜 displays an explanatory context label and plays a complete reviewed word/sentence. If reviewed speech context is absent, retain the readable form and meaning, show “pronunciation unavailable” for that form, and do not call TTS. Single-target actions also apply to a complete Japanese example or dialogue turn. Do not speak translations, grammar-slot labels or visible furigana twice. Furigana visibility does not change pronunciation. Content authoring must supply reviewed speech targets and contexts before release.

### Full-dialogue and turn interaction

- A title-speaker action starts the entire dialogue at its first turn.
- During full-dialogue playback, the title speaker and the currently speaking turn speaker show waves. Other turn speakers remain idle.
- Tapping the title speaker again cancels the current request and restarts the full dialogue at its first turn.
- Tapping any turn speaker, including the currently speaking turn, replaces full-dialogue playback with solo playback of that complete turn from its beginning. It ends after that turn; it does not continue the parent dialogue.
- Tapping the currently playing solo turn restarts that turn from its beginning.
- Selecting any other vocabulary/example/dialogue replaces current playback. Never mix independent utterances.
- Highlight only the active turn. Do not automatically scroll, move keyboard focus or transfer VoiceOver focus as playback advances. Manual scrolling and the owner's explicit section-jump action remain available.
- Whole-dialogue sequencing must follow actual utterance callbacks. Prototype timers do not define production timings, inter-turn pauses or speech speed. Speaker-specific voices and spoken character labels have not been approved.

### Separate stop action

B-U-47 requires an explicit stop control. DS-U-13 changes the speaker interaction without removing that requirement. Stop cancels the active request and clears playing waves/highlighting; it does not pause for later resumption. DS-U-17 approves the separate stop action in the lesson toolbar while playing. Keep stop usable during request preparation/playback; clear it when no request remains. Use approved metrics and localized stop wording. The same separate stop action is available on all playback-capable logical screens, including Kanji and kana, while pending or playing.

Stop on logical screen departure and app backgrounding. Resizing the same logical screen is not departure. Invalidate callbacks associated with canceled requests so an old completion cannot restart or advance the previous dialogue, overwrite current state or highlight an obsolete turn.

### Deferred Accessibility reference — not a current-phase gate

DS-U-47 defers the specialized semantics/acceptance below. They remain future design reference; the learning-content speaker action and its Japanese TTS are still current-phase functionality. No instruction to alter an ordinary native control's built-in platform behavior is inferred from deferral.

- The accessible action name describes what a tap actually does: play from the beginning when idle, restart from the beginning while playing.
- Expose playback state separately from action meaning. The control does not expose a mute or pause action.
- Non-color state cues include wave glyphs and an active-turn indicator. Use localized semantic wording and the approved subtle Teal playing treatment; specialist announcements are deferred.
- Announce meaningful start/stop/failure state without a continual stream of every synthesis callback. Exact VoiceOver announcement policy remains open for accessibility review.
- The speaker action has its own accessible target and must not activate the parent row's navigation/favorite action. Use the approved 44 pt minimum action target; specialist semantics remain deferred.

### Behavioral acceptance cases

1. Tap an idle word speaker: the selected word starts once; active waves appear when playback actually starts.
2. Tap that speaker during playback: pronunciation restarts from the beginning; no pause or stop-toggle behavior occurs.
3. Start the full dialogue: its first turn plays; title and active turn show waves, with only that turn highlighted.
4. Let a turn finish: advance to the next turn, updating indicators without scrolling or moving accessibility focus.
5. Tap the title during a later turn: restart at the first turn and invalidate old callbacks.
6. Tap any turn during full playback: play only that turn from its beginning, then return to idle; do not resume the prior dialogue.
7. Tap another item or the separate stop control: no old callback may resume the canceled request or change the current highlight.
8. Leave the logical screen or background the app: stop and clear indicators. A geometry change alone preserves the same logical request.
9. Disable visible furigana: Japanese pronunciation stays unchanged. A formula's placeholder labels are never passed to speech.
10. Remove suitable Japanese voice availability: reading remains usable and pronunciation offers explanatory guidance without a wrong-language substitute.

These remain implementation acceptance requirements. T01 now supplies bounded native component/UI evidence in audit/t05-native-validation.json; offline/physical audio and full learning-screen integration remain open. See the engineering handoff for exact scope.

## Lesson section-jump menu

Authority: DS-U-09/15/17. Provide direct navigation to vocabulary, grammar, sentence patterns and dialogue within the same continuous lesson, using a menu in the lesson toolbar. This explicit user action can scroll to a section; it does not authorize automatic playback-follow scrolling. Jumping within the same lesson does not by itself stop playback under the logical screen-departure rule. Use approved geometry and localized menu labels; user selection materializes that section. No automatic active-section-follow feature is introduced.

## App-wide furigana toolbar action

Authority: B-U-17/21/46 and DS-U-17. Expose a quick on/off control in the lesson toolbar, bound to the same persisted app-wide preference rather than a lesson-local setting. Default remains on. Changing visibility does not change Japanese playback readings. Use a native control representing its current state; custom Accessibility work is deferred. The compact review uses ふ, with a full localized label where needed. Save failures preserve the committed preference and offer retry. The HTML toolbar and its review-panel checkbox mirror one illustrative preference.

## Favorite context menu

Authority: B-U-25/46 and DS-U-20. Touch-and-hold on an eligible target opens its native context menu. Offer the applicable add/remove-favorite action for that exact content identity. Do not add permanent star buttons or ellipsis buttons as a substitute for the chosen interaction.

- Cover vocabulary, grammar points, sentence patterns, dialogues, individual Kanji, lessons and Kanji units. Parent headers/collection entries target the parent, not an arbitrary child.
- A complete example's speaker remains an audio action; the favorite action for its sentence-pattern group targets the pattern. Dialogue turns are not separately approved favorite targets.
- Long-press targeting must not accidentally activate the embedded speaker or learned-state control. Context menus should apply to the smallest eligible enclosing target.
- Keep native secondary-click invocation for pointer users. Dedicated accessibility actions/acceptance are deferred under DS-U-47.
- The menu reflects actual saved state. Remove immediately and show brief success after persistence; failed writes preserve committed state and offer retry under DS-U-44. Parent removal does not remove independently saved children.
- Opening the menu does not leave the logical reading screen. Starting/stopping audio still follows the playback contract; menu opening alone is not a new stop rule.

Use the native context-menu implementation, not custom production long-press timers. The browser sketch uses illustrative timers and a browser menu solely for review. [Apple context-menu guidance](https://developer.apple.com/design/human-interface-guidelines/context-menus) documents touch-and-hold and secondary-click invocation; the owner's chosen trigger is the product authority.
