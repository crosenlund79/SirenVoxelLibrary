# Metal Support Beam
- Asset ID: Claude_metal_support_beam
- Base ID: metal_support_beam
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Structural beam (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A rolled-steel column salvaged from a collapsed carport and stood up again on new bolts. Its paint is long gone; rust has taken the foot where water pooled and runs down from the cap plate.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.35 m
- Depth (Y): 0.35 m
- Height (Z): 2.55 m
- Grid: 7 x 7 x 51 cells at 0.05 m (detail tier), 743 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.5, 3.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`iron`, `iron_dark`, `iron_edge`, `rust_dark`, `rust_deep`, `steel_dark`

## Details included
- 0.25 m I-section column: two flanges and a web, open sides to +/-X
- Base and cap end plates with four nuts each, fillet welds at the joints
- Mill-scale dark steel with lit flange edges; rust at the foot and streaks from the cap

## Details excluded
- No paint
- No beam on top (separate module)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.35 x 0.35 m

## Outputs
- `models/construction/Claude_metal_support_beam/Claude_metal_support_beam.vox` (editable master)
- `models/construction/Claude_metal_support_beam/model.json`
- `models/construction/Claude_metal_support_beam/Claude_metal_support_beam.glb` (derived)
- `previews/construction/Claude_metal_support_beam/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
