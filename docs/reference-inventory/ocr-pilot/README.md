# OCR pilot: lessons 1 and 26

This is source-extraction evidence for development. It is not independently authored app learning content.

## Scope and method

- 28 whole pages: N5_MAIN PDFs 22–29, N5_GRAMMAR PDFs 29–34, N4_MAIN PDFs 22–29, N4_GRAMMAR PDFs 29–34.
- 8 language-specific region images from the first main/vocabulary page of each lesson. Crop coordinates are in [regions.json](regions.json).
- Apple Vision accurate recognition, revision 3, language correction off, rendered at 2.5 pixels/point (180 dpi).
- Whole-page languages: `ja-JP`, `vi-VT`, `en-US`. Region passes used `ja-JP` or `vi-VT`. `vi-VT` is the exact Vietnamese token returned by the installed Vision runtime; it does not select an app locale.
- 32 purposive vocabulary-fragment spot checks and 8 additional critical Japanese/annotation checks. Expected fragments were read from the source page images by the primary agent. This is not independent linguistic review.

Recovery requires the expected fragment within a recognized line after Unicode NFKC and whitespace removal. Diacritics and Kanji remain significant. These counts are **not** whole-corpus accuracy or character error rate; they include deliberately selected successful and failed cases.

## Vocabulary fragment results

| Source sample | Language | Whole page | Language-specific region |
| --- | --- | --- | --- |
| N5, vocabulary PDF 29 | Japanese Kanji fields | 8/8 | 3/8 |
| N5, vocabulary PDF 29 | Vietnamese meanings | 0/8 | 8/8 |
| N4, vocabulary PDF 29 | Japanese Kanji fields | 8/8 | 8/8 |
| N4, vocabulary PDF 29 | Vietnamese meanings | 0/8 | 7/8 |

The region pass recovered 15/16 sampled Vietnamese fragments, while the whole-page pass recovered none with accents intact. The Japanese region pass lost several N5 fields, so it is not a uniformly better replacement. Mixed Japanese annotations inside a Vietnamese column still become garbage.

## Critical observed examples

Seven of the eight additional whole-page checks failed; the successful control was `紹介して`. These are short image-checked fragments, not a corrected full lesson.

| Source / PDF page | Expected source fragment | Observed fragment | Finding |
| --- | --- | --- | --- |
| N5_MAIN / 22 | 銀行員 | 醸料賞 | Kanji substitution in a word with furigana. |
| N5_MAIN / 22 | さくら大学 | さくら笑学 | Kanji substitution in a proper name. |
| N4_MAIN / 22 | 生け花 | 生け袋 | Kanji substitution changes the study example. |
| N4_MAIN / 22 | 習いたい | 簪いたい | Kanji substitution changes the verb. |
| N4_MAIN / 22 | 先生 | 発 | Kanji/reading separation loses the original word. |
| N4_MAIN / 22 | 紹介して | 紹介して | Control: this phrase is recovered in the whole-page pass. |
| N4_GRAMMAR / 29 | みますⅡ | みますI | Verb group II misread as group I; compare the printed Roman numeral. |
| N4_GRAMMAR / 29 | れんらくしますⅢ | れんらくします皿 | Verb group III misread as a Kanji glyph. |

The region-only Vietnamese pass also read `quốc hội` as `quồc hội` in the sampled N4 meaning. Engine confidence does not remove the need to check these errors.

## Structural result and recommendation

Raw OCR has no verified vocabulary-row alignment or Kanji-to-furigana association. Verb groups, optional variants, brackets, suffixes and asterisks require explicit review. Preserve each raw page and region result alongside its source locator; do not infer missing readings from OCR fragments alone.

**Do not directly ingest these outputs into learning content.** Use OCR as an authoring aid, check Japanese and annotations against the source images, and independently author release explanations/examples/dialogues/translations under the standing project decision. The next bounded step is a reviewed structured sample for lesson 1 and lesson 26 before batch extraction.

## Files

- [Whole-page raw OCR](whole-page-raw.jsonl): one JSON object per source page; confidence and normalized image boxes retained.
- [Japanese region raw OCR](japanese-regions-raw.jsonl) and [Vietnamese region raw OCR](vietnamese-regions-raw.jsonl).
- [Region provenance](regions.json): normalized top-left crop coordinates in the rendered source page.
- [Review data](review.json): all 40 selected checks, expected fragments, observed lines, counts and limitations.

Raw OCR boxes use normalized **bottom-left** image coordinates; region manifests use normalized **top-left** source-page coordinates. Rendered page images and OCR executables remain temporary working artifacts, rather than duplicated repository/app assets.
