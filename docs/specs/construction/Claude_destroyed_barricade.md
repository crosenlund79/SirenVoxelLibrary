# Destroyed Barricade
- Asset ID: Claude_destroyed_barricade
- Base ID: destroyed_barricade
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Damage reference for wooden_barricade (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
What was left of the side-passage barricade the morning after: the near upright snapped at the foot, the far one still standing on its brace with a few planks nailed on, one swinging from a single nail, the rest lying where they fell.

Condition: **destroyed**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.55 m
- Height (Z): 1.35 m
- Grid: 20 x 11 x 27 cells at 0.05 m (detail tier), 487 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 4.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`break_fresh`, `iron_edge`, `pine_aged`, `pine_light`, `pine_mid`, `sage_dark`, `sage_deep`, `snag_light`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_mid`, `wgrey_warm`

## Details included
- Same uprights, brace feet and plank stock as Claude_wooden_barricade
- Far upright standing (1.35 m, splintered top) with broken plank stubs
- Near upright snapped into a stump, its upper half lying on the planks
- One broken plank hanging vertically from its last nail, foot on the pile
- Fallen planks lying in front, touching each other, the stump and the stubs

## Details excluded
- No fire or scorch marks
- No scattered single-voxel debris

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.4 m

## Outputs
- `models/construction/Claude_destroyed_barricade/Claude_destroyed_barricade.vox` (editable master)
- `models/construction/Claude_destroyed_barricade/model.json`
- `models/construction/Claude_destroyed_barricade/Claude_destroyed_barricade.glb` (derived)
- `previews/construction/Claude_destroyed_barricade/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
