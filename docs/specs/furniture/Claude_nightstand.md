# Nightstand
- Asset ID: Claude_nightstand
- Base ID: nightstand
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Bedside table; game prop 'nightstand' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The near-side nightstand, from the same honey-oak set as the double bed. The drawer was pulled open for a phone charger that was not there; the wind-up alarm clock stopped at some small hour and a paperback lies where it was put down.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.5 m
- Depth (Y): 0.6 m
- Height (Z): 0.65 m
- Grid: 10 x 12 x 13 cells at 0.05 m (detail tier), 502 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `brass`, `brass_dark`, `paper`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `porcelain_hi`, `terra_dark`

## Details included
- Drawer over an open shelf, drawer pulled a little open
- Twin-bell alarm clock with a pale face
- A paperback lying on top

## Details excluded
- No lamp (separate model)
- No phone or charger

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.5 x 0.45 m

## Outputs
- `models/furniture/Claude_nightstand/Claude_nightstand.vox` (editable master)
- `models/furniture/Claude_nightstand/model.json`
- `models/furniture/Claude_nightstand/Claude_nightstand.glb` (derived)
- `previews/furniture/Claude_nightstand/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
