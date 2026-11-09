# Agent context and maintenance

## Start here

1. Read the [documentation gate](index.html#documentation), then [delivery-plan.md](delivery-plan.md) for the next executable task and dependencies. DOC-PLAN-01 requires every documentation task to be done and synchronization/audit checks to pass before new development. The owner explicitly places translation production/review in development. DOC-PLAN-02 scheduled offline listening/real-audio verification in development; the owner later completed and attested the physical cases under DOC-PLAN-06. Preserve existing work and individual execution dependencies; phase readiness does not close implementation or release tasks.
2. Read [engineering-contract.md](engineering-contract.md) for runtime identity, ownership and data boundaries.
3. Read only the relevant [design contract](design-system/README.md).
4. For content work, use [authoring](content-authoring/README.md), [catalog](reference-inventory/catalog.json) and [audit evidence](audit/source-audit.json).

The single owner review is [index.html](index.html). Its embedded `project-contract` is maintained for features, flows, task status, proposals, tokens and English design/engineering contracts. Source data is not duplicated as a second editable product specification: authoring JSON remains canonical for the curriculum; the HTML snapshot is regenerated. The 279-file pre-audit baseline is in audit/baseline-manifest.json. Historical B-U/DS-U records remain evidence, not a current task queue.

DOC-PLAN-03 presents completed documentation as handoff material in the existing contracts, without completed documentation rows in the checklist or roadmap. Retain historical IDs, statuses and evidence for provenance and dependency checks. Open documentation work still appears and blocks readiness. At the DOC-PLAN-03 decision baseline, former T01.02 remained in development; its later physical completion and retirement are recorded under DOC-PLAN-06.

DOC-PLAN-04 moves T01 and its children to P1, retaining development scheduling and execution status. Completed P0 foundations are handoff material rather than execution rows. Scheduled P1 findings in development, acceptance and release remain open in the contract and tracked in their owning tasks, without duplication as current documentation issues. P0/P1 are priorities, not execution phases. Preserve historical evidence labels such as P0-T01; a planning change does not renew execution evidence.

DOC-PLAN-05 is historical. DOC-PLAN-06 removes the completed former T01/T01.01/T01.02 audio group from the active backlog and renumbers the former T02–T08 groups to current T01–T07. Use `task_id_migration` in the owner HTML for current and historical crosswalks. Older audit JSON and native evidence retain original labels as provenance; do not refresh them.

## Updating a decision or contract

Parse `<script id="project-contract" type="application/json">` in docs/index.html. Update only the relevant record/document string; preserve existing owner authority and distinguish approved decisions from proposals. JSON-escape `<`, `>` and `&` when serializing into HTML. Run `python3 scripts/sync_project_review.py`, then `--check` and `scripts/audit_project_docs.py`. No separate template or secondary HTML is required. Review presentation code lives in scripts/project_review.css and scripts/project_review.js; these do not own product rules.

Owner selections in the HTML are browser-local notes tied to a review hash covering the contract, curriculum and presentation, not repository changes or automatic approval. The user exports their feedback and sends it to the agent. Only then record the explicit decision, its wording and affected contracts. Do not reopen previously approved B-U/DS-U decisions without a concrete new conflict.

## Updating content

Change canonical lesson/unit/character JSON with stable IDs and source evidence. Run both content validators with `--self-test` and report outputs, regenerate readable Markdown, update coverage counts/current content manifest with a review addendum, regenerate review fixtures, then sync HTML. Do not rewrite historical review timestamps or pretend new content received earlier peer review. The 2026-11-07 audit adds examples in lessons 22 and 24; the earlier 302-example peer review remains historical.

## Current evidence limits

All canonical lesson/unit files and generated readable content are structurally checked. Six PDF hashes/page counts match. H02 records primary assigned-scope source/VI/EN/contextual-reading review; the entire 1,451-page corpus was not independently re-transcribed or certified by a human. H03 now has 301 VI/EN kana entries/contexts, a source-cell ledger and revision-bound primary self-review; see content-authoring/kana/README.md. Native kana integration/voice, native candidate integration and 17 locales remain tasks. H01 implements a separate Swift runtime library with package/state/migration tests on macOS, revalidated against the H02 revision; read [runtime-data-contract.md](runtime-data-contract.md) and the pinned [validation evidence](audit/t01-runtime-validation.json) for scope. The iOS application retains its scaffold. The completed former T01 bounded DEBUG/audio proof is archived as handoff with owner-attested physical E2E cases; current T01–T07 are the renumbered remaining roadmap, and full app/device acceptance remains open. The current final-documentation review attempted local file:// browser access; URL policy rejected it. No workaround or visual/interaction pass is claimed.

## Roles, not a large custom-agent roster

H02 and its four children are complete under B-U-51 primary self-review. Its [source ledger](content-authoring/source-reconciliation/ledger.md) enumerates 2,189 vocabulary rows, 253 grammar groups, 536 Kanji definitions and 1,498 unit lexical rows; all 826 curated master examples have source links. The validator pins 102 content reviews and source/content revisions, checks form/ID/variant/reading/milestone links and rejects 30 negative fixtures. All 28 grammar locator findings are resolved. The adjacent review.json records primary VI/EN/ruby review, exact image scope, 6,033 retained IDs, 26 added lexical IDs and 50 unchanged dialogue objects. Kanji transcription seeds are disclosed; optional dictionary illustrations are not exhaustive. Run `python3 scripts/validate_source_reconciliation.py --complete --self-test --check`. Refresh pins only after actual review of changed content, never to conceal drift.

Use the primary agent with these docs/checks now. If recurring batches warrant it, consider a content reviewer and an iOS integration reviewer with bounded input/output and immutable baselines. Do not automatically spawn them. A second agent's bounded review is not independent human certification. See the owner HTML for the recommendation and its OpenAI source.

## Latest name policy — B-U-59, 2026-11-08

The owner revoked the fictional-name omission in B-U-53. Retain source proper names in the assigned content scope; keep spelling, contextual reading and referent consistent. Do not filter names by fictional status or automatically map authored cast to textbook cast. The primary review restored 41 names from 38 rows on 19 visually checked source pages; see content-authoring/source-reconciliation/proper-name-review.json. H02 additionally restored 23 Kanji surname occurrences; its primary completion does not imply independent human certification.

## H03 handoff — 2026-11-08

H03.01–03 are complete as content-authoring tasks. The canonical kana JSON, source denominator, schema and per-item review live in content-authoring/kana/. Run `python3 scripts/validate_kana.py --complete --self-test --check`; after a real editorial review, `--write` refreshes validation only. All 301 examples have VI/EN meaning, orthographic reading and syllable/context speech policy. The 29 reference entries distinguish old spelling, explicit expansions and modern-equivalent contexts. T03.04 owns native tables/playback. No voice listening or independent-human/release acceptance is claimed.

At H03 entry, existing source-reconciliation input pins and lesson-27–50 readable exports were stale. H02 subsequently completed its owning review and regenerated those exports; H01 was actually rerun against the changed lesson/Kanji inputs, with its prior report preserved in audit/t01-runtime-validation-before-t02.json. The owner HTML still exposes future stale handoffs and the repository audit retains its rejection checks.

## H04 authoring handoff — 2026-11-08

H04.01–03 are complete as authoring tasks: 3,275 primary-reviewed candidates cover all 6,126 exact form/sense/variant targets. All 304 original examples retain their source wording, context, translations and IDs; all 50 dialogue objects remain fixed. Read content-authoring/sentence-bank/README.md and the generated inventory. Stable overlay UUIDs/source pointers preserve the original curriculum identities. Never regenerate identities or refresh review pins to hide drift. The immutable initial handoff remains in sentence-bank/history/.

Every candidate has full-span lexical/form/sense and grammar analysis, exact target exceptions and reviewed simplicity. Source-owned word bindings and 122 reviewed bare-character pairs distinguish the taught target from supporting compound vocabulary. Context-only lexical/grammar facts remain unfamiliar; 60 reviewed repeated lexical identities share actual introductions without changing IDs or independent N5/N4 prefixes. The oracle caps at three genuine matching examples and preserves distinct contextual readings while deduplicating identical content.

Speech authoring supplies 5,616 exact records, including 466 dictionary forms, and 155 reviewed bound contexts: 114 vocabulary entries / 120 forms plus 35 Kanji lexical occurrences. Bound records pin the exact context digest. The historical 53 count missed the second wave dash and marker-free readings. Source readings inherit H02; newly authored contexts, sentence annotations and particle projection have B-U-51 primary self-review. No voice listening or native integration is claimed.

Run `python3 scripts/validate_sentence_bank.py --complete --self-test --check`. `--write` regenerates reports only. The Python ranking/speech tools and fixtures are offline authoring evidence, not T03.05 native selection/snapshots or completed native/audio handoff acceptance. Original lesson/unit/master JSON and PDFs remain unchanged; H01's draft candidate/speech indices remain zero. Continue native work under its owning tasks rather than treating authoring completion as app/release acceptance.


## Historical T01 native handoff — superseded for status by DOC-PLAN-06

Read the former T01 section of engineering-contract.md and audit/t05-native-validation.json as historical simulator evidence. Its earlier in-progress and unperformed statements were superseded by the physical closure recorded under DOC-PLAN-06. The 14 native Simulator tests (including actual full-dialogue/solo-turn completion callbacks) do not establish offline listening, silent/media, real interruption or headset-removal acceptance. Injected missing-voice/system-event tests are explicitly labelled. No source curriculum, H01 package or project identifier changed. The proof exports 26 rows and eight fixed dialogue turns as DEBUG-only Swift data; no proof payload is compiled into Release. Run `python3 scripts/build_native_proof.py --check`; after implementation changes, rerun native tests and actually inspect captures before replacing evidence pins. Audit and review sync reject/expose stale T01 fingerprints. Do not refresh evidence merely to hide drift. Current T01 owns committed preferences and native learning-screen/runtime integration; iPad/Duo/performance/localization/release evidence remains separate.

The T01.02 continuation adds real-system eight-turn completion, dialogue-to-solo replacement/completion, stable stop and unrelated-route notification coverage. All ten component/integration tests share a serialized suite to isolate global notifications. Run test_sim with -parallel-testing-enabled NO. The pre-continuation evidence is retained in audit/t05-native-validation-before-continuation.json. No network-disabled or physical listening acceptance is implied.

The media-reset continuation fixes a retained synthesizer after reset: loss stops; reset invalidates before replacing the real synthesizer and detaching its old delegate. A deterministic regression plus an injected-notification/real-adapter retry regression pass. The complete suite has 14 tests, with fresh Release compilation and proof-marker exclusion. Actual OS reset, offline listening and physical audio remain untested. The owner confirmed no physical iPhone; do not ask again unless availability changes. Prior evidence is preserved in audit/t05-native-validation-before-media-reset.json.


## T05.01 localization handoff — 2026-11-09

Current T04.01 is complete as technical infrastructure; the parent remains in progress and T04.02 is ready. Read [localization/README.md](localization/README.md), the T04.01 engineering section and [revision-bound evidence](audit/t09-01-localization-validation.json). System resolution, typed per-field lookup, explicit English fallback/unavailable metadata, reviewed locale sidecars and locale-specific package/index projection are implemented. Source VI/EN content, identities, Japanese readings and prior editorial pins remain intact. New locale sidecars require exact owner IDs/revisions; drafts never enter the runtime index.

Run `python3 scripts/validate_localization.py --self-test --check`. Coverage enumerates 17,020 field addresses, separating 15,002 authored fields from 2,018 empty optional usage notes; fallback never counts as translated copy. The native Interface catalog contains six scoped English source keys; future UI and other locales remain work. H01 was actually rerun: 24 macOS tests pass, including five localization cases and a temporary sparse-locale package. The prior report is retained in audit/t01-runtime-validation-before-t09-01.json. One Xcode native UI test on iPhone 18 Pro / iOS 27.2 exercised EN/Arabic/Hebrew direction probes and supplied fallback metadata; all three captures were inspected. This is not integrated curriculum-reader, full locale translation, physical-device or release acceptance. Current T01 owns committed shared Settings/app wiring, T02 native search sessions, T04.02–19 translation/review. Do not refresh execution pins without the corresponding tests.

## Latest audio verification scheduling — DOC-PLAN-02, 2026-11-09

Under owner decision DOC-PLAN-02 (2026-11-09), offline listening and real-audio verification belong to development and are not required for the current documentation phase. Preserve the product requirements, unperformed cases and existing evidence; phase scheduling is not acceptance. Do not request a physical iPhone or run new audio tests merely to close documentation. At the DOC-PLAN-02 scheduling baseline, keep the then-open T01.02/A14 work in development. Its later physical closure is documented separately under DOC-PLAN-06; preserve the original evidence labels. The owner HTML records the exact instruction and phase disposition; no product feature or release criterion is removed.


## Current task IDs and native/audio closure — DOC-PLAN-06, 2026-11-09

The completed native/audio group was former T01 with children T01.01/T01.02. The owner confirmed all offline/silent fixture targets, full dialogue and solo playback, restart/Stop, actual interruption, headset removal, background/foreground and no automatic resume on the physical iPhone. Two real-driver integration tests passed on that device. The physical report records manual owner attestation, no physical UI automation, no screenshots/audio recording, and remaining scope limits; preserve those distinctions. The group is now an engineering handoff, not an active task. Former T02–T08 map in order to current T01–T07; current phase labels, owners and dependencies are in the owner HTML. The prior DOC-PLAN-05 map remains immutable migration history.
