"""Write docs/reviews/Claude_<batch>.md from the models on disk and a validation report.

    python3 tools/claude/review_doc.py catalog_A --validation /tmp/val.json --notes notes.md

The tables are generated from each model.json (never typed by hand). The lead's visual QC
notes (what was checked, corrected, and what still needs the art director's attention) are
included verbatim from --notes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sheets import BATCH_TITLES, CATEGORY_TITLES  # noqa: E402


def main():
    a = sys.argv[1:]
    batch = a[0]
    val = json.loads(Path(a[a.index("--validation") + 1]).read_text()) if "--validation" in a else {}
    notes = Path(a[a.index("--notes") + 1]).read_text() if "--notes" in a else ""
    metas = [json.loads(p.read_text()) for p in sorted(ROOT.glob("models/*/Claude_*/model.json"))]
    ms = sorted([m for m in metas if m.get("batch") == f"Claude_{batch}"],
                key=lambda m: (list(CATEGORY_TITLES).index(m["category"]), m["base_id"]))
    vm = val.get("models", {})
    title = BATCH_TITLES.get(batch, batch)
    L = [f"# Claude_{batch} — {title.split(' - ', 1)[-1]} (review sheet)", "",
         f"**Status: all {len(ms)} models are `candidate`, awaiting the user's review.** Nothing "
         "here is approved, and nothing has been copied into Sirens Went Quiet or any other game.",
         "", "- Creator: Claude (lead) with specialist Claude agents, each owning one model "
         "family; independent of GPT (no `GPT_` file was opened or used).",
         "- Brief: the user's full-catalog commission of 2026-11-24; per-model briefs in "
         "`docs/claude/manifest.json`, rules in `docs/claude/CATALOG_STYLE.md`.",
         "- Specs: `docs/specs/<category>/Claude_<base_id>.md` (generated from each generator).",
         ""]
    sheets = sorted((ROOT / "previews" / "batches").glob(f"Claude_{batch}*.png"))
    if sheets:
        L += ["## Contact sheets", ""]
        for p in sheets:
            L += [f"![{p.stem}](../../previews/batches/{p.name})", ""]
    scenes = sorted((ROOT / "previews" / "scenes").glob(f"Claude_{batch}_*.png"))
    if scenes:
        L += ["## Showcase scenes (actual models placed together)", ""]
        for p in scenes:
            L += [f"![{p.stem}](../../previews/scenes/{p.name})", ""]
    L += ["## Models", "",
          "| Asset | Category | Cell | Grid (cells) | Size W × D × H (m) | Voxels | GLB tris | "
          "Condition | Validation |", "|---|---|---:|---|---|---:|---:|---|---|"]
    for m in ms:
        r = vm.get(m["id"], {}).get("result", "not run")
        g = " × ".join(map(str, m["grid_size_cells"]))
        d = " × ".join(f"{v:g}" for v in m["dimensions_m"])
        L.append(f"| `{m['id']}` | {m['category']} | {m['voxel_size_m']:g} m | {g} | {d} | "
                 f"{m['occupied_voxels']:,} | {m['derived']['glb_triangles']:,} | "
                 f"{m['condition']} | {r} |")
    L += ["", "## Interpretations", ""]
    for m in ms:
        L.append(f"- **`{m['id']}`** — {m['story']}")
    warn = [(k, w) for k, v in vm.items() for w in v.get("warnings", [])]
    L += ["", "## Validation", "",
          "Run with `python3 tools/claude/validate.py --batch " + batch + "` (full mode: includes "
          "the Goxel import and the Khronos glTF-Validator). Checks per model: VOX structure "
          "(v150 `MAIN` > `SIZE`, `XYZI`, `RGBA`), bounds ≤ 256, no duplicate cells, valid palette "
          "indices, palette identical to Claude palette v2; counts, grid and metres match "
          "`model.json`; ground contact and pivot inside the footprint; one 6-connected piece "
          "(or a documented number of pieces); naming/status; independent parse by py-vox-io "
          "and an independent editor import through Goxel 0.11 (positions and colours "
          "identical); GLB bounds/orientation/winding/per-colour face area against the source; "
          "trimesh and pygltflib loads; Khronos glTF-Validator.", ""]
    passed = sum(1 for k, v in vm.items() if str(v.get("result", "")).startswith("pass"))
    L.append(f"Result: **{passed}/{len(ms)} pass**." if vm else "Result: not run.")
    if warn:
        L += ["", "Warnings (reviewed by the lead; see notes):"]
        L += [f"- `{k}`: {w}" for k, w in warn]
    L += ["", "**Not verified** (no GUI tools in the build environment): opening the files in "
          "**MagicaVoxel** itself, and **Godot** import of the derived `.glb` files.", ""]
    L += ["## Lead QC notes", "", notes.strip() or "_none_", ""]
    L += ["## How the previews were made", "",
          "All images are ray-traced by `tools/claude/voxrender.py` from the `.vox` files read "
          "back from disk (`tools/claude/render_previews.py`, `sheets.py`, `scenes.py`): "
          "orthographic cameras, the same soft-shadowed sun, sky occlusion and studio floor as "
          "the pilot. Hero az −35° el 30°; front and side elevations; scale view at a fixed, "
          "stated px/m beside the 1.75 m figure. Contact sheets use one camera, one light and one "
          "px/m per page. The game-camera strip uses the game's 56° pitch at ~62 px/m (a "
          "1.75 m figure ≈ 60 px), enlarged 2× nearest-neighbour. No concept art, no paint-overs. "
          "Previews are stored as 192-colour PNGs; the floor/background (never the voxels) is "
          "lightly smoothed to remove Monte-Carlo grain.", ""]
    out = ROOT / "docs" / "reviews" / f"Claude_{batch}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L))
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
