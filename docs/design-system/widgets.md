> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Widget design contract

Status: **NORMATIVE DESIGN CONTRACT v1.0.** All Home Screen counts/readability, shared language/furigana and navigation/source behavior are confirmed. Compact-family rendering bindings below preserve those rules; native eligibility/rendering still needs verification.

## Confirmed behavior

Authority: B-U-33/36–45/49/58 and DS-U-39/41.

- Home Screen and Lock Screen, all applicable platform/device families. No watchOS/Live Activity/Shortcuts feature is implied.
- Configure content type: vocabulary, sentence patterns or Kanji; configure source: learned lessons or favorites.
- Random selection from the configured eligible pool, with a 15-minute content timeline target subject to system scheduling. No spaced-repetition/mastery engine.
- Learned-source eligibility uses the actual independent level prefixes and explicit Kanji unit milestones. Favorites-source eligibility is independent of learned status, including items expanded from a favorited lesson/unit.
- Empty sources retain the selection and show explanatory guidance; do not borrow a different source's content.
- Show Japanese, furigana and meaning, with additional Kanji readings/examples when space permits. Reduce fields/counts in compact families for readability.
- Tapping opens the app. No per-item playback, favorite button or deeper navigation action is approved for widgets.

Use compact, versioned content/projections and bounded timeline work under [performance constraints](performance-and-footprint.md). A widget must work without a running app; never publish uncommitted state or let stale projection work replace a newer revision.

## Display matrix

Treat counts as upper targets, not a minimum density or permission to truncate required Japanese/ruby. Long text, large type or restricted family geometry can reduce them.

| Surface | Vocabulary | Sentence patterns | Kanji |
| --- | --- | --- | --- |
| Home small | 1 item | 1 short item | 1 character |
| Home medium | Up to 2 items | 1 item | 1 character with more detail |
| Home large | Up to 4 items | Up to 2 items | Up to 2 characters |
| iPad Extra Large | Up to 8 items; two columns of four. | Up to 4 items; two columns of two. | Up to 4 characters; two-by-two detail groups. |
| Applicable Extra Large Portrait | Same upper target, adapted to available geometry rather than rotating a fixed canvas. | Same target with natural text wrapping. | Same target with reflow for available width. |
| Lock rectangular | 1 concise item, fields adapted to fit. | 1 concise item, fields adapted to fit. | 1 character, fields adapted to fit. |
| Lock circular | 1 short complete term if readable; otherwise retain configuration and show a concise app-opening cue. | An entire sentence is usually unsuitable; show a concise app-opening cue if it cannot fit. | 1 complete character; add no unreadable detail. |
| Lock inline | 1 complete short Japanese item; ruby/meaning may be omitted if needed. | 1 complete short sentence only if readable, otherwise an app-opening cue. | 1 character with a brief meaning if it fits. |

Field order is Japanese with ruby when enabled/space permits, then meaning, then optional Kanji On/Kun/word/sentence detail; Hán-Việt appears only in Vietnamese. Keep complete Japanese/reading segments; remove optional fields/items before shrinking or showing a misleading fragment. If no complete target can fit a compact family, its app-opening cue is a rendering fallback, not a different content source or a claim that the source is empty.

DS-U-39/41 approves the Home counts, concise Lock Screen content and two-column Extra Large design. Counts are ceilings. Randomly sample distinct target IDs within one entry; a smaller pool/layout can show fewer items. Repetition between different timeline entries is compatible with random selection; do not turn this into spaced repetition or a no-repeat-history feature.

A sentence-pattern target displays one complete reviewed corresponding example, as in the approved visual review. Random selection chooses eligible pattern IDs; the example for that target follows the shared learned-aware candidate contract, including target exceptions/fallback. This does not add an inline TTS button or change favorites eligibility.

Extra Large uses the additional space for readable Japanese, meaning and optional contextual reading/detail. It is not a dashboard and adds no controls, progress, scores, new source mode or mixed-content setting. One configured content type/source remains the selection contract.

DS-U-45 limits optional Sino-Vietnamese detail to Vietnamese. DS-U-47/48 defers dedicated Accessibility support while explicitly retaining system text sizing and readability/count reduction. Other languages keep Japanese/meaning and available On/Kun/examples without a Sino-Vietnamese field.

## Shared preferences

Follow shared language/furigana. Native widget rendering mode/surface appearance remains the authority for full-color/tinted/Lock Screen treatment; apply approved semantic colors where supported rather than forcing app Light/Dark over system presentation. No per-widget language/furigana/appearance override is introduced.

## Configuration and source bindings

Use native widget editing for content type and learned/favorites source. No implicit substitute/default source is chosen: an unconfigured instance shows concise configuration guidance, and a configured empty pool shows its distinct empty-source message. Tapping either still opens the app, which follows its normal level/entry contract.

The in-app level picker does not silently replace the widget's eligible pool. Evaluate the committed learned prefixes and explicit milestones of each referenced level; expand favorited parents only within the chosen content type. Publish consistent revisions after committed writes. Native rendering uses the requested family and available geometry, not copied HTML dimensions.

## Platform and evidence limits

Verify actual family eligibility in the selected SDK and on applicable devices, including any extra-large variant. A name/declaration in existing discovery notes is not proof of gallery availability or a readable snapshot. HTML approximations do not establish WidgetKit rendering, timelines, accessibility or system refresh behavior.

Read-only inspection of the selected iOS 27.2 WidgetKit Swift interface found `systemExtraLarge` and `systemExtraLargePortrait` declarations. This is declaration evidence only; no focused widget compilation, iPad gallery or actual snapshot has been verified. The HTML review illustrates both approved layouts without claiming physical family dimensions.

[Apple widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets) informs readability and information density. Numerical targets are owner-approved ProjectBeta design values, not Apple-mandated values. The existing all-applicable-size scope and compact rendering matrix remain binding; platform eligibility and native snapshots are verified under T06/T07.
