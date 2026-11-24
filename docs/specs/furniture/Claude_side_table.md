# Side Table
- Asset ID: Claude_side_table
- Base ID: side_table
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Small table beside sofa/bed (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Bought new a month before everything stopped and still has its showroom finish. Its only mark is the cork coaster someone always remembered to use.

Condition: **lightly_used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.5 m
- Height (Z): 0.55 m
- Grid: 11 x 10 x 11 cells at 0.05 m (detail tier), 335 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`card`, `pine_hi`, `pine_light`, `sawdust`, `wood_stain`

## Details included
- Pale birch top on four square legs
- One drawer with a dark wooden knob
- Lower shelf between the legs
- A cork coaster on the top

## Details excluded
- No wear: it is the clean contrast to the worn pieces
- No glass or lamp on top (separate pickups)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.55 x 0.5 m

## Outputs
- `models/furniture/Claude_side_table/Claude_side_table.vox` (editable master)
- `models/furniture/Claude_side_table/model.json`
- `models/furniture/Claude_side_table/Claude_side_table.glb` (derived)
- `previews/furniture/Claude_side_table/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
