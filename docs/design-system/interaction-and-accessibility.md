> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Interaction, state and accessibility

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Local-write/favorites, Vietnamese-only Sino-Vietnamese, playback, system text sizing, RTL/localization and native states are confirmed. VoiceOver/specialized Accessibility support/testing is deferred under DS-U-47/48.

## Existing obligations

- Preserve committed local favorites, learned prefixes and preferences. Cancellation/save failure cannot be published as success or leak into widget/example eligibility.
- Stop playback on logical screen departure/backgrounding. Replacing/restarting invalidates old callbacks; changing geometry alone preserves the same logical screen.
- Read offline with missing-voice guidance and English translation fallback.
- Preserve approved system typography/geometry and system text-size following under DS-U-48. DS-U-49 retains RTL/localization. Dedicated VoiceOver/Accessibility specialization and acceptance are deferred.
- Do not claim an unavailable search index produced a complete no-results answer. Bound loading, search and widget work under [performance constraints](performance-and-footprint.md).

## Reviewed interaction decisions

| ID | Status | Concrete proposal |
| --- | --- | --- |
| DS-P-07 | ACCEPTED · DS-U-44 | Single-lesson changes/remove-favorite apply immediately without another confirmation; multi-lesson changes retain range confirmation. Brief success follows commitment; failed writes keep saved state and offer retry. |
| DS-P-08 | ACCEPTED · DS-U-44 | List directly saved parents/items only; saved lesson/unit is one entry. Existing widget parent expansion remains unchanged. |
| DS-P-09 | RESOLVED · DS-U-45 | Sino-Vietnamese display only when Vietnamese is selected, including optional widget detail. No additional preference switch. |
| DS-P-10 | ACCEPTED · DS-U-46 | Explicit speaker taps use media volume even in silent mode. No autoplay. Phone/audio interruption or headphone disconnection stops, without automatic resumption. |
| DS-P-11 | RESOLVED · DS-U-47/48/49 | Defer specialized VoiceOver/Accessibility. Retain system text sizing, native RTL navigation, proper Japanese order and native pointer context menus. |
| DS-P-12 | ACCEPTED · DS-U-49 | Scoped native loading/empty/error preserves context. Show a concise English fallback-language indication and readable pronunciation setup guidance. |

Confirmed rows are implementation requirements. Specialized Accessibility is not a current-phase delivery gate; platform/runtime evidence remains distinct from design approval.

## Screen-state contract

| Situation | Required invariant | Presentation |
| --- | --- | --- |
| Local detail loading | Keep selected ID/context; no corpus-wide decode or blocked navigation. | Scoped native indicator only while work is actually pending. |
| Failed local save | Do not report committed success or publish unsaved derived state. | Concise failure/retry accepted under DS-U-44. |
| Empty favorites | Preserve current filters and distinguish no saves from no filtered matches. | Concise localized empty-state text and the existing filter controls; no new action beyond approved navigation/context menus. |
| Search debounce/running | 500 ms trailing debounce on committed input; old query results cannot overwrite the current request. | Current request status without a false completed-empty result. |
| Completed no-results search | Only after the current query/scope completes over the approved corpus. | No-results copy and preserved editable query. |
| Empty widget source | Preserve configured source; app-opening tap remains usable. | Compact explanatory text, no substitute pool. |
| Missing Japanese voice | Reading remains fully usable; do not substitute another spoken language. | Setup guidance and retry; no invented direct link to unverified system settings. |
| Missing/corrupt content | Do not present unrelated content or claim the selection succeeded. | Scoped content-unavailable/retry presentation. Editorial completeness remains a release gate. |

## Current-phase evidence and deferred specialization

Current UI/runtime work still needs ruby/translation correctness, touch/pointer context menus, actual Japanese voice/offline/silent-mode/interruption behavior and performance evidence. System text sizing and RTL/localization remain current under DS-U-48/49. Dedicated VoiceOver/Accessibility adaptation and specialized acceptance are deferred under DS-U-47; retain earlier specialist criteria as future reference rather than a current gate. Browser markup and design approval are not native runtime evidence.
