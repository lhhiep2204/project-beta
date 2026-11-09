> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Settings and localization

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Shared language, System defaults, system text sizing, RTL/fallback presentation and the initial landing/level scope are confirmed.

## Confirmed controls

| Preference | Confirmed behavior | Authority |
| --- | --- | --- |
| Language | One shared selection for interface and translated meanings/explanations, default System. Japanese remains the taught language. Support the approved 19 languages and English fallback. | B-U-13/23/46, DS-U-35/36. |
| Appearance | System / Light / Dark, locally persisted; default System. | B-U-23/46, DS-U-36. |
| Furigana | On by default, app-wide, locally persisted; lesson-toolbar quick control uses the same preference. | B-U-17/21/46, DS-U-17. |
| Level | First launch asks N5/N4; later launches remember it. Open Lessons; Lessons/Kanji share the visible level switch/preference. | DS-U-18/36. |
| Text size | Follow system Dynamic Type with content-specific system type roles/weights. No independent in-app size control. | DS-U-37. |

The 19 supported languages remain Arabic, Bengali, Chinese Simplified, Dutch, English, French, German, Hebrew, Hindi, Indonesian, Italian, Korean, Portuguese, Russian, Spanish, Thai, Turkish, Ukrainian and Vietnamese. Do not add Japanese as an interface/translation language or split the shared preference into separate pickers.

Selecting a language does not change Japanese base text or its reviewed reading. UI strings and translated learning content remain separate resources with separate coverage, despite sharing the user preference. A missing translation must use the approved English fallback, not invent a machine translation or require a network request.

DS-U-45 limits displayed Sino-Vietnamese readings to Vietnamese. Hide this display field when the resolved shared language is not Vietnamese, including optional widget detail; retain the source data and previously approved search fields.

DS-U-47/48 defers VoiceOver/specialized Accessibility support/testing while retaining Dynamic Type. DS-U-49 retains RTL for Arabic/Hebrew and correct Japanese order; these are localization/UI requirements.

## Confirmed defaults and presentation

- Initial language choice: System; initial appearance: System.
- Respect system text size through Dynamic Type; type roles/weights differ by content kind under [foundations](foundations.md).
- After level selection, open Lessons at the remembered level. Lessons/Kanji share the preference through a visible level switch. Changing level never changes either learned prefix.

Use a native grouped Settings presentation: learning preferences (level, shared language, furigana) and appearance. Final translation catalogs must provide the approved language coverage; sample HTML text is not that localization batch. A browser review's text-size selector is a review tool, not an approved app setting.

## Localization and state obligations

- Keep selected target IDs, learned prefixes and direct favorite identities stable when language/appearance/furigana changes. The chosen example's translation/audio/ruby must stay aligned.
- Preserve complete mixed-script content and allow long translations to wrap. Do not reverse Japanese glyph/reading order in an RTL interface.
- Use native RTL navigation and proper LTR Japanese blocks. Show a concise English label beside translated learning content only when the requested language actually falls back to English. Preserve visible example IDs across language changes. Specialized VoiceOver remains deferred; playback follows logical screen ownership as specified in implementation-guide.md.
- Follow [performance constraints](performance-and-footprint.md): invalidate only affected presentation work; do not decode all languages or rebuild the full corpus for a preference toggle.
- Reminders, accounts/profiles, purchases, backup/export and speed settings remain deferred. Do not fill Settings with unrequested deferred controls.

No new language-coverage, native-layout or device-accessibility pass is established by this document.
