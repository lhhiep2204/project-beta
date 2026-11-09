> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.

# Design and implementation acceptance

Status: **CURRENT-PHASE ACCEPTANCE CONTRACT.** Document acceptance is distinct from native implementation, content authoring and release acceptance.

## Design artifact completion

- Agent entry point identifies normative decisions, tokens, screen/component contracts, scope overrides, performance constraints and implementation/content dependencies.
- No current requirement relies on a silent product assumption. Confirmed owner answers are traceable through DS-U IDs; ordinary implementation bindings are identified as such.
- HTML covers first entry, Lessons, Kanji, Favorites, Search, Settings, native-style states and widget/type exploration with representative data. Prototype-only controls and silent playback simulation stay outside product claims.
- Token values and the embedded review snapshot agree. Local links, JSON/JavaScript syntax and source-fixture identity/alignment are checked. Browser/native visual verification limits are reported honestly.

## Required native verification after implementation

| Area | Behavioral acceptance |
| --- | --- |
| Navigation | DS-U-50: at sufficient width, exactly sidebar and detail; destination controls and lesson/unit collection share the sidebar. No third content column at ample width. Compact tabs/hierarchy retain access to all routes. Resize/rotation/large text preserve destination, selected IDs/query and the same logical playback owner. |
| First entry/preferences | No implicit level on first launch; selection persists. Later launches open Lessons at remembered level. Shared level, language, appearance and furigana persist; no reading-position restoration. |
| Lessons | Topic-first continuous order; complete content remains reachable with lazy rendering; jump/search can materialize an offscreen target. System text size grows rows/reflows controls rather than clipping. |
| Learned prefix | N5/N4 independent; source numbering preserved. Correct changed-range confirmation; single changes immediate; cancel/failure unchanged. No uncommitted widget/example state. |
| Favorites | Exact direct parent/item targets, newest-first/filtering, no child explosion in app lists. Context menu/remove feedback correct. Independent child saves survive parent removal. A content-removed target remains unavailable under its old ID, can be removed explicitly, and is absent from widget/search candidates. |
| Search | 500 ms trailing debounce, no stale-result publication, full offline approved scope, case/Vietnamese/kana matching, exact/prefix/contains ranking and exact-location navigation. Japanese voiced distinctions/IME input remain correct. |
| Examples | Maximum three, no expansion, matching target/translation/audio, learned grammar → unfamiliar words → simplicity order, explicit target exception and simplest fallback. Reselect on open; no silent visible/speaking replacement. Fixed dialogues; basic kana exception. |
| Pronunciation | Idle/waves/restart behavior, whole-dialogue/solo-turn scope, exact per-form target/sense, replacement and separate stop. Bound forms use labeled complete reviewed context; missing context remains readable with item-scoped pronunciation unavailable. Never speak placeholders, translations or duplicated ruby. Stops on departure/background/interruption/headphone removal, no automatic resume. Explicit tap uses media volume in silent mode. Missing voice keeps reading and guidance. |
| Language/layout | Shared UI/content preference, English fallback indication, Vietnamese-only Sino-Vietnamese, RTL navigation with correct Japanese direction and contextual ruby. Test representative long translations and current system text sizes. |
| Widgets | Eligible family embedding/gallery, approved counts/readability reduction, learned/favorites source rules/milestones/parent expansion, random timelines under system scheduling, empty-source preservation and app-opening tap. No inline audio/favorite/deeper action. |
| State/failure | Scoped loading/empty/error, no false completed-empty search during unavailable index/loading, committed-success feedback only after save, retry without loss of context or unrelated saved data. |
| Performance | Follow the measured launch/render/search/audio/widget/size scenarios and evidence format in performance-and-footprint.md. Do not substitute architectural claims for measurements. |

Dedicated VoiceOver/Accessibility specialization and its acceptance matrix are deferred under DS-U-47/48. Native control behavior, system text-size following and RTL/localization remain current requirements; do not advertise specialized Accessibility support from this document.

## Content/release dependencies

Remaining work covers native adoption/voice verification of the authored kana/candidate/speech banks, T05.02–19 locale/UI completion and review, release rights, physical/Duo evidence and release identifiers. Migration implementation must preserve unavailable favorite IDs and reject a learned-prefix mapping that adds lessons. Track them in their owning content/engineering/release work, without guessing behavior in UI source. Authoring drafts and prototype fixtures are not runtime-ready release content.

## Evidence for this documentation task

Final evidence and verification limits are recorded in [the audit](../audit/report.md) and the owner HTML. This documentation review changes no iOS source and reruns no native tests. Existing bounded H01/T01/T05.01 evidence retains its recorded scope; no new application/device/performance pass is claimed.


## Documentation-to-development gate — DOC-PLAN-01, 2026-11-09

The owner requires every documentation task to complete before development. The owner explicitly places translation production/review in development. The owner HTML maintains DOC-01–06 and computes readiness from their statuses, H00, unresolved documentation findings, product proposals and current evidence drift. Required synchronization/audit checks must pass; this does not close implementation, native, performance or release tasks. Individual execution dependencies remain binding.


## Offline listening/audio scheduling — DOC-PLAN-02, 2026-11-09

Under owner decision DOC-PLAN-02 (2026-11-09), offline listening and real-audio verification belong to development and are not required for the current documentation phase. Preserve the product requirements, unperformed cases and existing evidence; phase scheduling is not acceptance. T01.02 remains in_progress as a development task. This decision changes the execution phase only; offline Japanese speech, media-volume behavior, interruption/headset stopping and no automatic resume remain the approved product contract. No additional native/audio test is performed or claimed by this documentation update.
