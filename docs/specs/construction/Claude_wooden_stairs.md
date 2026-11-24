# Simple Wooden Stairs
- Asset ID: Claude_wooden_stairs
- Base ID: wooden_stairs
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Porch/deck stairs (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Porch steps cut from new lumber last week: two notched stringers, five two-board treads and a precast pad at the foot. The first muddy boots have already worn a path up the middle.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.1 m
- Depth (Y): 1.7 m
- Height (Z): 1.0 m
- Grid: 11 x 17 x 10 cells at 0.1 m (standard tier), 283 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the foot of the stairs (the approach side); they rise toward -Y.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.5, 8.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`concrete`, `concrete_dark`, `pine_aged`, `pine_hi`, `pine_light`, `pine_mid`

## Details included
- Two cut (sawtooth) stringers flush with the tread ends, darker than the treads
- Five treads of two boards each rising 0.2 m per step to 1.0 m
- Precast concrete pad at the foot
- A darker walking path on the lower treads

## Details excluded
- No handrail
- No deck at the top (stairs hang from the deck rim)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.1 x 1.7 m

## Outputs
- `models/construction/Claude_wooden_stairs/Claude_wooden_stairs.vox` (editable master)
- `models/construction/Claude_wooden_stairs/model.json`
- `models/construction/Claude_wooden_stairs/Claude_wooden_stairs.glb` (derived)
- `previews/construction/Claude_wooden_stairs/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
