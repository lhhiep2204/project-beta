# Editorial review: lessons 1 and 26

Historical initial-sample review (2026-11-06). Counts and fingerprints below describe that snapshot; later batch additions and generated readable pages are outside those historical fingerprints. Current content is browsable in the [content index](content-index.md).


Review date: 2026-11-06. **Self-review accepted for batch authoring under B-U-51.** The owner initially offered to review, then explicitly delegated this gate to the primary agent. The two samples and ER-01 through ER-08 are accepted for further authoring as of 2026-11-07. This is primary-agent self-review; no independent human certification or release pass is asserted.

Read [Lesson 1](lesson-01.md) and [Lesson 26](lesson-26.md). Full IDs, before/after fields, evidence and version fingerprints are in the [item-level review record](editorial-review.json).

## Scope and result

The primary review covered 83 vocabulary entries, 12 grammar points, 12 templates, 24 examples and two dialogues (17 turns). Nine source pages were visually rechecked. Eight bounded findings were addressed; they are clarifications and translation refinements, not a claim that eight Japanese sentences were erroneous. All Japanese sentences, lexical forms, readings, verb groups and opaque item IDs were preserved. Eight examples now have separate bilingual context.

The editorial draft schema now permits optional bilingual `context` on examples. Context is situational guidance, separate from the spoken Japanese sentence and its translation; both language values must be nonblank when present. This does not select an app runtime contract. The [validator result](validation-report.json) records 14 rejected negative fixtures, 12 source anchors and six matching source PDF checksums.

## Changes for owner review

### ER-01: teaching clarification

Both noun-negative variants remain polite. Distinguish spoken contraction from a misleading polite-versus-impolite contrast.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 1 / noun_negative / notes | VI: Không đặt thêm です sau ありません trong mẫu này. Trong では, trợ từ は vẫn đọc là わ. / EN: Do not add です after ありません in this pattern. In では, the particle は is still pronounced わ. | VI: Cả じゃありません và ではありません đều là cách nói lịch sự; じゃ là dạng rút gọn thường gặp trong hội thoại. Không thêm です sau ありません. Trong では, trợ từ は vẫn đọc là わ. / EN: Both じゃありません and ではありません are polite forms; じゃ is a contraction common in conversation. Do not add です after ありません. In では, the particle は is still pronounced わ. |

Evidence: [PDF-N5-33](#pdf-n5-33), [TUFS-NOUN](#tufs-noun). Batch gate: accepted by primary self-review under B-U-51.

### ER-02: register clarification

The readable list flattened the register distinction even though JSON form metadata retained it. Make the contrast explicit for review.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 1 / person_over_there / usage | VI:  / EN:  | VI: あの方 là cách nói lịch sự hơn あの人 khi nhắc đến người kia. / EN: あの方 is a more polite way to refer to that person than あの人. |
| 1 / who / usage | VI:  / EN:  | VI: どなた là cách hỏi lịch sự hơn だれ. / EN: どなた is a more polite alternative to だれ. |

Evidence: [PDF-N5-29](#pdf-n5-29). Batch gate: accepted by primary self-review under B-U-51.

### ER-03: missing context

The affiliation example names Aoi without establishing that it is a company. Supply context outside the Japanese sentence.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 1 / fictional_company / context | (not provided) | VI: Trong ví dụ hư cấu này, Aoi là tên một công ty. / EN: In this fictional example, Aoi is the name of a company. |

Evidence: [PDF-N5-34](#pdf-n5-34). Batch gate: accepted by primary self-review under B-U-51.

### ER-04: missing context

The explanatory statement/question examples lacked the shared observation or prior question that motivates んです. They are not isolated neutral announcements.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 26 / explain_unwell / context | (not provided) | VI: Một người thấy bạn có vẻ mệt và hỏi bạn bị sao; bạn giải thích tình trạng của mình. / EN: Someone notices that you look unwell and asks what is wrong; you explain your condition. |
| 26 / explain_day_off / context | (not provided) | VI: Một người ngạc nhiên vì hôm nay bạn không đi làm; bạn giải thích rằng mình được nghỉ. / EN: Someone is surprised that you are not at work today; you explain that it is your day off. |
| 26 / where_wallet_found / context | (not provided) | VI: Người đối thoại vừa nói đã nhặt được một chiếc ví; bạn hỏi thêm nơi họ nhặt được. / EN: The other person has just said they picked up a wallet; you ask where they found it. |
| 26 / late_sports_day / context | (not provided) | VI: Bạn biết người đối thoại đã đến hội thi thể thao muộn và muốn hỏi lý do. / EN: You know the other person arrived late for the sports day and ask why. |

Evidence: [PDF-N4-33](#pdf-n4-33), [JF-NDESU](#jf-ndesu). Batch gate: accepted by primary self-review under B-U-51.

### ER-05: translation alignment

The English translation assumed form-filling while Vietnamese only said writing. Establish a form-filling context and align both translations. The Japanese sentence is unchanged.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 26 / explain_form / context | (not provided) | VI: Bạn đang điền một mẫu giấy nhưng chưa biết phải viết thông tin vào đâu. / EN: You are completing a form and do not know where to write the information. |
| 26 / explain_form / translation | VI: Anh/chị có thể chỉ giúp tôi cách viết được không? / EN: Could you show me how to fill this in? | VI: Anh/chị có thể chỉ giúp tôi cách điền mẫu này được không? / EN: Could you show me how to fill this in? |

Evidence: [PDF-N4-34](#pdf-n4-34), [JF-REQUEST](#jf-request). Batch gate: accepted by primary self-review under B-U-51.

### ER-06: translation precision

In the rubbish-collection context, 出す means putting items out for collection. Make this more precise than simply placing bottles somewhere. No actual collection rule is supplied.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 26 / put_out / meanings | [{"form_keys": ["standard"], "text": {"en": "put out, here with rubbish", "vi": "đổ; đưa ra, trong ngữ cảnh đổ rác"}}] | [{"form_keys": ["standard"], "text": {"en": "put out for collection, here with rubbish", "vi": "đem ra để thu gom, trong ngữ cảnh rác"}}] |
| 26 / where_bottle / context | (not provided) | VI: Bạn hỏi về chỗ đem chai ra thu gom tại một địa điểm hư cấu. / EN: You ask where to put bottles out for collection at a fictional location. |
| 26 / where_bottle / translation | VI: Tôi nên để chai ở đâu? / EN: Where should I put out the bottles? | VI: Tôi nên đem chai ra chỗ nào để thu gom? / EN: Where should I put out the bottles for collection? |

Evidence: [PDF-N4-30](#pdf-n4-30). Batch gate: accepted by primary self-review under B-U-51.

### ER-07: reading scope clarification

The bound-form reading 〜がいしゃ should not imply that the standalone word 会社 is read がいしゃ. Preserve the printed bound form and explain the scope.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 26 / company_suffix / usage | VI:  / EN:  | VI: Cách đọc 〜がいしゃ ở đây là dạng ghép, như ガス会社（ガスがいしゃ）. Từ 会社 đứng riêng đọc là かいしゃ. / EN: The reading 〜がいしゃ here is a compound form, as in ガス会社（ガスがいしゃ）. The standalone word 会社 is read かいしゃ. |

Evidence: [PDF-N4-30](#pdf-n4-30). Batch gate: accepted by primary self-review under B-U-51.

### ER-08: missing context

The short は example needs an established topic so its translation does not imply an unexplained contrast.

| Lesson / item / field | Before | After |
| --- | --- | --- |
| 26 / volunteering_topic / context | (not provided) | VI: Sau khi nói về các hoạt động khác, người đối thoại chuyển sang hỏi về hoạt động tình nguyện. / EN: After discussing other activities, the other person turns to volunteering. |

Evidence: [PDF-N4-34](#pdf-n4-34), [TUFS-PARTICLES](#tufs-particles). Batch gate: accepted by primary self-review under B-U-51.

## Delegated self-review checklist

- [x] OR-01: Confirm vocabulary forms, meanings, readings and verb groups in both lessons.
- [x] OR-02: Confirm grammar, register, pattern variants and ER-01 through ER-08.
- [x] OR-03: Check the naturalness and meaning equivalence of all examples and dialogue turns in Japanese, Vietnamese and English.
- [x] OR-04: Confirm each added context supports the intended usage and is not part of the Japanese utterance.
- [x] OR-05: Approve each sample or identify corrections by lesson and editorial key.

The checklist was completed by the primary agent under the owner’s explicit delegation. Concrete new uncertainties will be confirmed with the owner. Acceptance applies to the pinned revision and the authoring gate only.

## Evidence consulted

The owner PDFs remain the authority for lesson/unit boundaries and listed readings. External teaching references corroborate grammar facts only. All entries below were inspected on 2026-11-06; example/dialogue wording remains newly authored.

<a id="pdf-n5-29"></a>

- **PDF-N5-29**: [N5_GRAMMAR PDF 29, printed 10](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=29). Primary visual comparison.

<a id="pdf-n5-30"></a>

- **PDF-N5-30**: [N5_GRAMMAR PDF 30, printed 11](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=30). Primary visual comparison.

<a id="pdf-n5-32"></a>

- **PDF-N5-32**: [N5_GRAMMAR PDF 32, printed 13](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=32). Primary visual comparison.

<a id="pdf-n5-33"></a>

- **PDF-N5-33**: [N5_GRAMMAR PDF 33, printed 14](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=33). Primary visual comparison.

<a id="pdf-n5-34"></a>

- **PDF-N5-34**: [N5_GRAMMAR PDF 34, printed 15](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N5.pdf#page=34). Primary visual comparison.

<a id="pdf-n4-29"></a>

- **PDF-N4-29**: [N4_GRAMMAR PDF 29, printed 8](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=29). Primary visual comparison.

<a id="pdf-n4-30"></a>

- **PDF-N4-30**: [N4_GRAMMAR PDF 30, printed 9](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=30). Primary visual comparison.

<a id="pdf-n4-33"></a>

- **PDF-N4-33**: [N4_GRAMMAR PDF 33, printed 12](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=33). Primary visual comparison.

<a id="pdf-n4-34"></a>

- **PDF-N4-34**: [N4_GRAMMAR PDF 34, printed 13](../Ba%CC%89n%20di%CC%A3ch%20va%CC%80%20gia%CC%89i%20thi%CC%81ch%20ngu%CC%9B%CC%83%20pha%CC%81p%20-%20N4.pdf#page=34). Primary visual comparison.

<a id="tufs-noun"></a>

- **TUFS-NOUN**: [TUFS: noun predicates and negatives](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/001.html). Both nominal forms are polite; じゃ is common in speech.

<a id="tufs-topic"></a>

- **TUFS-TOPIC**: [TUFS: noun topic sentences](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/002.html). Topic-particle pronunciation and respectful name suffix usage.

<a id="tufs-particles"></a>

- **TUFS-PARTICLES**: [TUFS: topic and additive particles](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/095.html). Topic/contrast and additive も in the selected examples.

<a id="jf-ndesu"></a>

- **JF-NDESU**: [Japan Foundation: んです (BTS00120)](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00120/ja/render.do). Context-sensitive explanatory uses, questions, prefacing requests and the noun/na-adjective link.

<a id="jf-request"></a>

- **JF-REQUEST**: [Japan Foundation: ていただけませんか (BMA00096)](https://www.kyozai.jpf.go.jp/kyozai/material/BMA00096/ja/render.do). Polite requests for a beneficial action performed by the listener.

## Revision fingerprints

The [JSON record](editorial-review.json) pins all reviewed lesson JSON/Markdown, the schema, source anchors, validator and validation output with SHA-256. New content invalidates approval of affected files.

| File | SHA-256 |
| --- | --- |
| docs/content-authoring/lesson-01.json | `9a6e08476d7671606f61e351e1483937e104bed59f5845afd49ccb592bca4d2d` |
| docs/content-authoring/lesson-01.md | `b8c1156e284a4ff983f9686b8260e13cccf600859ca92cf42bbef0014eaad3ff` |
| docs/content-authoring/lesson-26.json | `64232f79db3a1c53371be6f18ac20accae6146a827830494f7ced9aa77548f04` |
| docs/content-authoring/lesson-26.md | `71c64c4e1ae676a59c990325d6f68a3d8be41e804e6580b2b3a2f6c3dccee77e` |
| docs/content-authoring/authoring.schema.json | `1cca2bc488541714d1d5a00e2d79a310304de9eb8b5fe1c6574b29d49b0c00f1` |
| docs/content-authoring/source-checks.json | `24e8cf2eb7bd83feaad6cd54f5b8bbc071a2323df34c4f0cfb14229834ca9575` |
| docs/content-authoring/validation-report.json | `dea9f871ccf5f364346e06612f9aecd5da4267f5e1acc5ae5bffcdfddeb6515e` |
| scripts/validate_authoring_samples.py | `a6e4e36c36fb7aacb640f3a07e357b5ed044806cc8fc722388cbdaa7a8a409fd` |

## Remaining evidence

The delegated authoring gate is accepted for these two samples; independent human and release acceptance remain unclaimed. English/Vietnamese are the only authored languages; the other 17 remain missing. These are bounded samples, not complete lessons or the full curriculum. Actual voice pronunciation and app rendering remain unverified. The owner separately authorized batch authoring under B-U-51/52/53; no release pass follows from this review packet.
