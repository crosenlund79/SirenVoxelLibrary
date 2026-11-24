# Wooden Floor Section
- Asset ID: Claude_wooden_floor_section
- Base ID: wooden_floor_section
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Floor module 1x1 m (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A fresh deck module from a builder's merchant pallet: pine decking screwed square across three joists and a rim, nothing walked on it yet but the builder.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 1.0 m
- Height (Z): 0.2 m
- Grid: 10 x 10 x 2 cells at 0.1 m (standard tier), 130 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 5.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`pine_aged`, `pine_hi`, `pine_light`, `pine_mid`

## Details included
- Rim joists front and back, three joists along Y underneath
- Ten decking planks across the joists with staggered butt joints
- Fastener lines over each joist

## Details excluded
- No railing (separate module)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 1.0 m

## Outputs
- `models/construction/Claude_wooden_floor_section/Claude_wooden_floor_section.vox` (editable master)
- `models/construction/Claude_wooden_floor_section/model.json`
- `models/construction/Claude_wooden_floor_section/Claude_wooden_floor_section.glb` (derived)
- `previews/construction/Claude_wooden_floor_section/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
