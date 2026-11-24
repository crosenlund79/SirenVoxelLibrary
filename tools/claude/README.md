# tools/claude — Claude's small voxel toolset

Creator: **Claude**. These scripts produce and check only `Claude_`-prefixed assets. They never read, write or move `GPT_` files. The renderer, validator and GLB exporter are creator-neutral, so they can be reused for fair side-by-side renders if the user wants.

| File | Purpose |
|---|---|
| `voxkit.py` | Shared Claude palette — v1 (pilot, 112 colours) and v2 (catalog: v1 unchanged plus 15 new material rows, 232 named roles) — one material ramp per 8-swatch row of MagicaVoxel's palette grid; a `Grid` canvas with drawing helpers (boxes, cylinders on any axis, ellipsoids, chamfered boxes, paste, mirror); and a MagicaVoxel VOX v150 writer/reader (`SIZE`, `XYZI`, `RGBA`). |
| `models/<base_id>.py` | One hand-designed generator per model, plus its `META` (story, resolution rationale, pivot, attachments). |
| `build.py` | Builds named generators: the `.vox`, cropped to occupancy with a ground-contact check, `model.json`, the derived `.glb` and a spec page in `docs/specs/`. Never writes `catalog.json`. Pilot IDs are frozen and delegate to `build_pilot.py` (palette v1, byte-identical rebuilds). |
| `catalog_sync.py` | Lead-only: merges every Claude `model.json` on disk into `catalog.json`; never modifies another creator's entries or a user-decided status. |
| `render_previews.py` | Catalog preview profile: hero 640 px, front/side 480 px, scale view at a fixed, stated px/m with the 1.75 m figure; same light and cameras as the pilot; `--quick --out DIR` for iteration renders. |
| `sheets.py` | One-scale contact sheets per batch and category, true game-camera readability strips (56°, ~62 px/m), showcase-scene rendering, thumbnail overview. |
| `scenes.py` | Showcase scenes (models placed together: dining set, pot on stove, tools on the bench, …). |
| `catalog_page.py` | Generates `catalog/index.html`, a static browser with thumbnails and viewer deep links. |
| `manifest.py` | Renders `docs/claude/MASTER_MANIFEST.md` from `docs/claude/manifest.json`, with status derived from files on disk. |
| `export_glb.py` | `.vox` → `.glb`: greedy-meshed visible faces, library → Godot axes `(x, z, −y)`, floor pivot, linear `COLOR_0` vertex colours, faceted normals. |
| `voxrender.py` (+ optional `vtrace.c`) | Ray tracer that renders the actual voxel cells: soft sun shadows, sky occlusion, seamless studio floor, orthographic cameras, 1.75 m reference mannequin. The C kernel compiles automatically with `gcc`; otherwise it falls back to numpy (same results, slower). |
| `preview.py` | Pilot-only (frozen): renders the pilot's 1200 px `hero / front / side / scale` and `previews/batches/Claude_pilot_001.png`. |
| `validate.py` | Format, bounds, count, dimension, pivot, connectivity (or documented pieces) and naming checks; independent comparisons with py-vox-io and Goxel; GLB bounds, orientation, winding and per-colour face-area checks; Khronos glTF-Validator; art lints (voxel budget, hidden interior fill, viewer cap). Select models by ID or `--batch`; `--fast` skips Goxel/Khronos. |
| `resolution_study.py`, `studies/` | Rendered evidence for the two resolution decisions that were tested side by side (a rejected 0.10 m rain-collector block-out and the pine at three cell sizes). |

## Catalog workflow

See `docs/claude/CATALOG_STYLE.md` for the production rules and `docs/claude/MASTER_MANIFEST.md` for the plan and status.

```bash
python3 tools/claude/build.py sofa                      # or --batch catalog_A
python3 tools/claude/render_previews.py sofa
python3 tools/claude/validate.py sofa                   # or --batch catalog_A; no args = whole library + catalog check
python3 tools/claude/catalog_sync.py && python3 tools/claude/catalog_page.py && python3 tools/claude/manifest.py
python3 tools/claude/sheets.py batch catalog_A && python3 tools/claude/sheets.py gamecam catalog_A
python3 tools/claude/scenes.py catalog_A
```

## Reproduce the pilot

```bash
pip install numpy pillow                     # required
pip install py-vox-io trimesh pygltflib      # optional independent checks
python3 tools/claude/build.py                # .vox, model.json, .glb, catalog
python3 tools/claude/preview.py              # previews + contact sheet (a few minutes)
python3 tools/claude/resolution_study.py
python3 tools/claude/validate.py
```

Optional external checks used for `Claude_pilot_001`: Goxel 0.11 (`apt install goxel xvfb`, run headless through `xvfb-run`) and the Khronos glTF-Validator (`npm install gltf-validator`, then set `GLTF_VALIDATOR_DIR` to the folder that contains `node_modules`).

Generators are deterministic, so re-running `build.py` reproduces byte-identical `.vox` files. The `.vox` files remain the editable masters: once the user edits one in MagicaVoxel, that file wins and the generator becomes history.
