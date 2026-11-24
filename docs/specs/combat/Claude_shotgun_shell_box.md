# Shotgun Shell Box
- Asset ID: Claude_shotgun_shell_box
- Base ID: shotgun_shell_box
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Shotgun ammo pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A fresh box of shotgun shells from a hardware store's back shelf, opened for the first time: the lid is folded back and two shells have been taken out and set down in front of it.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.225 m
- Depth (Y): 0.175 m
- Height (Z): 0.2125 m
- Grid: 18 x 14 x 17 cells at 0.0125 m (micro tier), 1,066 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 7.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`brass`, `card`, `card_deep`, `card_hi`, `label_cream`, `label_green`, `red`, `red_dark`

## Details included
- Printed card box (muted green with a cream band) with its lid standing open
- Three rows of five shells standing brass-up, two gaps where shells were taken
- Two loose shells against the box (one lying, one standing on its head): red hulls, brass heads, crimped ends

## Details excluded
- No brand, gauge or text printing
- No loose powder or wads

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.225 x 0.175 m

## Outputs
- `models/combat/Claude_shotgun_shell_box/Claude_shotgun_shell_box.vox` (editable master)
- `models/combat/Claude_shotgun_shell_box/model.json`
- `models/combat/Claude_shotgun_shell_box/Claude_shotgun_shell_box.glb` (derived)
- `previews/combat/Claude_shotgun_shell_box/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
