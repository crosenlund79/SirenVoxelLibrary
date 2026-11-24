# Wooden Foundation Support
- Asset ID: Claude_wooden_foundation_support
- Base ID: wooden_foundation_support
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Foundation module (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A cribbing pier stacked by a careful builder: old creosoted sleeper offcuts laid log-cabin fashion on a cast concrete pad, capped with a steel bearing plate.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.35 m
- Depth (Y): 0.35 m
- Height (Z): 1.2 m
- Grid: 7 x 7 x 24 cells at 0.05 m (detail tier), 707 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.5, 3.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig. Cribbing is read from its alternating crossed sleepers; at 0.1 m cells a 0.3 m pier is three cells and each sleeper a single cell, which reads as a chequered stick. At 0.05 m the 0.1 m sleepers keep their square ends and the overhang of each layer.

## Materials and colors
`bark_dark`, `concrete`, `concrete_dark`, `concrete_hi`, `pine_dark`, `steel`, `steel_dark`, `steel_light`, `wood_deep`, `wood_stain`

## Details included
- Cast concrete pad with chamfered top edges
- Ten layers of 0.1 m sleepers, each layer crossing the one below, ends overhanging the crossing by one cell
- Steel bearing plate on top with four lag bolts

## Details excluded
- No beam on top (separate module)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.35 x 0.35 m

## Outputs
- `models/construction/Claude_wooden_foundation_support/Claude_wooden_foundation_support.vox` (editable master)
- `models/construction/Claude_wooden_foundation_support/model.json`
- `models/construction/Claude_wooden_foundation_support/Claude_wooden_foundation_support.glb` (derived)
- `previews/construction/Claude_wooden_foundation_support/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
