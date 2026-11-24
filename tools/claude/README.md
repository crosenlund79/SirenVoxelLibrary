# tools/claude — Claude's small voxel toolset

Creator: **Claude**. These scripts produce and check only `Claude_`-prefixed assets. They never read, write or move `GPT_` files. The renderer, validator and GLB exporter are creator-neutral, so they can be reused for fair side-by-side renders if the user wants.

| File | Purpose |
|---|---|
| `voxkit.py` | Shared Claude palette (one material ramp per 8-swatch row of MagicaVoxel's palette grid), a tiny `Grid` canvas, and a MagicaVoxel VOX v150 writer/reader (`SIZE`, `XYZI`, `RGBA`). |
| `models/<base_id>.py` | One hand-designed generator per model, plus its `META` (story, resolution rationale, pivot, attachments). |
| `build.py` | Builds the `.vox`, crops it to occupancy, checks ground contact, writes `model.json` and the derived `.glb`, and merges `Claude_` records into `catalog.json` without touching other creators' entries. |
| `export_glb.py` | `.vox` → `.glb`: greedy-meshed visible faces, library → Godot axes `(x, z, −y)`, floor pivot, linear `COLOR_0` vertex colours, faceted normals. |
| `voxrender.py` (+ optional `vtrace.c`) | Ray tracer that renders the actual voxel cells: soft sun shadows, sky occlusion, seamless studio floor, orthographic cameras, 1.75 m reference mannequin. The C kernel compiles automatically with `gcc`; otherwise it falls back to numpy (same results, slower). |
| `preview.py` | Renders `hero / front / side / scale` for every Claude candidate **from the `.vox` files on disk**, plus `previews/batches/Claude_pilot_001.png`. |
| `validate.py` | Format, bounds, count, dimension, pivot, connectivity and naming checks; independent comparisons with py-vox-io and Goxel; GLB bounds, orientation, winding and per-colour face-area checks; Khronos glTF-Validator. |
| `resolution_study.py`, `studies/` | Rendered evidence for the two resolution decisions that were tested side by side (a rejected 0.10 m rain-collector block-out and the pine at three cell sizes). |

## Reproduce

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
