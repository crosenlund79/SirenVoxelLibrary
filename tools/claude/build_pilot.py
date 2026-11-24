"""FROZEN pilot builder for Claude_pilot_001 (kept so the pilot stays reproducible).

Use tools/claude/build.py for everything else; it delegates here for the pilot IDs.
Pinned to palette v1 so the committed pilot .vox files reproduce byte for byte.

Original docstring: Build Claude's pilot candidates: .vox source, model.json and derived .glb.

    python3 tools/claude/build.py            # all five
    python3 tools/claude/build.py workbench_worn

Writes only Claude_-prefixed paths under models/<category>/Claude_<base_id>/.
Status is always 'candidate'; only the user can approve a model.
"""
from __future__ import annotations

import importlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import voxkit as vk  # noqa: E402
from export_glb import write_glb  # noqa: E402

CREATOR = "Claude"
BATCH = "pilot_001"
MODELS = ["workbench_worn", "rain_collector_basic", "wood_stove_compact",
          "single_bed_unmade", "pine_dead_small"]


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def build_one(base_id: str) -> dict:
    mod = importlib.import_module(f"models.{base_id}")
    res = mod.build()
    grid: vk.Grid = res["grid"]
    cell = res["cell"]
    lo, hi = grid.bounds()
    if lo[2] != 0:
        raise SystemExit(f"{base_id}: lowest voxel at z={lo[2]} - model must stand on z=0")
    g, off = grid.cropped()
    nx, ny, nz = g.shape

    if "pivot_cells" in res:
        px, py, pz = res["pivot_cells"]
        pivot = [px - off[0], py - off[1], 0.0]
        footprint = None
    else:
        (x0, x1), (y0, y1) = res["footprint_cells"]
        pivot = [(x0 + x1 + 1) / 2 - off[0], (y0 + y1 + 1) / 2 - off[1], 0.0]
        footprint = [round((x1 - x0 + 1) * cell, 3), round((y1 - y0 + 1) * cell, 3)]

    asset_id = f"{CREATOR}_{base_id}"
    cat = mod.CATEGORY
    mdir = ROOT / "models" / cat / asset_id
    pdir = ROOT / "previews" / cat / asset_id
    mdir.mkdir(parents=True, exist_ok=True)
    vox_path = mdir / f"{asset_id}.vox"
    glb_path = mdir / f"{asset_id}.glb"
    vk.write_vox(vox_path, g, vk.PALETTE_RGB_V1)

    def to_m(c):
        """source voxel coordinate -> metres relative to the pivot (library axes)."""
        return [round((c[0] - off[0] - pivot[0]) * cell, 4), round((c[1] - off[1] - pivot[1]) * cell, 4),
                round((c[2] - off[2] - pivot[2]) * cell, 4)]

    attachments = {}
    for key, cell_key in [("flue_outlet", "flue_outlet_cell"), ("gutter_inlet", "inlet_connection_cell")]:
        if cell_key in res:
            info = dict(mod.META["attachments"].get(key, {}))
            c = res[cell_key]
            info["voxel"] = [c[0] - off[0], c[1] - off[1], c[2] - off[2]]
            info["offset_m_from_pivot"] = to_m(c)
            attachments[key] = info

    counts = Counter(g.v[g.v > 0].tolist())
    palette_roles = [{"index": int(i), "role": vk.role_of(int(i)),
                      "hex": "#%02X%02X%02X" % tuple(vk.PALETTE_RGB_V1[int(i)]), "voxels": int(n)}
                     for i, n in sorted(counts.items())]
    glb_stats = write_glb(glb_path, asset_id, g.v, vk.PALETTE_RGB_V1, cell, pivot,
                          extras={"source": vox_path.name, "voxel_size_m": cell,
                                  "pivot_voxel": pivot, "creator": CREATOR})
    meta = mod.META
    record = {
        "schema_version": 1,
        "id": asset_id,
        "base_id": base_id,
        "creator": CREATOR,
        "name": mod.NAME,
        "category": cat,
        "revision": 1,
        "status": "candidate",
        "batch": f"{CREATOR}_{BATCH}",
        "source": vox_path.name,
        "source_format": "MagicaVoxel VOX v150 (SIZE, XYZI, RGBA), single model",
        "derived": {"glb": glb_path.name, "glb_vertices": glb_stats["vertices"],
                    "glb_triangles": glb_stats["triangles"],
                    "glb_note": "Derived from the .vox by tools/claude/export_glb.py; do not edit "
                                "by hand. Linear COLOR_0 vertex colours, one material."},
        "voxel_size_m": cell,
        "resolution_tier": meta["resolution_tier"],
        "resolution_rationale": meta["resolution_rationale"],
        "source_axes": {"right": "+X", "front": "+Y", "up": "+Z"},
        "godot_forward": "-Z",
        "godot_mapping": "godot = ((vx - px) * s, (vz - pz) * s, -(vy - py) * s)",
        "pivot_voxel": [round(v, 3) for v in pivot],
        "pivot_note": meta["pivot_note"],
        "front_note": meta["front_note"],
        "grid_size_cells": [int(nx), int(ny), int(nz)],
        "dimensions_m": [round(nx * cell, 3), round(ny * cell, 3), round(nz * cell, 3)],
        "dimensions_note": "Occupied extents of the voxel grid (X width, Y depth, Z height).",
        "occupied_voxels": int(g.count()),
        "palette": "Shared Claude pilot palette (tools/claude/voxkit.py); one material family "
                   "per 8-swatch row in MagicaVoxel's palette grid.",
        "material_roles": sorted({r["role"] for r in palette_roles}),
        "palette_roles": palette_roles,
        "attachments": attachments,
        "collision_hint": meta["collision_hint"],
        "story": meta["story"],
        "notes": meta["notes"],
        "generator": rel(HERE / "models" / f"{base_id}.py"),
        "previews": {v: rel(pdir / f"{v}.png") for v in ("hero", "front", "side", "scale")},
        "verification": {
            "automated": f"tools/claude/validate.py; results in docs/reviews/{CREATOR}_{BATCH}.md",
            "magicavoxel_gui_open": "unverified (MagicaVoxel not available in the build environment)",
            "godot_import": "unverified (Godot not available in the build environment)",
        },
        "game_integration": [],
    }
    if footprint:
        record["footprint_m"] = footprint
    (mdir / "model.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"{asset_id:34s} cells {nx}x{ny}x{nz} @ {cell} m  -> "
          f"{record['dimensions_m']} m, {record['occupied_voxels']} voxels, "
          f"glb {glb_stats['triangles']} tris")
    return record


def update_catalog(records):
    path = ROOT / "catalog.json"
    cat = json.loads(path.read_text())
    models = cat.setdefault("models", [])
    by_id = {m["id"]: i for i, m in enumerate(models)}
    for r in records:
        entry = {
            "id": r["id"], "base_id": r["base_id"], "creator": r["creator"], "name": r["name"],
            "category": r["category"], "status": "candidate", "revision": r["revision"],
            "source_path": f"models/{r['category']}/{r['id']}/{r['source']}",
            "metadata_path": f"models/{r['category']}/{r['id']}/model.json",
            "preview_path": f"previews/{r['category']}/{r['id']}/",
            "derived_paths": [f"models/{r['category']}/{r['id']}/{r['derived']['glb']}"],
            "voxel_size_m": r["voxel_size_m"], "dimensions_m": r["dimensions_m"],
            "occupied_voxels": r["occupied_voxels"], "game_integrations": [],
        }
        if not r["id"].startswith(f"{CREATOR}_"):
            raise SystemExit("refusing to write a non-Claude catalog entry")
        if r["id"] in by_id:
            old = models[by_id[r["id"]]]
            if old.get("status") not in (None, "candidate"):
                raise SystemExit(f"{r['id']} is {old['status']} - refusing to overwrite")
            models[by_id[r["id"]]] = entry
        else:
            models.append(entry)
    path.write_text(json.dumps(cat, indent=2) + "\n")


if __name__ == "__main__":
    ids = sys.argv[1:] or MODELS
    recs = [build_one(b) for b in ids]
    update_catalog(recs)
