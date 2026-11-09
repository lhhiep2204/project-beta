# Agent design-contract map

The only owner review is [../index.html](../index.html). No separate palette, entry, lesson or widget HTML is maintained. Product scope, flows, tasks and approved behavior are in that artifact; the contracts below are generated from its embedded project-contract and must not be independently edited.

| Work | Read |
| --- | --- |
| Scope/history | [Owner decisions (historical)](decisions.md); current feature cards and migration/speech requirements in the HTML |
| Foundation | [foundations.md](foundations.md), [tokens.json](tokens.json) |
| Navigation/flows | [implementation-guide.md](implementation-guide.md), [entry-and-learning-state.md](entry-and-learning-state.md) |
| Playback | [components.md](components.md), [screens-and-playback.md](screens-and-playback.md) |
| Search/favorites/kana/Kanji | [kanji-alphabets-search-favorites.md](kanji-alphabets-search-favorites.md) |
| Candidate selection | [example-selection.md](example-selection.md) |
| Settings/states | [settings-and-localization.md](settings-and-localization.md), [interaction-and-accessibility.md](interaction-and-accessibility.md) |
| Widgets/performance | [widgets.md](widgets.md), [performance-and-footprint.md](performance-and-footprint.md) |
| Acceptance | [acceptance.md](acceptance.md), [engineering contract](../engineering-contract.md), [delivery plan](../delivery-plan.md) |

Keep Dynamic Type, RTL/native states and TTS; specialized VoiceOver/Accessibility remains deferred under DS-U-47/48/49. Prototype geometry, timers, two-language samples and 57 kana cells are not native behavior or full curriculum proof. Earlier file-specific review notes are historical evidence only.

Run `python3 scripts/build_design_review.py` after corpus changes, then `python3 scripts/sync_project_review.py`. The review's app and widget simulations are embedded in the one HTML and isolated from application data. Structural/helper checks cannot substitute for browser/native visual and interaction QA.
