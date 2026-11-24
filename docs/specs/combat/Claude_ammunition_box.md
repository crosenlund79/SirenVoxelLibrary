# Ammunition Box
- Asset ID: Claude_ammunition_box
- Base ID: ammunition_box
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Ammo storage/pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A surplus steel ammo can bought at a gun show to keep a hunter's cartridges dry. The olive paint is chipped bare along the lid edge and the latch, and a quiet stencil block on the side has faded to a dull khaki.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2875 m
- Depth (Y): 0.175 m
- Height (Z): 0.175 m
- Grid: 23 x 14 x 14 cells at 0.0125 m (micro tier), 1,264 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 7.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`green_deep`, `khaki_dark`, `olive`, `olive_dark`, `rust_dark`, `rust_deep`, `steel_dark`

## Details included
- Long, narrow, tall steel can with an overhanging lid lip
- Cam latch lever on the left end, pull tip worn bright
- Folding carry handle lying flat on the lid
- Rear lid hinge knuckles
- Faded stencil band as a plain colour block
- Chipped paint on the lid's front edge and a corner

## Details excluded
- No readable stencil text or lot numbers
- No visible cartridges

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2875 x 0.175 m

## Outputs
- `models/combat/Claude_ammunition_box/Claude_ammunition_box.vox` (editable master)
- `models/combat/Claude_ammunition_box/model.json`
- `models/combat/Claude_ammunition_box/Claude_ammunition_box.glb` (derived)
- `previews/combat/Claude_ammunition_box/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
