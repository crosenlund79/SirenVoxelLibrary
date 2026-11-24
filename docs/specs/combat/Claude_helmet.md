# Simple Helmet
- Asset ID: Claude_helmet
- Base ID: helmet
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Protective gear (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An army-surplus steel helmet bought for a costume decades ago and kept in a basement. Somebody wore it for real afterwards: the crown is sun-faded, the front rim is scraped to bare metal, the left side carries a dent, and the unbuckled chin strap trails on the ground.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.3625 m
- Depth (Y): 0.325 m
- Height (Z): 0.1625 m
- Grid: 29 x 26 x 13 cells at 0.0125 m (micro tier), 1,651 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [14.5, 13.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`green_deep`, `khaki`, `khaki_dark`, `olive`, `olive_dark`, `steel`, `steel_dark`

## Details included
- Round steel dome with a narrow rolled rim
- Sun-faded crown
- Rim scraped bare at the front
- Shallow dent on the left side
- Khaki webbing chin strap trailing from the left, steel buckle

## Details excluded
- No insignia, rank or unit markings
- No camouflage cover or net
- No visible liner or suspension

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.3625 x 0.325 m

## Outputs
- `models/combat/Claude_helmet/Claude_helmet.vox` (editable master)
- `models/combat/Claude_helmet/model.json`
- `models/combat/Claude_helmet/Claude_helmet.glb` (derived)
- `previews/combat/Claude_helmet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
