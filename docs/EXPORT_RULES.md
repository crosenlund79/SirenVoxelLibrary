# Production, Formats and Export Rules

## 1. Source of truth

**`source.vox` is the editable master.** Never substitute a screenshot, a raster sprite, or a baked polygon mesh for it.

For each model `<category>/<asset_id>`, use:

```text
models/<category>/<asset_id>/
  source.vox            # canonical editable source
  model.json            # machine-readable metadata
  model.glb             # optional generated Godot-ready mesh
previews/<category>/<asset_id>/
  hero.png
  front.png
  side.png
  scale.png
docs/specs/<category>/<asset_id>.md
```

Derived exports are reproducible from the source and should not be edited by hand. This path convention is the default; if the pilot requires a different scheme, document the change before generating many assets.

## 2. Required metadata

A per-model `model.json` must include the following minimal information. Example values below are illustrative, not an approved model:

```json
{
  "schema_version": 1,
  "id": "example_workbench",
  "name": "Example Workbench",
  "category": "furniture",
  "revision": 1,
  "status": "candidate",
  "source": "source.vox",
  "voxel_size_m": 0.1,
  "source_axes": {"right": "+X", "front": "+Y", "up": "+Z"},
  "godot_forward": "-Z",
  "pivot_voxel": [8.5, 3.5, 0.0],
  "dimensions_m": [1.7, 0.7, 0.9],
  "occupied_voxels": 1250,
  "material_roles": ["aged_pine", "dark_steel"],
  "game_integration": []
}
```

`pivot_voxel` is in **voxel-coordinate units** measured from the source grid's minimum corner; it may use half-cell coordinates to express a centred floor pivot. `dimensions_m` are (X width, Y depth, Z height). Source model world dimensions should be consistent with occupied extents and `voxel_size_m`. If the model uses additional intentional empty space or offsets, document them.

**Catalog status versus metadata status:** the catalog is the review index. Before publishing, ensure the catalog and model metadata agree; never claim `approved` without explicit user approval.

## 3. Formats

**Required:**
- `.vox` in a documented MagicaVoxel-compatible VOX format with a valid palette and actual occupied voxel data.
- `model.json` as described above.
- Actual model renders (`.png`) captured from the voxel model, not AI images presented as evidence of a finished asset.

**Optional:**
- `.glb` for efficient rendering in Godot or other 3D engines.
- A lossless raw-voxel interchange file for consumers that explicitly need voxel data.

Prefer simple MagicaVoxel `SIZE`, `XYZI`, `RGBA` for the pilot. Respect the format's **single-model 256-cell axis limits and palette conventions**; for larger objects, design a deliberate multi-model scene or split instead of silently truncating data. Validate compatibility with the target editor before claiming that it opens correctly.

A `.glb` is a **derived mesh**, not an editable voxel master and not a guarantee of destructive in-game voxel behavior.

## 4. Geometry and mesh conversion

- Store exact cell size in metres and coordinate convention per model.
- On export, convert library (X right, Y front, Z up) to Godot (X right, Y up, Z front-negative), then apply the metadata pivot offset. Test the mapping with an unmistakably asymmetric object.
- Export visible surfaces only; avoid a separate triangle mesh for every hidden cube face.
- Use palette colors/material roles consistently. Preserve the broad silhouette and material separation.
- Prefer greedy meshing for same-material coplanar faces when safe; do not merge across required material or transparency boundaries.
- Avoid a giant collection of runtime nodes per voxel.
- Mesh collision in Godot should generally use simplified game-specific collision, not every rendered triangle. The game controls that choice.
- Avoid invented surface normals or smoothing that melts blocky geometry. Faceted voxel surfaces are intentional.

## 5. Test and acceptance gate

On every candidate model, verify:
1. File is actually a valid voxel asset; loader/parser can read occupied voxel entries and palette.
2. All voxel coordinates are within declared bounds; no duplicates or invalid material indices.
3. Occupied count agrees with `model.json`.
4. Bounds times resolution agree with stated metres, or differences are explicitly documented.
5. Pivot, support plane and forward direction match the contract.
6. Rendered hero/front/side/scale previews derive from the same source.
7. Scale view includes a 1.75 m human reference.
8. Geometry is legible at the intended game camera distance.
9. If `.glb` is produced: parse/open it in a compatible viewer or Godot, verify proportions, axis orientation, colors and absence of missing faces.
10. Review approves the art; automated success alone never substitutes for human selection.

Report tool/runtime restrictions honestly. If MagicaVoxel itself is not available, a format parser and another viewer can validate the VOX binary structure, but mark **actual MagicaVoxel GUI open** as unverified until tested.

## 6. Import into Sirens Went Quiet

Do **not** copy directly to the game when creating a model.

Once the user selects an approved model for a game:
- Copy or vendor the **specific approved revision** with provenance (asset id, source commit SHA, license/ownership note, revision).
- Choose the *render path*: static `.glb` for ordinary props, or an explicit grid conversion for objects that truly need per-voxel destruction.
- Account for potential mismatch between model cell size and the game's structural voxel size.
- Check correct scale, rotation, pivot, placement footprint, occlusion and performance in the actual game camera.
- Preserve a straightforward way to replace customized artwork where the receiving project's policy requires it.
- Mark the specific game integration in catalog metadata only after it has actually happened.

Do not automatically add a submodule, package dependency, Godot plugin or runtime library loader. Manual, traceable selective copying is the initial approach.
