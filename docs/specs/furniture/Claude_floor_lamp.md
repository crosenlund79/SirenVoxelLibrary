# Floor Lamp
- Asset ID: Claude_floor_lamp
- Base ID: floor_lamp
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Dead floor lamp; game prop 'floor_lamp' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The reading lamp behind the sofa. Its linen shade was knocked in the rush to leave and the near rim stayed dented; the cord still trails across the floor to a socket that has not worked for months.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.6 m
- Depth (Y): 0.7 m
- Height (Z): 1.6 m
- Grid: 12 x 14 x 32 cells at 0.05 m (detail tier), 315 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.5, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `bulb_warm`, `charcoal`, `cream`, `cream_mid`, `cream_shadow`, `iron`, `iron_edge`, `steel`, `steel_dark`

## Details included
- Weighted round iron base
- Thin dark pole with a lighter collar and switch
- Linen drum shade with trim bands, its near rim dented by a knock
- Unlit bulb inside the shade under a top diffuser
- Cord trailing across the floor

## Details excluded
- Nothing lit or glowing

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.35 x 0.35 m

## Outputs
- `models/furniture/Claude_floor_lamp/Claude_floor_lamp.vox` (editable master)
- `models/furniture/Claude_floor_lamp/model.json`
- `models/furniture/Claude_floor_lamp/Claude_floor_lamp.glb` (derived)
- `previews/furniture/Claude_floor_lamp/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
