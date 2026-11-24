# Double Bed
- Asset ID: Claude_double_bed
- Base ID: double_bed
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Main bed; game prop 'bed' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The parents' bed. Only the near side was slept in that last night: its pillow is still dented and skewed, and the mauve duvet was yanked up in a hurry before they left - square on the far side, rumpled and turned back on the near one.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.75 m
- Depth (Y): 2.1 m
- Height (Z): 0.9 m
- Grid: 35 x 42 x 18 cells at 0.05 m (detail tier), 4,306 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [17.5, 21.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`cream`, `cream_deep`, `cream_hi`, `cream_mid`, `mauve`, `mauve_dark`, `mauve_hi`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`

## Details included
- Honey-oak frame with a panelled headboard and a low footboard
- Mauve duvet pulled up crookedly, hanging lower on the near (-X) side
- Near side slept in: turned-back fold, sheet showing, dented pillow
- Far side neat: plump pillow, duvet up to it

## Details excluded
- No throw cushions
- No pattern on the bedding

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.65 x 2.1 m

## Outputs
- `models/furniture/Claude_double_bed/Claude_double_bed.vox` (editable master)
- `models/furniture/Claude_double_bed/model.json`
- `models/furniture/Claude_double_bed/Claude_double_bed.glb` (derived)
- `previews/furniture/Claude_double_bed/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a2_bedroom_office.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
