"""Compact registry for catalog generators (creator: Claude).

Family files in tools/claude/models/catalog/*.py define several models each:

    from catalog_registry import model
    from voxkit import Grid

    @model("sofa", story="Bought second-hand, ...", details=["..."])
    def sofa():
        g = Grid(50, 22, 20)
        ...
        return g                      # or {"grid": g, "footprint_cells": ..., "attachments": ...}

Everything not given is filled from docs/claude/manifest.json (name, category, cell, batch,
condition, gameplay_use) and from tier/category defaults (rationale, pivot, front, collision).
tools/claude/build.py falls back to this registry when there is no standalone
models/<base_id>.py, so the build, preview, validation and catalog tools work unchanged.
A family file that fails to import only disables its own models (reported, not fatal).
"""
from __future__ import annotations

import importlib
import json
import traceback
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = {a["base_id"]: a for a in
            json.loads((ROOT / "docs/claude/manifest.json").read_text())["assets"]}
REGISTRY: dict[str, SimpleNamespace] = {}
IMPORT_ERRORS: dict[str, str] = {}

TIER_OF = {0.0125: "micro", 0.025: "fine", 0.05: "detail", 0.1: "standard", 0.2: "coarse",
           0.5: "map"}
TIER_WHY = {
    "micro": "1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the "
             "grip, cap or label that identifies it.",
    "fine": "2.5 cm cells: a handheld or small gear item whose handles, straps and blades would "
            "be 2-4x too thick at 5 cm.",
    "detail": "5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, "
              "rails, cushions, doors) stay believable instead of toy-like; matches the game's "
              "0.05 m character rig.",
    "standard": "10 cm cells (the game's structural grid): large silhouettes such as walls, "
                "vehicles and trees read clearly without inflating the voxel count.",
    "coarse": "20 cm cells for a large, distant silhouette.",
    "map": "50 cm cells: regional-map scale, real-world metres with far fewer voxels; only "
           "massing, roofs, entrances and one identifying feature are modelled.",
}
FRONT = {
    "furniture": "+Y is the side a person uses (seat, doors, drawers, controls).",
    "survival": "+Y is the working / interaction side.",
    "construction": "+Y is the outside face; the module fills its full span.",
    "combat": "Working end / muzzle points +Y, top side up; lowest point on z = 0.",
    "consumables": "+Y is the label / opening side.",
    "vegetation": "No functional front; character details face the default camera (-X/+Y).",
    "decorations": "+Y faces the street or the person using it.",
    "vehicles": "The vehicle's nose is +Y.",
    "map": "+Y is the street side / main entrance.",
    "characters": "The character faces +Y in a neutral standing display pose.",
}
FOOTPRINT_PIVOT = "Bottom centre of the occupied footprint at ground level."


def model(base_id: str, *, story: str, name: str | None = None, category: str | None = None,
          cell: float | None = None, batch: str | None = None, condition: str | None = None,
          gameplay_use: str | None = None, why: str | None = None, pivot_note: str | None = None,
          front_note: str | None = None, notes=(), collision_hint: str | None = None,
          details=None, exclusions=None, silhouette: str | None = None, attachments=None,
          compare_base_id: str | None = None, **extra):
    """Register a generator function. `why` is appended to the tier's default rationale."""
    m = MANIFEST.get(base_id, {})

    def deco(fn):
        c = float(cell if cell is not None else m.get("cell_m", 0.05))
        tier = TIER_OF[round(c, 4)]
        cat = category or m.get("category")
        meta = {
            "story": story,
            "condition": condition or m.get("condition", "used"),
            "gameplay_use": gameplay_use or m.get("gameplay_use") or "Catalog prop",
            "resolution_tier": tier,
            "resolution_rationale": TIER_WHY[tier] + (" " + why if why else ""),
            "pivot_note": pivot_note or FOOTPRINT_PIVOT,
            "front_note": front_note or FRONT.get(cat, "+Y is the front."),
            "notes": list(notes) or [m.get("brief", "")],
            "collision_hint": collision_hint or "Box matching dimensions_m, centred on the pivot.",
        }
        for k, v in (("details", details), ("exclusions", exclusions),
                     ("silhouette", silhouette), ("attachments", attachments)):
            if v:
                meta[k] = v
        meta.update({k: v for k, v in extra.items() if k != "hollow"})

        def build():
            r = fn()
            if not isinstance(r, dict):
                r = {"grid": r}
            if extra.get("hollow", True):
                hollow(r["grid"])
            r.setdefault("cell", c)
            if "pivot_cells" not in r and "footprint_cells" not in r:
                lo, hi = r["grid"].bounds()
                r["footprint_cells"] = ((int(lo[0]), int(hi[0])), (int(lo[1]), int(hi[1])))
            return r

        REGISTRY[base_id] = SimpleNamespace(
            BASE_ID=base_id, CATEGORY=cat, NAME=name or m.get("name", base_id),
            BATCH=f"catalog_{batch or m.get('batch', 'X')}", CELL=c, META=meta, build=build,
            COMPARE_BASE_ID=compare_base_id, __name__=f"catalog.{fn.__module__}.{base_id}",
            FAMILY_FILE=fn.__module__)
        return fn
    return deco


def hollow(g):
    """Remove invisible interior fill: cells whose whole 3x3x3 neighbourhood is occupied.
    (The 6-neighbour rule is not enough: it removes the cell above a small foot and leaves the
    foot attached only through a void.) The visible surface is unchanged, the remaining shell
    stays closed, and tools/claude/validate.py re-checks 6-connectivity afterwards."""
    import numpy as np
    v = g.v > 0
    p = np.pad(v, 1)
    inner = v.copy()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                inner &= np.roll(p, (dx, dy, dz), axis=(0, 1, 2))[1:-1, 1:-1, 1:-1]
    g.v[inner] = 0
    return int(inner.sum())


def discover(verbose=False):
    """Import every family file; a broken file is reported and skipped."""
    for p in sorted((HERE / "models" / "catalog").glob("*.py")):
        if p.stem.startswith("_"):
            continue
        name = f"models.catalog.{p.stem}"
        try:
            importlib.import_module(name)
        except Exception:  # noqa: BLE001 - keep other families usable
            IMPORT_ERRORS[p.stem] = traceback.format_exc(limit=3)
            if verbose:
                print(f"[registry] {p.stem} failed to import:\n{IMPORT_ERRORS[p.stem]}")
    return REGISTRY
