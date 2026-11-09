# Japanese reference inventory

As of 2026-11-06. This inventory records the six owner-provided PDFs and their navigational structure. It supports the approved reference-authoring approach in [B-U-03/04/15/18/41/48/50](../01-discovery-and-open-questions.md); it does not change product behavior or define the app content model.

## Use the index

- [Lessons 1–50](lesson-index.md): main text, translation/grammar and associated Kanji units.
- [Kanji units 1–50](kanji-index.md): page ranges and publisher lesson milestones.
- [Machine-readable catalog](catalog.json): source checksums, inclusive ranges, relationships and source findings.
- [OCR pilot for lessons 1 and 26](ocr-pilot/README.md): raw outputs, sampled corrections and extraction recommendation.
- [Start-page checks](heading-verification.json): 150 expected lesson/unit headings and recognized source headers.

## Source inventory

N5/N4 below are filename labels. Covers/title pages identify Minna no Nihongo Elementary I/II, 2nd edition. These reference counts do not classify every item into a JLPT level or set the final count of independently authored app items.

| Source ID | PDF | Pages | Main reference scope |
| --- | --- | --- | --- |
| N5_MAIN | [ Minna no Nihongo - N5.pdf](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=1) | 265 | Lessons 1–25 |
| N5_GRAMMAR | [Bản dịch và giải thích ngữ pháp - N5.pdf](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=1) | 201 | Lessons 1–25 |
| N5_KANJI | [Sách Kanji bài học - N5.pdf](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=1) | 218 | Units 1–20; 220 introduced characters |
| N4_MAIN | [Sách giáo khoa - Minna no Nihongo - N4.pdf](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=1) | 330 | Lessons 26–50; answer/script booklet |
| N4_GRAMMAR | [Bản dịch và giải thích ngữ pháp - N4.pdf](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=1) | 181 | Lessons 26–50 |
| N4_KANJI | [Sách Kanji bài học - N4.pdf](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=1) | 256 | Units 21–50; 316 additional characters |

Total: **1,451 PDF pages, 50 lesson chapters, 50 Kanji units**. Original PDFs are unchanged and remain development-time references outside the app resource tree.

## Page conventions and checks

PDF positions include covers and blanks. Printed numbers belong to the book and can restart in appendices. All range ends are inclusive. `body_printed_to_pdf_offset` applies only to the numbered main body; use the explicit location for each appendix.

All 150 chapter/unit starting positions matched their expected source headings. Table-of-contents starts, body pagination and intervening review boundaries were cross-checked. Source hashes are in `catalog.json`. Earlier full-page overview/pagination audits found no missing lesson; no sentence-level editorial approval is claimed. OCR confidence values are engine outputs, not measured correctness.

## Findings to preserve

| ID | Source location | Finding | Handling |
| --- | --- | --- | --- |
| REF-Q01 | N5_MAIN PDF 210, expected printed 194 | Visible label is `94`. | Keep PDF position 210; record expected printed 194. |
| REF-Q02 | N4_GRAMMAR PDF 12, printed xi | Dark scan noise obscures some learning-flow diagram labels. | Consult N4_MAIN PDF 11 for the corresponding guide diagram. |
| REF-Q03 | N4_MAIN PDFs 2 and 330 | Exact duplicate blank images. | Exclude front/end blanks from extraction. |
| REF-Q04 | Main and Kanji books | No usable body text layer. | OCR candidates need source-image checking. |
| REF-Q05 | Translation/grammar books | Existing text layers have recognition errors. | Do not use as transcription ground truth. |

Near-blank pages recorded during the source audit: N5 grammar PDF 201; N5 Kanji PDFs 17, 19, 29, 41, 43, 115, 153, 177, 179, 211, 217; N5 main PDF 244; N4 grammar PDF 179; N4 Kanji PDFs 2, 146, 180, 184, 256; N4 main PDFs 2, 268, 272, 330. Their section context did not indicate a missing lesson.

## Other source sections

This table intentionally separates review, reference, quizzes and answers from lesson/unit body ranges. Unnumbered covers, blanks, imprints and some front-matter pages are not indexed as learning content.

| Source | Section | Role | PDF pages | Printed pages |
| --- | --- | --- | --- | --- |
| N5_MAIN | Review A | review | [46–47](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=46) | 30–31 |
| N5_MAIN | Review B | review | [80–81](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=80) | 64–65 |
| N5_MAIN | Review C | review | [122–123](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=122) | 106–107 |
| N5_MAIN | Review D | review | [158–159](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=158) | 142–143 |
| N5_MAIN | Review E | review | [184–185](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=184) | 168–169 |
| N5_MAIN | Review F | review | [210–211](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=210) | 194–195 |
| N5_MAIN | Review G | review | [236–237](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=236) | 220–221 |
| N5_MAIN | Adverbs/conjunctions/conversation expressions I | reference | [124–125](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=124) | 108–109 |
| N5_MAIN | Adverbs/conjunctions/conversation expressions II | reference | [238–241](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=238) | 222–225 |
| N5_MAIN | General review | review | [242–243](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=242) | 226–227 |
| N5_MAIN | Verb forms | reference | [245](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=245) | 229 |
| N5_MAIN | Learning item list | reference | [246–249](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=246) | 230–233 |
| N5_MAIN | Index | reference | [250–265](../%20Minna%20no%20Nihongo%20-%20N5.pdf#page=250) | 234–249 |
| N4_MAIN | Review H | review | [62–63](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=62) | 42–43 |
| N4_MAIN | Review I | review | [104–105](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=104) | 84–85 |
| N4_MAIN | Review J | review | [148–149](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=148) | 128–129 |
| N4_MAIN | Review K | review | [190–191](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=190) | 170–171 |
| N4_MAIN | Review L | review | [232–233](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=232) | 212–213 |
| N4_MAIN | Adverbs/conjunctions/conversation expressions I | reference | [106–107](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=106) | 86–87 |
| N4_MAIN | Adverbs/conjunctions/conversation expressions II | reference | [234–235](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=234) | 214–215 |
| N4_MAIN | General review | review | [236–241](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=236) | 216–221 |
| N4_MAIN | Verb forms | reference | [242–243](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=242) | 222–223 |
| N4_MAIN | Learning item list | reference | [244–247](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=244) | 224–227 |
| N4_MAIN | Index | reference | [248–267](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=248) | 228–247 |
| N4_MAIN | Exercise B/C answer examples | answer_examples | [273–297](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=273) | 1–25 |
| N4_MAIN | Problem audio scripts and answers | transcripts_and_answers | [298–326](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=298) | 26–54 |
| N4_MAIN | Review/general-review answer examples | answer_examples | [327–329](../Sa%CC%81ch%20gia%CC%81o%20khoa%20-%20Minna%20no%20Nihongo%20-%20N4.pdf#page=327) | 55–57 |
| N5_GRAMMAR | Topic/subject and clause reference columns | reference | [179–182](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=179) | 160–163 |
| N5_GRAMMAR | Appendices: numbers, time, counters, verb conjugation | reference | [183–200](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=183) | 164–181 |
| N4_GRAMMAR | Elementary I grammar/reference overview | reference | [23–26](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=23) | 2–5 |
| N5_KANJI | Kanji introduction | primer | [20–27](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=20) | 3–10 |
| N5_KANJI | Preparatory activities | primer | [30–40](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=30) | 13–23 |
| N5_KANJI | Kanji Ninja 1 | review | [64–67](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=64) | 47–50 |
| N5_KANJI | Kanji Ninja 2 | review | [88–91](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=88) | 71–74 |
| N5_KANJI | Kanji Ninja 3 | review | [112–114](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=112) | 95–97 |
| N5_KANJI | Kanji Ninja 4 | review | [136–151](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=136) | 119–134 |
| N5_KANJI | Kanji Ninja answers | answers | [152](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=152) | 135 |
| N5_KANJI | Unit quizzes | quiz | [154–173](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=154) | 137–156 |
| N5_KANJI | Quiz answers | answers | [174–176](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=174) | 157–159 |
| N5_KANJI | Kanji/word reference entries | reference | [181–210](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=181) | 2–31 |
| N5_KANJI | Word index | reference | [212–216](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N5.pdf#page=212) | 33–37 |
| N4_KANJI | Supplement to Unit 25 | supplement | [34](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=34) | 16 |
| N4_KANJI | Review 1 | review | [56–57](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=56) | 38–39 |
| N4_KANJI | Review 2 | review | [78–79](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=78) | 60–61 |
| N4_KANJI | Review 3 | review | [100–101](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=100) | 82–83 |
| N4_KANJI | Review 4 | review | [122–123](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=122) | 104–105 |
| N4_KANJI | Review 5 | review | [144–145](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=144) | 126–127 |
| N4_KANJI | Unit quizzes 23–50 | quiz | [147–174](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=147) | 129–156 |
| N4_KANJI | Quiz answers | answers | [175–179](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=175) | 157–161 |
| N4_KANJI | Kanji/word reference entries | reference | [186–237](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=186) | 4–55 |
| N4_KANJI | Word index | reference | [238–247](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=238) | 56–65 |
| N4_KANJI | Radical index | reference | [248–253](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=248) | 66–71 |
| N4_KANJI | Character list | reference | [254–255](../Sa%CC%81ch%20Kanji%20ba%CC%80i%20ho%CC%A3c%20-%20N4.pdf#page=254) | 72–73 |

## Next authoring step

The OCR pilot supports assisted extraction with page/region provenance and manual Japanese/annotation review. The initial lesson 1/26 samples and subsequent 50-lesson/50-unit Vietnamese/English authoring batch are now recorded in [content authoring](../content-authoring/README.md). Keep raw source transcription separate from independently authored release explanations, examples, dialogues and translations. B-U-58 confirms separate learned prefixes per level. Learned-source Kanji eligibility evaluates the level of the milestone's referenced lesson, rather than inferring it from the Kanji unit's filename level: units 21–25 retain their N5 lesson 25 milestone even though their source volume is labeled N4. This eligibility condition does not restrict browsing or change the favorites source.
