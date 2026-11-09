# ProjectBeta

Offline Japanese learning for iOS/iPadOS, covering the approved N5 and N4 curriculum in the same phase.

**Owner: read and review only [docs/index.html](docs/index.html).** It contains the current feature scope, screen flows, integrated app/widget simulations, full authored curriculum reader, source audit, prioritized tasks and versioned review notes. It works locally without hosting.

The [development user stories](docs/index.html#development) include per-task fixtures, success/failure Given/When/Then scenarios and E2E closure prerequisites under DEV-PLAN-01. The roadmap defaults to the development phase; its English handoff is generated in [delivery-plan.md](docs/delivery-plan.md). These are test plans; execution status and existing bounded evidence remain explicit.

Completed documentation is presented as [handoff material](docs/index.html#documentation) under DOC-PLAN-03, without completed documentation task listings. Existing contracts and historical evidence remain available. The former T01.02 is complete; its physical audio proof now lives in the DOC-PLAN-06 handoff.

Completed P0 foundations remain in the handoff. DOC-PLAN-06 removes completed T01 and renumbers the remaining groups T01–T07, preserving active task order and recording both crosswalks in the owner HTML.

The previous DOC-PLAN-05 crosswalk remains in migration history. The current DOC-PLAN-06 crosswalk moves the completed former T01 IDs to the engineering handoff and maps the remaining groups to T01–T07. Historical execution evidence keeps its original labels.

The [documentation gate](docs/index.html#documentation) owns readiness for development: every documentation task must be complete and the checks below must pass before new development proceeds. The owner explicitly places translation authoring/review in development (DOC-PLAN-01). DOC-PLAN-02 originally scheduled offline listening/real-audio verification in development; the owner later completed and attested those physical cases, now archived under DOC-PLAN-06. The roadmap preserves existing implementation work and each task's execution dependencies. Documentation completion does not establish app or release acceptance. H02/H03/H04 retain their bounded primary authoring reviews; remaining locales and native integration/evidence remain explicit tasks. Current data contains 50 lessons, 50 Kanji units and 536 character definitions. Counts are not proof of semantic completeness.

Agents start at [AGENTS.md](AGENTS.md), then [agent context](docs/agent-context.md). Product and engineering contracts live in the HTML's `project-contract` block; agent exports are generated and checked. Editorial JSON and the PDF catalog remain canonical data/evidence, with a generated copy in the review. Do not edit exports independently.

```sh
python3 scripts/validate_authoring_samples.py --self-test
python3 scripts/validate_authoring_batch.py --complete --self-test
python3 scripts/validate_kana.py --complete --self-test --check
python3 scripts/validate_sentence_bank.py --complete --self-test --check
python3 scripts/validate_source_reconciliation.py --complete --self-test --check
python3 scripts/validate_localization.py --self-test --check
python3 scripts/render_authoring_content.py --check
python3 scripts/sync_project_review.py --check
python3 scripts/audit_project_docs.py
```

T04.01's [localization handoff](docs/localization/README.md) implements System resolution, per-field English fallback, revision-bound locale sidecars and locale-aware package/index projection. Its [evidence](docs/audit/t09-01-localization-validation.json) records 24 macOS runtime tests and one native UI test across EN/Arabic/Hebrew with three inspected captures. The UI catalog covers the implemented scaffold/infrastructure; translation review remains T04.02–19; full app wiring is current T01 work. Refresh the generated coverage after reviewed input changes with `python3 scripts/validate_localization.py --self-test --write`.

H02's [source ledger](docs/content-authoring/source-reconciliation/ledger.md) records 2,189 vocabulary rows, 253 grammar groups, 536 Kanji definitions and 1,498 unit lexical rows, with revision-bound primary source/VI/EN/reading review of all 102 lesson/unit/master files. After an actual editorial review of changed canonical inputs, run `python3 scripts/validate_source_reconciliation.py --complete --self-test --write` before syncing the owner HTML. The gate checks all four recorded reviews and their fingerprints; machine linkage checks do not independently establish linguistic accuracy or release acceptance.

H01 runtime foundations live in `ios/ProjectBeta/Runtime`, a separate Swift 6 library. Generate an explicitly draft package into an empty directory and run the package/state/migration tests on macOS:

```sh
python3 scripts/build_runtime_package.py --output /tmp/beta-runtime-package
python3 scripts/verify_runtime.py --report docs/audit/t01-runtime-validation.json
```

The verification command uses temporary packages and build/cache paths under `/tmp`; it also exercises real SwiftData disk save/reopen. See the generated [runtime contract](docs/runtime-data-contract.md) for the v1 formats, integration boundary and approved migration rules. Release generation remains blocked by missing content/review evidence. Generated packages are not checked in or added to app resources by H01.

After an authorized content or contract change: regenerate content Markdown, review fixtures, then the owner review. Keep `--check` passing. No dependency installation is needed; source-page validation uses the existing Poppler `pdfinfo` utility.

The iOS application retains its four-tab scaffold. The completed former T01 native/audio proof is archived in the DOC-PLAN-06 engineering handoff with physical device listening attestations and two physical-device real-driver integration tests; its older simulator/UI evidence is separately scoped. H01 verifies the separate runtime library on macOS. The current roadmap renumbers the former T02–T08 groups to T01–T07; full app wiring is current T01. No full app, WidgetKit, performance or release pass is claimed. Existing staged work is preserved; no commit or index reset was performed.

H03's [kana inventory](docs/content-authoring/kana/README.md) contains 301 reviewed authoring entries and VI/EN contexts, including a separate rare/reference group. Its source ledger and per-item self-review are revision-bound; `validate_kana.py --complete` checks authoring acceptance, not native voice or release acceptance. After an actual content review, refresh its report with `--complete --self-test --write`, regenerate readable content and sync the owner HTML. The 57 prototype cells remain representative fixtures; T03.04 owns native kana UI/playback.

H04 authoring is **complete**. Its [sentence/speech inventory](docs/content-authoring/sentence-bank/README.md) contains 3,275 primary-reviewed complete candidates covering all 6,126 form/sense/variant targets, with complete dependency/simplicity annotations and an empty gap ledger. All 304 original examples and 50 fixed dialogues retain their source content and IDs. The 5,616 exact speech records include 466 dictionary forms; 155 bound contexts cover 114 vocabulary entries / 120 forms plus 35 Kanji lexical occurrences. Run `python3 scripts/validate_sentence_bank.py --complete --self-test --check`. `--write` regenerates reports without refreshing editorial pins. Primary self-review and inherited H02 readings do not establish independent human or release acceptance. The completed native/audio handoff is documented separately; T03.05 owns native playback/selection; H01's draft runtime remains unchanged.


The completed native handoff's [native evidence](docs/audit/t05-native-validation.json) pins implementation, content inputs, native test results and external captures. Check the derived fixture with `python3 scripts/build_native_proof.py --check`; regenerate it with `python3 scripts/build_native_proof.py` only after reviewed input changes. Use Xcode MCP to run the ProjectBeta scheme's tests on iPhone 18 Pro / iOS 27.2 with `extraArgs: ["-parallel-testing-enabled", "NO"]`; see the generated engineering contract for Debug launch arguments and the documented limits of physical evidence. Release compilation excludes the proof data/screen and does not bypass content release gates.
