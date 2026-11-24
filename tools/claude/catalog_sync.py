"""Merge Claude candidates on disk into catalog.json (lead-only; one writer at a time).

    python3 tools/claude/catalog_sync.py            # sync every Claude model.json on disk
    python3 tools/claude/catalog_sync.py --check    # report differences, write nothing
    python3 tools/claude/catalog_sync.py --only sofa armchair   # only these base IDs (batch commits)

Rules (docs/RIVAL_WORKFLOW.md, docs/REVIEW_PROCESS.md):
  * Only entries whose id starts with "Claude_" are added or refreshed.
  * Entries of any other creator are never modified, reordered or removed.
  * An existing Claude entry whose status is not "candidate" (i.e. the user approved or
    rejected it) is never overwritten.
  * A Claude entry is only written when its .vox and model.json exist on disk.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def entry_from(meta: dict, mdir: Path) -> dict:
    cat, a = meta["category"], meta["id"]
    e = {
        "id": a, "base_id": meta["base_id"], "creator": "Claude", "name": meta["name"],
        "category": cat, "status": "candidate", "revision": meta.get("revision", 1),
        "source_path": f"models/{cat}/{a}/{meta['source']}",
        "metadata_path": f"models/{cat}/{a}/model.json",
        "preview_path": f"previews/{cat}/{a}/",
        "derived_paths": [f"models/{cat}/{a}/{meta['derived']['glb']}"],
        "voxel_size_m": meta["voxel_size_m"], "dimensions_m": meta["dimensions_m"],
        "occupied_voxels": meta["occupied_voxels"], "game_integrations": [],
    }
    for k in ("batch", "scale_family", "condition", "compare_base_id"):
        if k in meta:
            e[k] = meta[k]
    return e


def main():
    check = "--check" in sys.argv
    only = set(sys.argv[sys.argv.index("--only") + 1:]) if "--only" in sys.argv else None
    path = ROOT / "catalog.json"
    cat = json.loads(path.read_text())
    models = cat.setdefault("models", [])
    index = {m["id"]: i for i, m in enumerate(models)}
    added, refreshed, kept = [], [], []
    for mp in sorted(ROOT.glob("models/*/Claude_*/model.json")):
        meta = json.loads(mp.read_text())
        if only is not None and meta["base_id"] not in only and meta["id"] not in only:
            continue
        if not meta["id"].startswith("Claude_") or meta.get("creator") != "Claude":
            raise SystemExit(f"refusing non-Claude metadata {mp}")
        if not (mp.parent / meta["source"]).exists():
            continue
        e = entry_from(meta, mp.parent)
        if meta["id"] in index:
            old = models[index[meta["id"]]]
            if old.get("status") not in (None, "candidate"):
                kept.append(meta["id"])        # user decision recorded - never overwrite
                continue
            if old != e:
                refreshed.append(meta["id"])
                models[index[meta["id"]]] = e
        else:
            added.append(meta["id"])
            index[meta["id"]] = len(models)
            models.append(e)
    on_disk = {json.loads(p.read_text())["id"] for p in ROOT.glob("models/*/Claude_*/model.json")}
    stale = [m["id"] for m in models if m["id"].startswith("Claude_") and m["id"] not in on_disk]
    print(f"added {len(added)}, refreshed {len(refreshed)}, user-decided kept {len(kept)}, "
          f"Claude entries without files {stale}")
    others = sum(1 for m in models if not m["id"].startswith("Claude_"))
    print(f"other creators' entries preserved untouched: {others}")
    if not check:
        path.write_text(json.dumps(cat, indent=2) + "\n")


if __name__ == "__main__":
    main()
