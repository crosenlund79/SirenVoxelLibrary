# Dresser
- Asset ID: Claude_dresser
- Base ID: dresser
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Chest of drawers; lootable; game prop 'dresser' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An old mahogany chest of drawers handed down twice. Its top drawer was yanked out and emptied in a hurry - only the rucked lining paper is left - and the drawer below the middle was shoved shut on a jumper sleeve.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.25 m
- Depth (Y): 0.85 m
- Height (Z): 0.9 m
- Grid: 25 x 17 x 18 cells at 0.05 m (detail tier), 1,883 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `cream_mid`, `leather`, `leather_dark`, `leather_deep`, `leather_hi`, `paper`, `pine_aged`, `sage`, `sage_dark`

## Details included
- Four drawers in a mahogany frame on bracket feet, brass pulls
- Top drawer pulled right out and empty, lining paper rucked up
- A sage jumper sleeve caught in a closed drawer, hanging down the front
- Finish rubbed pale along the top's front edge

## Details excluded
- No mirror
- No clutter on top

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.25 x 0.5 m

## Outputs
- `models/furniture/Claude_dresser/Claude_dresser.vox` (editable master)
- `models/furniture/Claude_dresser/model.json`
- `models/furniture/Claude_dresser/Claude_dresser.glb` (derived)
- `previews/furniture/Claude_dresser/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
