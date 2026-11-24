# Dining Chair
- Asset ID: Claude_dining_chair
- Base ID: dining_chair
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Dining chair; game prop 'chair' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
One of the six chairs bought with the oak dining table. Its seat front and crest rail are rubbed pale by years of hands pulling it out, and one spindle that snapped was replaced with a darker one from the hardware shop.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.45 m
- Depth (Y): 0.5 m
- Height (Z): 0.9 m
- Grid: 9 x 10 x 18 cells at 0.05 m (detail tier), 207 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.5, 5.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`pine_aged`, `pine_hi`, `pine_light`, `pine_mid`, `wood_stain`

## Details included
- Same oak, tones and H-stretcher as Claude_dining_table
- Spindle back with a deep crest rail
- One replaced, darker spindle
- Seat front and crest rail rubbed pale

## Details excluded
- No seat pad

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.45 x 0.5 m

## Outputs
- `models/furniture/Claude_dining_chair/Claude_dining_chair.vox` (editable master)
- `models/furniture/Claude_dining_chair/model.json`
- `models/furniture/Claude_dining_chair/Claude_dining_chair.glb` (derived)
- `previews/furniture/Claude_dining_chair/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
