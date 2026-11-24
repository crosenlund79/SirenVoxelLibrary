# Wheelie Bin
- Asset ID: Claude_trash_bin
- Base ID: trash_bin
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (game trash_bin) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A household wheelie bin left at the kerb for a collection that never came. The lid will not shut over the last black bag someone forced in, and the lid front is rubbed pale where hands lifted it every week.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.6 m
- Depth (Y): 0.55 m
- Height (Z): 0.95 m
- Grid: 12 x 11 x 19 cells at 0.05 m (detail tier), 909 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 5.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `charcoal`, `green`, `green_dark`, `green_deep`, `green_light`, `iron`, `porcelain_shadow`, `steel_dark`

## Details included
- Tapered body wider at the top, rolled rim
- Lid propped open at the front by a bulging black bag
- Two wheels on an axle and a moulded handle at the back (-Y)
- House number painted on the front as a plain pale block
- Grime band at the foot, rubbed lid lip

## Details excluded
- No readable numbers or council marks
- No loose litter

## Construction and placement notes
- Collision suggestion: Box 0.6 x 0.5 x 0.9 m; the lid gap is cosmetic.
- Placement footprint: 0.6 x 0.45 m

## Outputs
- `models/decorations/Claude_trash_bin/Claude_trash_bin.vox` (editable master)
- `models/decorations/Claude_trash_bin/model.json`
- `models/decorations/Claude_trash_bin/Claude_trash_bin.glb` (derived)
- `previews/decorations/Claude_trash_bin/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
