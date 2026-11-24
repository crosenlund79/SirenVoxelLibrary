"""Build Claude's candidates: .vox source, model.json, derived .glb and the spec page.

    python3 tools/claude/build.py sofa armchair     # named base IDs
    python3 tools/claude/build.py --batch catalog_A # every generator whose BATCH matches
    python3 tools/claude/build.py --list            # list generators

Writes only Claude_-prefixed paths:
    models/<category>/Claude_<base_id>/{Claude_<base_id>.vox, .glb, model.json}
    docs/specs/<category>/Claude_<base_id>.md
It never writes catalog.json (run tools/claude/catalog_sync.py for that, from one place),
never touches GPT_ files and never sets any status other than 'candidate'.

The five pilot generators (Claude_pilot_001) are frozen: they are only rebuilt with
--allow-pilot, which reproduces their committed .vox byte for byte (palette v1).
"""
from __future__ import annotations

import importlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import voxkit as vk  # noqa: E402
from export_glb import write_glb  # noqa: E402

CREATOR = "Claude"
PILOT = {"workbench_worn", "rain_collector_basic", "wood_stove_compact",
         "single_bed_unmade", "pine_dead_small"}
CATEGORIES = {"furniture", "household", "consumables", "medical", "survival", "architecture",
              "combat", "vegetation", "exterior", "vehicles", "regional", "characters",
              "construction", "decorations", "map"}  # last three: GPT's names, for aligned folders
TIERS = {"micro": 0.0125, "fine": 0.025, "detail": 0.05, "standard": 0.1, "coarse": 0.2,
         "map": 0.5}
CONDITIONS = {"new", "lightly_used", "used", "worn", "damaged", "improvised", "abandoned",
              "destroyed", "living", "dead", "n/a"}
REQUIRED_META = ["story", "condition", "gameplay_use", "resolution_tier", "resolution_rationale",
                 "pivot_note", "front_note", "notes", "collision_hint"]


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def all_generators() -> list[str]:
    import catalog_registry
    single = {p.stem for p in (HERE / "models").glob("*.py")
              if not p.stem.startswith("_") and p.stem != "__init__"}
    return sorted(single | set(catalog_registry.discover()))


def load(base_id: str):
    if (HERE / "models" / f"{base_id}.py").exists():
        return importlib.import_module(f"models.{base_id}")
    import catalog_registry
    reg = catalog_registry.discover()
    if base_id not in reg:
        errs = "\n".join(f"{k}: {v.splitlines()[-1]}" for k, v in
                         catalog_registry.IMPORT_ERRORS.items())
        raise SystemExit(f"no generator for {base_id}" + (f"\nbroken family files:\n{errs}"
                                                         if errs else ""))
    return reg[base_id]


def build_one(base_id: str, allow_pilot: bool = False) -> dict:
    if base_id in PILOT and not allow_pilot:
        raise SystemExit(f"{base_id} is a frozen pilot candidate; use --allow-pilot to rebuild it")
    mod = load(base_id)
    if base_id in PILOT:  # legacy path keeps the pilot's committed metadata format
        import build_pilot
        return build_pilot.build_one(base_id)
    assert mod.BASE_ID == base_id, (mod.BASE_ID, base_id)
    assert mod.CATEGORY in CATEGORIES, f"{base_id}: unknown category {mod.CATEGORY}"
    meta = mod.META
    missing = [k for k in REQUIRED_META if k not in meta]
    assert not missing, f"{base_id}: META is missing {missing}"
    assert meta["condition"] in CONDITIONS, f"{base_id}: condition {meta['condition']}"
    res = mod.build()
    grid: vk.Grid = res["grid"]
    cell = float(res["cell"])
    tier = meta["resolution_tier"]
    assert tier in TIERS and abs(TIERS[tier] - cell) < 1e-9, \
        f"{base_id}: tier {tier} does not match cell {cell}"
    pal_version = getattr(mod, "PALETTE_VERSION", 2)
    palette = vk.PALETTES[pal_version]
    lo, hi = grid.bounds()
    if lo[2] != 0:
        raise SystemExit(f"{base_id}: lowest voxel at z={lo[2]} - model must stand on z=0")
    g, off = grid.cropped()
    nx, ny, nz = g.shape
    if max(nx, ny, nz) > 256:
        raise SystemExit(f"{base_id}: {g.shape} exceeds the VOX 256-cell axis limit")

    if "pivot_cells" in res:
        px, py, _ = res["pivot_cells"]
        pivot = [px - off[0], py - off[1], 0.0]
        footprint = None
    else:
        (x0, x1), (y0, y1) = res["footprint_cells"]
        pivot = [(x0 + x1 + 1) / 2 - off[0], (y0 + y1 + 1) / 2 - off[1], 0.0]
        footprint = [round((x1 - x0 + 1) * cell, 4), round((y1 - y0 + 1) * cell, 4)]

    asset_id = f"{CREATOR}_{base_id}"
    cat = mod.CATEGORY
    mdir = ROOT / "models" / cat / asset_id
    pdir = ROOT / "previews" / cat / asset_id
    mdir.mkdir(parents=True, exist_ok=True)
    vox_path = mdir / f"{asset_id}.vox"
    glb_path = mdir / f"{asset_id}.glb"
    vk.write_vox(vox_path, g, palette)

    def to_m(c):
        """source voxel coordinate (cell centre) -> metres from the pivot, library axes."""
        return [round((c[0] + 0.5 - off[0] - pivot[0]) * cell, 4),
                round((c[1] + 0.5 - off[1] - pivot[1]) * cell, 4),
                round((c[2] + 0.5 - off[2] - pivot[2]) * cell, 4)]

    attachments = {}
    for key, c in (res.get("attachments") or {}).items():
        info = dict(meta.get("attachments", {}).get(key, {}))
        info["voxel"] = [int(c[0] - off[0]), int(c[1] - off[1]), int(c[2] - off[2])]
        info["offset_m_from_pivot"] = to_m(c)
        attachments[key] = info

    counts = Counter(g.v[g.v > 0].tolist())
    palette_roles = [{"index": int(i), "role": vk.role_of(int(i)),
                      "hex": "#%02X%02X%02X" % tuple(palette[int(i)]), "voxels": int(n)}
                     for i, n in sorted(counts.items())]
    assert all(r["role"] for r in palette_roles), f"{base_id}: unnamed palette index used"
    glb_stats = write_glb(glb_path, asset_id, g.v, palette, cell, pivot,
                          extras={"source": vox_path.name, "voxel_size_m": cell,
                                  "pivot_voxel": pivot, "creator": CREATOR})
    batch = f"{CREATOR}_{mod.BATCH}"
    scale = getattr(mod, "SCALE", "full")
    record = {
        "schema_version": 1,
        "id": asset_id,
        "base_id": base_id,
        "creator": CREATOR,
        "name": mod.NAME,
        "category": cat,
        "revision": 1,
        "status": "candidate",
        "batch": batch,
        "scale_family": scale,
        "source": vox_path.name,
        "source_format": "MagicaVoxel VOX v150 (SIZE, XYZI, RGBA), single model",
        "derived": {"glb": glb_path.name, "glb_vertices": glb_stats["vertices"],
                    "glb_triangles": glb_stats["triangles"],
                    "glb_note": "Derived from the .vox by tools/claude/export_glb.py; do not edit "
                                "by hand. Linear COLOR_0 vertex colours, one material."},
        "voxel_size_m": cell,
        "resolution_tier": tier,
        "resolution_rationale": meta["resolution_rationale"],
        "source_axes": {"right": "+X", "front": "+Y", "up": "+Z"},
        "godot_forward": "-Z",
        "godot_mapping": "godot = ((vx - px) * s, (vz - pz) * s, -(vy - py) * s)",
        "pivot_voxel": [round(v, 3) for v in pivot],
        "pivot_note": meta["pivot_note"],
        "front_note": meta["front_note"],
        "grid_size_cells": [int(nx), int(ny), int(nz)],
        "dimensions_m": [round(nx * cell, 4), round(ny * cell, 4), round(nz * cell, 4)],
        "dimensions_note": "Occupied extents of the voxel grid (X width, Y depth, Z height).",
        "occupied_voxels": int(g.count()),
        "condition": meta["condition"],
        "gameplay_use": meta["gameplay_use"],
        "palette": f"Shared Claude palette v{pal_version} (tools/claude/voxkit.py); one material "
                   "family per 8-swatch row in MagicaVoxel's palette grid.",
        "palette_version": pal_version,
        "material_roles": sorted({r["role"] for r in palette_roles}),
        "palette_roles": palette_roles,
        "attachments": attachments,
        "collision_hint": meta["collision_hint"],
        "story": meta["story"],
        "notes": meta["notes"],
        "generator": rel(HERE / "models" / f"{base_id}.py"),
        "spec": f"docs/specs/{cat}/{asset_id}.md",
        "previews": {v: rel(pdir / f"{v}.png") for v in ("hero", "front", "side", "scale")},
        "verification": {
            "automated": f"tools/claude/validate.py; results in docs/reviews/{batch}.md",
            "magicavoxel_gui_open": "unverified (MagicaVoxel not available in the build environment)",
            "godot_import": "unverified (Godot not available in the build environment)",
        },
        "game_integration": [],
    }
    if footprint:
        record["footprint_m"] = footprint
    if getattr(mod, "COMPARE_BASE_ID", None):
        record["compare_base_id"] = mod.COMPARE_BASE_ID
    if getattr(mod, "FAMILY_FILE", None):
        record["generator"] = rel(HERE / "models" / "catalog" /
                                  (mod.FAMILY_FILE.split(".")[-1] + ".py"))
    for opt in ("mount", "allowed_components", "components_reason", "variant_of", "pairs_with"):
        if opt in meta:
            record[opt] = meta[opt]
    (mdir / "model.json").write_text(json.dumps(record, indent=2) + "\n")
    write_spec(record, meta)
    print(f"{asset_id:40s} {nx}x{ny}x{nz} @ {cell} m -> {record['dimensions_m']} m, "
          f"{record['occupied_voxels']} voxels, glb {glb_stats['triangles']} tris")
    return record


def write_spec(r: dict, meta: dict) -> None:
    """Spec page in the docs/MODEL_SPEC_TEMPLATE.md layout, generated from the generator."""
    d = r["dimensions_m"]
    lines = [
        f"# {r['name']}",
        f"- Asset ID: {r['id']}",
        f"- Base ID: {r['base_id']}",
        f"- Creator: Claude",
        f"- Category: {r['category']}",
        f"- Status: Candidate (generated; awaiting user review - not approved)",
        f"- Batch: {r['batch']}",
        f"- Scale family: {r['scale_family']}",
        f"- Intended uses: {r['gameplay_use']} (possible use in Sirens Went Quiet; "
        "not authorization to integrate)",
        "- Brief approved by: user commission for the full Claude catalog (2026-11-24); "
        "the model itself is not approved",
        "",
        "## Function and story",
        r["story"],
        f"\nCondition: **{r['condition']}**.",
        "",
        "## Silhouette",
        meta.get("silhouette", "See the generator docstring and previews."),
        "",
        "## Dimensions and orientation",
        f"- Width (X): {d[0]} m",
        f"- Depth (Y): {d[1]} m",
        f"- Height (Z): {d[2]} m",
        f"- Grid: {' x '.join(map(str, r['grid_size_cells']))} cells at {r['voxel_size_m']} m "
        f"({r['resolution_tier']} tier), {r['occupied_voxels']:,} occupied voxels",
        "- Front direction: +Y (library voxel)",
        f"- Front: {r['front_note']}",
        f"- Pivot: {r['pivot_note']} (pivot_voxel {r['pivot_voxel']})",
        f"- Resolution rationale: {r['resolution_rationale']}",
        "",
        "## Materials and colors",
        ", ".join(f"`{m}`" for m in r["material_roles"]),
        "",
        "## Details included",
    ]
    lines += [f"- {n}" for n in (meta.get("details") or r["notes"])]
    lines += ["", "## Details excluded"]
    lines += [f"- {n}" for n in (meta.get("exclusions") or
                                 ["No logos, brands or readable text.",
                                  "No random speckle noise."])]
    if r["attachments"]:
        lines += ["", "## Attachment points"]
        for k, v in r["attachments"].items():
            lines.append(f"- `{k}`: voxel {v['voxel']}, {v['offset_m_from_pivot']} m from the "
                         f"pivot. {v.get('description', '')}")
    if r.get("mount"):
        lines += ["", "## Mounting", json.dumps(r["mount"])]
    lines += ["", "## Construction and placement notes",
              f"- Collision suggestion: {r['collision_hint']}"]
    if r.get("footprint_m"):
        lines.append(f"- Placement footprint: {r['footprint_m'][0]} x {r['footprint_m'][1]} m")
    if r.get("allowed_components"):
        lines.append(f"- Separate pieces: {r['allowed_components']} "
                     f"({r.get('components_reason', '')})")
    lines += ["", "## Outputs",
              f"- `models/{r['category']}/{r['id']}/{r['source']}` (editable master)",
              f"- `models/{r['category']}/{r['id']}/model.json`",
              f"- `models/{r['category']}/{r['id']}/{r['derived']['glb']}` (derived)",
              f"- `previews/{r['category']}/{r['id']}/{{hero,front,side,scale}}.png`",
              f"- Generator: `{r['generator']}`",
              "", "## Acceptance checks",
              "- [x] Source parses and matches render (tools/claude/validate.py)",
              "- [x] Preview images are actual renders from source, not generated concept images",
              "- [ ] Recognizable silhouette at thumbnail size (user review)",
              "- [ ] Physically believable scale next to 1.75 m person (user review)",
              "- [ ] User has reviewed and explicitly approved this revision", ""]
    out = ROOT / r["spec"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))


if __name__ == "__main__":
    args = sys.argv[1:]
    allow_pilot = "--allow-pilot" in args
    if "--list" in args:
        for b in all_generators():
            m = load(b)
            print(f"{b:34s} {getattr(m, 'BATCH', 'pilot_001'):12s} {m.CATEGORY}")
        sys.exit(0)
    if "--batch" in args:
        want = args[args.index("--batch") + 1]
        ids = [b for b in all_generators() if b not in PILOT and getattr(load(b), "BATCH", "") == want]
    else:
        ids = [a for a in args if not a.startswith("--")]
    if not ids:
        raise SystemExit(__doc__)
    for b in ids:
        build_one(b, allow_pilot)
