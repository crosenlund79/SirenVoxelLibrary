# Wooden Beam
- Asset ID: Claude_wooden_beam
- Base ID: wooden_beam
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Structural beam (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A short glulam beam bought for a carport that never went up; a fabricator welded steel end plates on so it bolts straight between two posts.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.3 m
- Height (Z): 0.3 m
- Grid: 20 x 6 x 6 cells at 0.05 m (detail tier), 288 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 3.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig. Its glulam laminations (~4 cm) and the bolted end plates only exist at 0.05 m; at 0.1 m the beam is a 2 x 2 stick with a 10 cm steel slab on each end.

## Materials and colors
`charcoal`, `pine_hi`, `pine_light`, `pine_mid`, `steel`, `steel_dark`, `steel_light`

## Details included
- Four visible laminations along the length
- Steel end plates wider and taller than the timber, four bolt holes each
- Two through-bolts near each end on both faces (knife-plate connection)

## Details excluded
- No posts (separate module)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.3 m

## Outputs
- `models/construction/Claude_wooden_beam/Claude_wooden_beam.vox` (editable master)
- `models/construction/Claude_wooden_beam/model.json`
- `models/construction/Claude_wooden_beam/Claude_wooden_beam.glb` (derived)
- `previews/construction/Claude_wooden_beam/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
