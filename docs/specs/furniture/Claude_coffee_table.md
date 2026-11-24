# Coffee Table
- Asset ID: Claude_coffee_table
- Base ID: coffee_table
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Living-room table; game prop 'coffee_table' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A solid oak coffee table that took the knocks of a family living room: the front corner was chipped when the sofa was dragged past it and never filled, and the shelf underneath still holds the last week's paper and two magazines.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.15 m
- Depth (Y): 0.6 m
- Height (Z): 0.45 m
- Grid: 23 x 12 x 9 cells at 0.05 m (detail tier), 782 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bluegrey_hi`, `cream_mid`, `cream_shadow`, `paper`, `pine_aged`, `pine_hi`, `pine_light`, `pine_mid`, `terra_hi`

## Details included
- Three-board oak top with softened corners and a chipped front corner
- Square legs, plain apron
- Lower shelf with a folded newspaper and magazines

## Details excluded
- No mugs or remotes baked on top (separate pickups)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.15 x 0.6 m

## Outputs
- `models/furniture/Claude_coffee_table/Claude_coffee_table.vox` (editable master)
- `models/furniture/Claude_coffee_table/model.json`
- `models/furniture/Claude_coffee_table/Claude_coffee_table.glb` (derived)
- `previews/furniture/Claude_coffee_table/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
