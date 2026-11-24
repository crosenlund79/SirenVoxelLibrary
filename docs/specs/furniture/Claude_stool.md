# Stool
- Asset ID: Claude_stool
- Base ID: stool
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Kitchen stool; game prop 'stool' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The kitchen stool everyone perched on to talk to the cook. Its seat is rubbed pale in the middle and the front footrest is worn to bare wood by heels.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.45 m
- Depth (Y): 0.45 m
- Height (Z): 0.7 m
- Grid: 9 x 9 x 14 cells at 0.05 m (detail tier), 161 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.5, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `wood_stain`

## Details included
- Round-ish seat with a pale, worn centre
- Four square legs with a seat rail
- Footrest rungs on all four sides, the front one heel-worn

## Details excluded
- No cushion

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.45 x 0.45 m

## Outputs
- `models/furniture/Claude_stool/Claude_stool.vox` (editable master)
- `models/furniture/Claude_stool/model.json`
- `models/furniture/Claude_stool/Claude_stool.glb` (derived)
- `previews/furniture/Claude_stool/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
