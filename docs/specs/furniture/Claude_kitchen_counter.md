# Kitchen Base Unit
- Asset ID: Claude_kitchen_counter
- Base ID: kitchen_counter
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Modular base unit; game prop 'counter' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The everyday prep counter beside the cooker. The left drawer, where the cutlery lived, was yanked open by someone looking for a knife and left out; the paint is rubbed through to the wood where hands pulled the doors for years.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.25 m
- Depth (Y): 0.7 m
- Height (Z): 0.9 m
- Grid: 25 x 14 x 18 cells at 0.05 m (detail tier), 1,945 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 6.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `pine_hi`, `pine_light`, `pine_mid`, `sage`, `sage_dark`, `sage_deep`, `sage_hi`

## Details included
- Two sage shaker doors under two slab drawers, charcoal bar handles
- Oiled pine worktop with a forearm-pale front edge in the work zone
- Recessed toe kick; carcass reveals read as dark grooves
- Left (cutlery) drawer pulled out 5 cm, its pine box sides showing
- Paint rubbed to bare wood beside the handles of the left door

## Details excluded
- No baked-on clutter (board, kettle and crockery are separate pickups)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.25 x 0.65 m

## Outputs
- `models/furniture/Claude_kitchen_counter/Claude_kitchen_counter.vox` (editable master)
- `models/furniture/Claude_kitchen_counter/model.json`
- `models/furniture/Claude_kitchen_counter/Claude_kitchen_counter.glb` (derived)
- `previews/furniture/Claude_kitchen_counter/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
