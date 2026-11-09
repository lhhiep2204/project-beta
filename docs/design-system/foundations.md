> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Visual foundations

Status: **NORMATIVE DESIGN VALUES — DS-U-37/41.** System fonts, Dynamic Type, Teal, balanced density, content-specific typography and the authored color/geometry values below are approved. Read tokens.json for the machine-readable contract. Native implementation verification remains required; dedicated Accessibility scope follows the override below.

**Phase scope — DS-U-47/48/49:** retain system text sizing and RTL/localization. VoiceOver/specialized Accessibility adaptation and its acceptance are deferred; future specialist references below are not current delivery gates.

## Typography roles

Use the system font family selected for the script/locale and semantic text style. Do not bundle SF fonts, force Latin glyph metrics onto Japanese, or use fixed production text sizes. Reference values below describe a standard-size iOS sample; the system and content layout determine actual scaled metrics.

| Role | System style / weight | Reference size | Use |
| --- | --- | --- | --- |
| Screen/topic title | Large title / bold | 34 pt | Top-level title and lesson topic. |
| Content section | Title 2 / semibold | 22 pt | Vocabulary, grammar, patterns, dialogue. |
| Item/grammar heading | Headline / semibold | 17 pt | Short headings; wraps when necessary. |
| Japanese word | Title 2 / regular | 22 pt | Main vocabulary and word-example form. |
| Japanese sentence/dialogue | Title 3 / regular | 20 pt | Complete examples and dialogue turns. |
| Meaning/explanation | Body / regular | 17 pt | Translations and prose explanations. |
| Guidance | Subheadline / regular | 15 pt | Supporting usage notes. |
| Metadata | Footnote / regular | 13 pt | Level, lesson association and speaker label. |
| Ruby | System regular, scales with associated Japanese text | 11 pt at 20–22 pt base | Contextual reading above Kanji. Never a fixed unscaled overlay. |
| Kanji detail glyph | System regular, scales with content text | 64 pt reference | One selected character, with no forced size that crowds meaning/actions. |

The typography roles implement the owner's requested size/weight hierarchy. Do not introduce a separate content-size preference or suppress accessibility sizes. At large sizes reflow actions/columns and grow rows rather than reducing Japanese type or clipping translations. Ruby must remain associated with its base segment across wrapping and mixed punctuation; no fake whitespace alignment.

System styles are the implementation authority for standard text, not the reference numbers. Ruby and a prominent Kanji glyph may need a relative/scaled system-font treatment supported by the verified renderer. A browser scale slider is a review affordance only.

## Semantic colors

Use native semantic background, grouped surface, primary/secondary label, separator and error colors. Do not freeze their browser approximation hex values into the native UI. Teal is an authored adaptive accent, not a claim that these are Apple's system-teal values.

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| Accent / interactive label | `#007C78` | `#64D8CB` | Selected navigation and primary interactive content. |
| On-accent label | `#FFFFFF` | `#000000` | Content over the opaque accent fill. |
| Increased-contrast accent | `#005E5A` | `#94F0E3` | Adaptive accessibility variant; verify on native surfaces. |
| Primary content / background / secondary content / separator | Native semantic roles | Native semantic roles | Readable reading surfaces and hierarchy. |
| Playing turn fill | Subtle Teal tint over semantic content surface | Subtle Teal tint over semantic content surface | Pair with wave glyph/playing marker, never color alone. |

Do not use Teal for every word, all Kanji readings or every metadata label. Keep Japanese and translations in readable semantic foreground roles. Validate contrast on actual surfaces, materials and rendering modes; opaque-pair calculations alone do not establish native accessibility.

## Geometry for balanced density

| Token/role | Approved value/rule |
| --- | --- |
| Spacing scale | 4, 8, 12, 16, 20, 24, 32, 40 pt. |
| Primary content inset | 20 pt in a compact reading view; native safe-area/list margins take precedence for native components. |
| Japanese-to-meaning gap | 8 pt; sufficient ruby metrics belong to Japanese layout rather than extra blank rows. |
| Content-row vertical inset | 12 pt per side, growing naturally for wrapping/large type. |
| Section separation | 32 pt; native separator/heading establishes grouping. |
| Effective action target | At least 44 × 44 pt with non-overlapping hit regions. |
| Custom grouped surface radius | 16 pt; native cards/menus/widgets retain their platform shape. |
| Controls | Native shape/metrics; use capsule or circle only where the control's native role supports it. |
| Body width on wide layouts | Readable centered column, approximately 680 pt target; allow fitting and accessibility reflow rather than forcing a fixed canvas. |

These approved geometry values do not override native navigation/widget margins or authorize fixed row heights.

## Materials and motion

Use native Liquid Glass for navigation/control layers. Keep study content on semantic readable surfaces; do not turn every vocabulary/grammar/dialogue row into a glass card. Prefer native component appearance instead of recreating blur in production. Use native platform behavior for system rendering settings; dedicated customization/acceptance for Accessibility settings is deferred under DS-U-47/48. Never layer custom glass onto already-glass native chrome without evidence of need.

Use native selection/navigation feedback. No decorative continuous sound-wave animation, confetti, learned-score celebration or automatic playback-follow movement is introduced. Icon waves indicate playback state; the app does not infer a measured audio waveform from them. Custom haptics or animation timings remain unselected.

## Evidence and references

The HTML review demonstrates approved Light/Dark/type roles and iPad Extra Large layouts with authored source examples. It approximates typography/materials; it does not verify actual Dynamic Type, contextual ruby wrapping, native accessibility, widget dimensions or SDK compilation.

- [Apple system fonts](https://developer.apple.com/documentation/technologyoverviews/fonts): locale/script-aware system typography.
- [Apple Dynamic Type](https://developer.apple.com/videos/play/wwdc2024/10074/): adapting layouts and text size.
- [Apple design tips](https://developer.apple.com/design/tips/): readable content and effective touch targets.
- [Apple materials](https://developer.apple.com/design/human-interface-guidelines/materials): content/navigation layering and accessibility-responsive materials.
