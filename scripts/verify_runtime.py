#!/usr/bin/env python3
"""T01 package/state failure fixtures + real macOS Swift/SwiftData tests.

Outputs are temporary; this does not build or exercise the iOS application.
"""
import copy
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import uuid

sys.dont_write_bytecode = True
from build_runtime_package import ROOT, build, digest, encoded, normalize
from translation_overlays import pin, review_pin


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="beta-runtime-") as temp:
        work = Path(temp)
        base = work / "base"
        manifest = build(base)
        # End-to-end sparse locale projection: one reviewed meaning, one unreviewed meaning.
        source_path = 'docs/content-authoring/lesson-01.json'
        first_word = json.loads((ROOT / source_path).read_bytes())['vocabulary'][0]
        localized_row = dict(path=source_path, pointer='/vocabulary/0/meanings/0/text', ownerID=first_word['id'],
                             sourceSha256=pin(first_word), text='synthetic-ar-meaning', state='reviewed', reviewer='test fixture only', reviewSha256=None)
        localized_row['reviewSha256'] = review_pin('ar', localized_row)
        second_word = json.loads((ROOT / source_path).read_bytes())['vocabulary'][1]
        draft_row = dict(localized_row, pointer='/vocabulary/1/meanings/0/text', ownerID=second_word['id'],
                         sourceSha256=pin(second_word), text='synthetic-ar-draft', state='draft', reviewer='', reviewSha256=None)
        localized_manifest = build(work / 'localized', locale_overlays=[dict(version=1, locale='ar', fields=[localized_row, draft_row])])
        assert set(localized_manifest['entities']) == set(manifest['entities'])
        again = work / "repeat"
        build(again)
        for path in base.rglob("*"):
            if path.is_file():
                assert path.read_bytes() == (again / path.relative_to(base)).read_bytes(), path
        assert normalize("ĐIỆN THOẠI") == "dien thoai"
        assert normalize("ガッコウ") == normalize("がっこう")
        assert normalize("が") != normalize("か")
        try:
            build(work / "release", "release")
            raise AssertionError("Release unexpectedly built")
        except ValueError as error:
            assert "Release blocked" in str(error)
        # Every authored UUID, including non-favorite word/example identities, survives.
        authored = set()
        def ids(value):
            if isinstance(value, dict):
                if "id" in value:
                    uuid.UUID(value["id"])
                    authored.add(value["id"])
                for child in value.values():
                    ids(child)
            elif isinstance(value, list):
                for child in value:
                    ids(child)
        for path in manifest["sourceInputHashes"]:
            if Path(path).name.startswith(("lesson-", "unit-", "characters-")):
                ids(json.loads((ROOT / path).read_text()))
        assert authored == set(manifest["entities"])
        (work / "expected-authored-ids.json").write_bytes(encoded(sorted(authored)))
        units = [v for v in manifest["entities"].values() if v["kind"] == "unit" and 21 <= v["number"] <= 25]
        for unit in units:
            milestone = manifest["unitMilestones"][unit["rootID"]]
            assert manifest["entities"][milestone]["number"] == 25
            assert manifest["entities"][milestone]["level"] == "N5"

        def fixture(name, mutate):
            dest = work / name
            shutil.copytree(base, dest)
            m = copy.deepcopy(manifest)
            mutate(m, dest)
            (dest / "manifest.json").write_bytes(encoded(m))
            return m

        fixture("unsupported", lambda m, p: m.update(schemaVersion=99))
        fixture("relabelled", lambda m, p: m.update(mode="release"))
        fixture("missing-reference", lambda m, p: m["orderedLessons"]["N5"].append(str(uuid.uuid4())))
        fixture("unsafe-path", lambda m, p: m["shards"].update({"../escape.json": next(iter(m["shards"].values()))}))
        fixture("checksum", lambda m, p: (p / next(iter(m["shards"]))).write_bytes(b"{}"))
        fixture("bad-index", lambda m, p: (p / "search.sqlite").write_bytes(b"not sqlite"))

        def changed_index(m, p, statement, parameters=()):
            db = sqlite3.connect(p / "search.sqlite")
            db.execute(statement, parameters)
            db.commit()
            db.close()
            raw = (p / "search.sqlite").read_bytes()
            m["searchIndex"].update(sha256=digest(raw), bytes=len(raw))
        fixture("index-version", lambda m, p: changed_index(m, p, "PRAGMA user_version=99"))
        fixture("index-target", lambda m, p: changed_index(m, p, "UPDATE results SET targetID='missing' WHERE rowid=1"))
        fixture("index-incomplete", lambda m, p: changed_index(m, p, "DELETE FROM results WHERE rowid=1"))

        def wrong_pointer(m, p):
            location = next(v for v in m["entities"].values() if v["kind"] == "vocabulary")
            location["pointer"] = "/vocabulary/999999"
        fixture("pointer", wrong_pointer)
        def bad_detail_ref(m, p):
            location = next(v for v in m["entities"].values() if v["kind"] == "lesson")
            path = location["shard"]
            data = json.loads((p / path).read_bytes())
            data["content"]["sentence_patterns"][0]["grammar_point_id"] = "missing"
            raw = encoded(data)
            (p / path).write_bytes(raw)
            m["shards"][path] = dict(sha256=digest(raw), bytes=len(raw))
        fixture("detail-reference", bad_detail_ref)

        def upgrade(m, p):
            m["contentVersion"] += ".next"
            changed_index(m, p, "UPDATE metadata SET value=? WHERE key='contentVersion'", (m["contentVersion"],))
        newer = fixture("additive", upgrade)
        # Real appended lesson fixture: existing prefixes retain exactly their meaning.
        appended_id = "00000000-0000-4000-8000-000000000001"
        def append(m, p):
            upgrade(m, p)
            m["contentVersion"] += ".append"
            changed_index(m, p, "UPDATE metadata SET value=? WHERE key='contentVersion'", (m["contentVersion"],))
            path = f"shards/{appended_id}.json"
            raw = encoded(dict(schemaVersion=1, rootID=appended_id, content=dict(id=appended_id)))
            (p / path).write_bytes(raw)
            m["shards"][path] = dict(sha256=digest(raw), bytes=len(raw))
            m["entities"][appended_id] = dict(kind="lesson", rootID=appended_id, targetID=appended_id,
                level="N4", number=51, pointer="", shard=path)
            m["orderedLessons"]["N4"].append(appended_id)
        fixture("appended", append)
        def reordered(m, p):
            upgrade(m, p)
            m["orderedLessons"]["N5"][:2] = list(reversed(m["orderedLessons"]["N5"][:2]))
        fixture("reordered", reordered)
        def removed(m, p):
            upgrade(m, p)
            # Remove the last vocabulary in its lesson so the remaining entity pointers stay stable.
            id, location = next((i, v) for i, v in reversed(list(m["entities"].items())) if v["kind"] == "vocabulary")
            path = location["shard"]
            data = json.loads((p / path).read_bytes())
            assert location["pointer"].startswith("/vocabulary/")
            index = int(location["pointer"].rsplit("/", 1)[1])
            assert index == len(data["content"]["vocabulary"]) - 1
            assert data["content"]["vocabulary"][index]["id"] == id
            data["content"]["vocabulary"].pop()
            raw = encoded(data)
            (p / path).write_bytes(raw)
            m["shards"][path] = dict(sha256=digest(raw), bytes=len(raw))
            del m["entities"][id]
            db = sqlite3.connect(p / "search.sqlite")
            db.execute("DELETE FROM fields WHERE resultID=?", (id,))
            db.execute("DELETE FROM results WHERE id=?", (id,))
            db.commit()
            db.close()
            raw = (p / "search.sqlite").read_bytes()
            m["searchIndex"].update(sha256=digest(raw), bytes=len(raw))
        fixture("removed", removed)
        mapping = dict(schemaVersion=2, fromVersion=manifest["contentVersion"], toVersion=newer["contentVersion"],
                       lessonReplacements={}, approvalReference=None)
        (work / "mapping.json").write_bytes(encoded(mapping))
        print(f"PASS generator: deterministic 636 shards; {len(authored)} exact authored IDs; release gate; normalization; cross-level milestones", flush=True)
        env = dict(os.environ, BETA_RUNTIME_FIXTURES=str(work),
                   CLANG_MODULE_CACHE_PATH="/tmp/project-beta-t01-clang-cache",
                   SWIFTPM_MODULECACHE_OVERRIDE="/tmp/project-beta-t01-module-cache")
        command = ["swift", "test", "--disable-sandbox", "--package-path", str(ROOT / "ios/ProjectBeta/Runtime"),
                   "--scratch-path", "/tmp/project-beta-t01-swift-build"]
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        result.check_returncode()
        passed = re.search(r"Test run with (\d+) tests.*passed", result.stdout + result.stderr)
        assert passed, "Missing Swift Testing completion evidence"
        if args.report:
            files = sorted((ROOT / "ios/ProjectBeta/Runtime").rglob("*"))
            files = [p for p in files if p.is_file() and ".build" not in p.parts and ".swiftpm" not in p.parts]
            files += [ROOT / "scripts/build_runtime_package.py", Path(__file__)]
            report = dict(task="P0-T01", completedAt=datetime.now(timezone.utc).isoformat(),
                scope="Derived package validation and macOS Swift/SwiftData library tests; not an iOS application test",
                platform=dict(system=platform.system(), version=platform.mac_ver()[0], architecture=platform.machine()),
                compiler=subprocess.run(["swift", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
                contentVersion=manifest["contentVersion"], shards=len(manifest["shards"]), authoredIDs=len(authored),
                searchRows=sqlite3.connect(base / "search.sqlite").execute("SELECT COUNT(*) FROM results").fetchone()[0],
                swiftTestsPassed=int(passed[1]), invalidPackageFixtures=11,
                generatorChecks=["Byte-identical rebuild", "Every authored UUID preserved", "Release blocked",
                    "Japanese/Latin normalization", "Units 21–25 milestone N5 lesson 25",
                    "Sparse reviewed locale sidecar projects into detail/index; draft fields excluded"],
                migrationFixtures=["additive-version", "appended-lesson", "removed-vocabulary", "unavailable-favorite-retention",
                    "reordered-lessons-exact-prefix", "explicit-reviewed-prefix-mapping", "migration-save-rollback"],
                inputHashes=manifest["sourceInputHashes"], implementationHashes={str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in files},
                limitations=["Draft content only; no release package or reviewed speech-context bank",
                    "No iOS app build/device/UI/TTS/WidgetKit/performance acceptance",
                    "CoreData notification-registration warnings in restricted host; disk round-trip assertions passed",
                    "Save failure is injected at persistence seam; no disk-full or physical-device fault injection"])
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_bytes(json.dumps(report, ensure_ascii=False, indent=2).encode() + b"\n")
            print("Wrote runtime evidence: " + str(args.report))


if __name__ == "__main__":
    main()
