> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Learned-aware sentence examples

Status: **NORMATIVE DESIGN CONTRACT v1.0.** Product rules are confirmed. The deterministic bindings below implement the approved priority; candidate-bank authoring and runtime evidence remain separate work.

## Confirmed requirement

Authority: DS-U-22/26–30/32–34 and B-U-20/40/58.

- Apply learned-aware selection to sentence-example surfaces throughout the app, including vocabulary, grammar, sentence patterns and Kanji.
- Exclude the alphabet area: use the most basic suitable words/sentences regardless of learned-prefix state. This is not a lesson-locking rule or a new alphabet learned-state model.
- Independently author and review the sentence candidates in advance; bundle them with contextual readings and translations for offline use.
- At runtime, select/order reviewed candidates; do not generate/rewrite sentences or add a runtime AI/API/content-server dependency.
- AI content authoring is a possible future direction only. Existing development-time authoring approvals remain distinct from an in-app AI feature.
- Keep dialogue scripts unchanged: neither select alternate dialogue versions nor replace/reorder their individual turns. Apply learned-aware selection to accompanying example sentences.

## Familiarity and fallback

Familiarity derives from the union of vocabulary/grammar taught in lessons actually marked learned in either N5 or N4. Each level retains its independent prefix. Selecting N4 does not mean N5 is learned, and marking N4 never changes N5 state. Do not introduce scores, inferred mastery or a Kanji-specific learned marker.

Permit the target character/word or grammar point currently being taught to be new. Prefer candidates whose supporting vocabulary and grammar are already learned. If none exists, still show the simplest corresponding sentence rather than suppressing the example.

DS-U-33 confirms this priority order among matching candidates: learned supporting grammar first, then fewer unfamiliar words, then simpler/shorter sentences. Implement as ordered criteria, not a weighted mastery score: fewer distinct unfamiliar supporting grammar references, fewer distinct unfamiliar supporting vocabulary references, then reviewed editorial simplicity order, Japanese sentence length and stable authored order/ID. The explicit teaching target is excluded from its corresponding unfamiliar-dependency count. Editorial simplicity order is content metadata to author/review, not an invented learner score.

Target correspondence is required in both preferred and fallback candidates. Simplicity must not justify an unrelated sentence or one that fails to demonstrate the intended meaning/grammar. Translation and pronunciation must belong to the selected sentence, not to a discarded candidate.

Only the explicit grammar point being taught is exempt; do not exempt unrelated grammar dependencies. Render fallback sentences with the same normal Japanese/translation treatment. No new unknown-word badge or mastery indicator is required; the owner selected the simplest fallback, not another learning-status feature.

## Source content and authoring boundary

- Character-set entries such as 日 currently provide meanings, On/Kun, Sino-Vietnamese and examples such as 日曜日, 今日 and 毎日. These are words/compounds, not the required sentence-candidate bank.
- Unit word examples likewise provide contextual readings and meanings, not a learned-aware sentence bank.
- Original lesson sentences retain stable IDs, pattern references and grammar-point IDs. H04 supplies complete vocabulary/form/sense and supporting-grammar analysis in a revision-bound sidecar.
- The source format and H04 sidecar are editorial assets, not app runtime integration. The H04 validation report establishes its authoring coverage; a design requirement alone cannot prove it.

Sources: [N5 character set](../content-authoring/kanji/characters-n5.json), [unit 1](../content-authoring/kanji/unit-01.json), [lesson 1](../content-authoring/lesson-01.json), [authoring schema](../content-authoring/authoring.schema.json).

## Confirmed content approach and integration boundary

Prepare an independently authored, reviewed sentence bank bundled offline with the app. Select/order candidates against the actual persisted learned-prefix state. The display cap/ranking contract is specified here; this design work does not establish bank/dependency completeness.

Candidate evidence should include stable sentence/target IDs, Japanese with reviewed contextual readings, translations, vocabulary/form dependencies, grammar dependencies, explicit lesson/level links and editorial review status. Do not infer “all vocabulary learned” from grammar IDs alone or from an unreviewed character/substring match. Inflected forms can introduce grammatical dependencies beyond knowing a dictionary word.

## Selection flow with explicit open stages

1. Resolve reviewed candidates for the target and the actual persisted learned-prefix snapshot.
2. Evaluate supporting dependencies against actually marked lessons in both levels, retaining explicit target-character/word/grammar exceptions.
3. Prefer matching candidates under the confirmed order: learned supporting grammar, fewer unfamiliar words, then simpler/shorter sentences.
4. If no fully familiar-supporting-language candidate exists, still show the best corresponding reviewed candidate under the same confirmed familiarity/simplicity order. “Simplest” does not discard the owner's grammar-first preference in favor of raw text length alone.
5. Display matching Japanese, ruby, translation and pronunciation for at most three sentences total per target. DS-U-40 removes the earlier “more” proposal: there is no expansion, pagination or load-more action for examples.
6. Select from the latest successfully persisted learned state when the page opens. Keep visible/speaking examples stable while the page stays open; do not automatically replace them after a learned-state change.

## Implementation bindings and dependencies

| Area | Binding / remaining evidence |
| --- | --- |
| Ranking detail | Use the ordered criteria above with reviewed dependency/simplicity metadata. The bank must supply them; do not infer completeness from string matching. |
| Search/language | Explicit search opens its referenced sentence within the three-sentence cap. Language changes retain its Japanese ID and resolve the matching translation. Read implementation-guide.md. |
| Display | Show at most three actual reviewed matching candidates, in order, without duplicated/padded examples or expansion. A shorter available list is valid. |
| Empty bank | Missing/corrupt candidates use the approved scoped content-unavailable/retry state. Do not substitute unrelated content or claim a dependency-complete bank exists. |

Do not introduce numeric familiarity weights, hidden mastery scores, inferred learning or random ordering without an approved selection policy. Dialogue scripts remain fixed under DS-U-34. Load candidate/dependency data on demand and keep selection work bounded under [DS-U-31 performance constraints](performance-and-footprint.md).

## Future acceptance evidence

Verify target correspondence, complete dependency coverage, deterministic ordering/fallback, independent level state and mark/unmark updates. Test N5-only, N4-only, both-level and no-learned-lesson states, without inferring N5 familiarity in N4-only cases. Verify the taught-target exception, usable unfamiliar-support fallback, basic kana examples, the display cap and fixed dialogues. Cancellation/save failure cannot expose unsaved learned state. Test visible-example stability, matching translations/audio and exact search navigation under the final contracts.

The original design round did not establish authoring or native acceptance. The H04 handoff below now records complete primary authoring review. Runtime/native verification remains separate, and HTML lesson excerpts remain static samples.


## H04 complete authoring inventory — 2026-11-08

The canonical [sentence bank](../content-authoring/sentence-bank/README.md) contains 3,275 primary-reviewed complete candidates covering all 6,126 exact targets: 2,731 vocabulary forms/senses,255 grammar points,280 pattern variants,536 characters and 2,324 Kanji lexical occurrences. All 304 original examples retain their source identity, Japanese, translation and context; all 50 dialogue objects remain unchanged. No substring or homonymous reading certifies correspondence.

Every candidate has complete lexical/form/sense spans, supporting grammar, exact target exceptions and editorial simplicity. Character examples require a reviewed lexical binding, a source-curated master-example UUID relation and the displayed character. The 122 reviewed bare-character pairs allow only the actual taught bare meaning to be new, not a compound or another same-glyph sense. Context-only support is unintroduced and stays unfamiliar. The 60 reviewed repeated-lexeme groups share actual introductions without merging IDs or level prefixes.

The offline Python oracle checks none/N5-only/N4-only/both prefixes, grammar-first ranking, target exceptions, unfamiliar-support fallback, stable order/snapshot, the total-three cap and forced search inclusion. It suppresses duplicate written/spoken examples and identical spoken VI/EN content with alternate orthography, while preserving distinct contextual readings such as 一日 (いちにち / ついたち). Deduplication cannot create target matches. The exact form/sense speech resolver rejects wrong pairs, missing contexts and stale source/context revisions.

The full `--complete --self-test --check` gate passes with 27 rejected invalid fixtures and 24 reference checks. Inspect the [generated inventory](../content-authoring/sentence-bank/inventory.md), [primary review](../content-authoring/sentence-bank/review.json) and [revision-bound report](../content-authoring/sentence-bank/validation-report.json). T04.05 owns native selector/visible snapshots; T01 owns ruby/playback and voice evidence. No application/device, independent-human, remaining-locales or release acceptance follows from these authoring checks.
